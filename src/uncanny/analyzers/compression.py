"""
Compression-based AI detection (Zippy-style).

AI text is more predictable and compresses better than human text.
Uses cross-compression: compress sample alongside a large AI-generated prelude.
If the sample compresses well with the AI prelude, it shares statistical patterns.

Uses both LZMA and zlib for two independent signals.
"""

from __future__ import annotations

import lzma
import zlib

from uncanny.analyzers.base import Analyzer
from uncanny.tokenizer import split_sentences
from uncanny.types import AnalyzerResult, SentenceScore

# Large AI-generated prelude to prime the compression dictionary.
# Diversity of topics ensures broad pattern matching.
_AI_PRELUDE = (
    "The implementation of this feature requires careful consideration of several "
    "architectural patterns to ensure maintainability and scalability. By leveraging "
    "existing infrastructure components, we can achieve seamless integration while "
    "minimizing technical debt. This approach provides a robust and comprehensive "
    "solution that addresses the identified requirements effectively. Furthermore, "
    "the modular design enables future extensibility and facilitates testing across "
    "multiple deployment scenarios. It is important to note that the proposed "
    "architecture follows industry best practices and established design principles. "
    "The systematic evaluation of available alternatives demonstrates that this "
    "approach optimally balances performance constraints with development velocity. "
    "Additionally, the proposed solution incorporates comprehensive error handling "
    "mechanisms and provides detailed logging capabilities for operational visibility. "
    "In the context of modern software development, the adoption of microservices "
    "architecture has become increasingly prevalent among organizations seeking to "
    "improve their deployment frequency and operational resilience. The transition "
    "from monolithic systems to distributed architectures presents both opportunities "
    "and challenges that must be carefully evaluated. Key considerations include "
    "service discovery, load balancing, and inter-service communication protocols. "
    "The proliferation of cloud-native technologies has fundamentally transformed "
    "the landscape of enterprise software development. Container orchestration "
    "platforms such as Kubernetes provide a standardized approach to managing "
    "distributed workloads across heterogeneous infrastructure environments. "
    "The integration of continuous integration and continuous deployment pipelines "
    "enables teams to deliver software updates with greater frequency and reliability. "
    "Machine learning models have demonstrated remarkable capabilities across a wide "
    "spectrum of applications, from natural language processing to computer vision. "
    "The training process involves optimizing model parameters through iterative "
    "exposure to labeled datasets, enabling the model to learn complex patterns "
    "and relationships within the data. Transfer learning techniques allow "
    "practitioners to leverage pre-trained models, significantly reducing the "
    "computational resources required for domain-specific applications. "
    "Effective project management requires a thorough understanding of stakeholder "
    "requirements and a systematic approach to resource allocation. By establishing "
    "clear communication channels and defining measurable objectives, teams can "
    "maintain alignment throughout the development lifecycle. Regular retrospectives "
    "provide opportunities for continuous improvement and process optimization. "
    "The security implications of deploying applications in cloud environments "
    "necessitate a comprehensive approach to identity management and access control. "
    "Implementing zero-trust security models ensures that all network communications "
    "are authenticated and encrypted, regardless of their origin or destination."
)

_HUMAN_PRELUDE = (
    "So I tried like three different approaches before landing on this one honestly. "
    "The weird part was the timeout — still not 100% sure why it happens on cold "
    "starts but whatever, the retry logic handles it. Honestly the code is kind of "
    "ugly in that section, I'll clean it up later maybe. Dave suggested using Redis "
    "but that felt like overkill for what we need right now. Oh also, the tests are "
    "flaky on CI sometimes because of the mock server timing out, been meaning to "
    "fix that for weeks. Anyway the PR is up if you wanna take a look, no rush tho. "
    "I grabbed lunch at that new place on 5th, pretty good actually. Tomorrow I need "
    "to figure out the auth flow because the token refresh is broken again. "
    "ok so I've been banging my head against this for two days and I'm about to lose "
    "it. I swear the config was working yesterday but now everything's undefined? "
    "Checked the env vars like 5 times. Restarted the server. Cleared all caches. "
    "Nothing. Then Jake casually mentions 'oh yeah I renamed that variable' in "
    "standup this morning. Bro. TELL PEOPLE WHEN YOU DO THAT. "
    "lol so the client called and they want the whole dashboard redesigned before "
    "friday. like, the WHOLE thing. I told sarah we literally can't do that and she "
    "was like 'well we promised them' ??? since when?? anyway i'm just gonna mock "
    "something up in figma real quick and see if they'll accept incremental changes "
    "instead of the full rewrite they're asking for. fingers crossed. "
    "my cat walked across my keyboard during a production deploy and somehow "
    "nothing broke?? honestly that's more concerning than if it had. either our "
    "CI is really good or really bad and i don't want to find out which. "
    "quick question — has anyone gotten hot module replacement to actually work "
    "with the new bundler? mine just refreshes the whole page every time which "
    "defeats the entire purpose. tried the docs, tried stackoverflow, tried "
    "yelling at my monitor. the monitor didn't help. "
    "update on the database migration: it's mostly done but there's this one table "
    "with like 50M rows that takes forever to alter. I'm running it in batches "
    "overnight but it keeps dying around 3am because the connection pool times out. "
    "gonna try bumping the timeout to something ridiculous and just let it cook. "
    "worst case we do it over the weekend when nobody's using the system."
)


def _compress_size(data: bytes, method: str) -> int:
    if method == "lzma":
        return len(lzma.compress(data, preset=3))
    return len(zlib.compress(data, level=6))


def _cross_compress_score(text: str) -> float:
    """
    Cross-compression scoring using both LZMA and zlib.

    For each compressor:
    1. Compress prelude alone
    2. Compress prelude + sample
    3. Delta = combined - prelude_alone
    4. Compare AI delta vs human delta

    Returns 0-1 where higher = more AI-like.
    """
    sample_bytes = text.encode("utf-8")
    ai_bytes = _AI_PRELUDE.encode("utf-8")
    human_bytes = _HUMAN_PRELUDE.encode("utf-8")

    scores = []
    for method in ("lzma", "zlib"):
        ai_base = _compress_size(ai_bytes, method)
        human_base = _compress_size(human_bytes, method)

        ai_combined = _compress_size(ai_bytes + sample_bytes, method)
        human_combined = _compress_size(human_bytes + sample_bytes, method)

        ai_delta = ai_combined - ai_base
        human_delta = human_combined - human_base

        total = ai_delta + human_delta
        if total == 0:
            scores.append(0.5)
            continue

        # Lower ai_delta means sample compresses better with AI prelude
        raw = 1.0 - (ai_delta / total)

        # Amplify the signal — raw values cluster around 0.5
        # Apply sigmoid-like stretching centered at 0.5
        centered = (raw - 0.5) * 10.0  # amplify differences
        import math
        stretched = 1.0 / (1.0 + math.exp(-centered))

        scores.append(stretched)

    return sum(scores) / len(scores)


class CompressionAnalyzer(Analyzer):
    """Detects AI text using compression ratio analysis."""

    name = "compression"

    def analyze(self, text: str) -> AnalyzerResult:
        sentences = split_sentences(text)

        sentence_scores: list[SentenceScore] = []
        for sent_text, start, end in sentences:
            if len(sent_text.strip()) < 20:
                sentence_scores.append(SentenceScore(sent_text, 0.5, start, end))
                continue

            score = _cross_compress_score(sent_text)
            sentence_scores.append(SentenceScore(sent_text, score, start, end))

        # Overall score on full text
        if text.strip() and len(text) >= 20:
            overall = _cross_compress_score(text)
        else:
            overall = 0.5

        return AnalyzerResult(
            name=self.name,
            score=overall,
            sentence_scores=sentence_scores,
            metadata={"method": "lzma+zlib"},
        )
