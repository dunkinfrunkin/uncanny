"""
Competitor implementations for benchmarking comparison.

Implements the core algorithm of each competitor so we can compare
accuracy and performance on the same corpus.
"""

from __future__ import annotations

import lzma
import re
import zlib
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Zippy (Thinkst) — compression-ratio differential analysis
# https://github.com/thinkst/zippy
#
# Algorithm:
# 1. Compress a large AI-generated prelude text
# 2. Compress prelude + sample together
# 3. Compare compression ratios
# 4. If sample compresses better with prelude (negative delta), it's AI
# ---------------------------------------------------------------------------

# Zippy uses an 87KB AI-generated prelude. We use a representative subset
# that captures the same statistical properties.
_ZIPPY_PRELUDE = (
    "Certainly! Here is an example of a personal profile:\n\n"
    "My name is Emily Johnson and I am a 28-year-old marketing professional "
    "living in New York City. I graduated from New York University with a degree "
    "in Marketing and have been working in the industry for the past six years. "
    "Currently, I am employed as a Senior Marketing Manager at a tech startup "
    "where I am responsible for developing and executing marketing strategies to "
    "drive growth and brand awareness. In my free time, I enjoy exploring the "
    "city's diverse food scene, practicing yoga, and volunteering at a local "
    "animal shelter. I am passionate about using my skills to make a positive "
    "impact in the world and am always looking for new opportunities to learn "
    "and grow both personally and professionally.\n\n"
    "The history of the Internet is a fascinating journey that began in the late "
    "1960s with the creation of ARPANET, a project funded by the United States "
    "Department of Defense. ARPANET was designed to enable communication between "
    "research institutions and government agencies, and it laid the groundwork "
    "for what would eventually become the modern Internet. In the 1970s, the "
    "development of TCP/IP protocols standardized how data was transmitted across "
    "networks, making it possible for different computer systems to communicate "
    "with each other seamlessly. The 1980s saw the expansion of networking "
    "technologies beyond military and academic settings, with the introduction "
    "of commercial Internet service providers. The creation of the World Wide "
    "Web by Tim Berners-Lee in 1989 revolutionized how information was accessed "
    "and shared, introducing concepts like hyperlinks and web browsers that made "
    "the Internet accessible to the general public. Throughout the 1990s and "
    "2000s, the Internet experienced exponential growth, transforming industries "
    "from retail to entertainment and fundamentally changing how people interact "
    "with information and each other.\n\n"
    "Artificial intelligence has emerged as one of the most transformative "
    "technologies of the 21st century. Machine learning algorithms, particularly "
    "deep learning models, have demonstrated remarkable capabilities in tasks "
    "ranging from image recognition to natural language processing. The development "
    "of large language models has enabled computers to generate human-like text, "
    "translate between languages, and engage in complex reasoning tasks. These "
    "advancements have significant implications for industries including healthcare, "
    "where AI systems can assist in diagnosing diseases and developing treatment "
    "plans, and education, where personalized learning experiences can be created "
    "based on individual student needs. However, the rapid advancement of AI "
    "technology also raises important ethical considerations, including concerns "
    "about bias in training data, the potential for job displacement, and the "
    "need for transparent and accountable AI systems. As the field continues to "
    "evolve, it is essential that researchers, policymakers, and society as a "
    "whole engage in thoughtful discussions about how to harness the benefits of "
    "AI while mitigating its risks.\n\n"
    "The impact of climate change on global ecosystems represents one of the most "
    "pressing challenges facing humanity today. Rising temperatures have led to "
    "significant changes in weather patterns, resulting in more frequent and severe "
    "natural disasters including hurricanes, droughts, and wildfires. The melting "
    "of polar ice caps and glaciers has contributed to rising sea levels, "
    "threatening coastal communities and small island nations. Biodiversity loss "
    "has accelerated as species struggle to adapt to rapidly changing environmental "
    "conditions. The scientific consensus, supported by organizations such as the "
    "Intergovernmental Panel on Climate Change, emphasizes the urgent need for "
    "coordinated global action to reduce greenhouse gas emissions and transition "
    "to sustainable energy sources. Governments, businesses, and individuals all "
    "have important roles to play in addressing this crisis and ensuring a "
    "sustainable future for generations to come."
)


def _clean_text(text: str) -> str:
    """Zippy's text preprocessing."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s.,!?;:'\"-]", "", text)
    return text.strip()


@dataclass
class ZippyResult:
    score: float  # 0-1, higher = more AI-like
    label: str
    method: str
    delta: float  # raw compression delta


def _zippy_detect(text: str, method: str = "lzma") -> ZippyResult:
    """
    Faithful reimplementation of Zippy's core algorithm.

    Compresses prelude alone, then prelude + sample.
    Compares compression ratios to determine if sample is AI-like.
    """
    text = _clean_text(text)
    prelude = _ZIPPY_PRELUDE
    prelude_bytes = prelude.encode("utf-8")
    sample_bytes = text.encode("utf-8")
    combined_bytes = prelude_bytes + b" " + sample_bytes

    if method == "lzma":
        prelude_compressed = len(lzma.compress(prelude_bytes, preset=4))
        combined_compressed = len(lzma.compress(combined_bytes, preset=4))
    else:  # zlib
        prelude_compressed = len(zlib.compress(prelude_bytes, level=6))
        combined_compressed = len(zlib.compress(combined_bytes, level=6))

    prelude_ratio = prelude_compressed / len(prelude_bytes)
    combined_ratio = combined_compressed / len(combined_bytes)

    delta = combined_ratio - prelude_ratio

    # Zippy: negative delta = AI (compresses better with prelude)
    # Convert to 0-1 score: more negative delta = higher AI probability
    # Typical deltas: AI text -0.02 to -0.001, human text 0.001 to 0.03
    if delta <= 0:
        score = min(0.5 + abs(delta) * 25, 1.0)
    else:
        score = max(0.5 - delta * 25, 0.0)

    if score >= 0.5:
        label = "AI"
    else:
        label = "Human"

    return ZippyResult(score=score, label=label, method=method, delta=delta)


def zippy_ensemble(text: str) -> ZippyResult:
    """Zippy's ensemble approach: average of LZMA and zlib."""
    lzma_result = _zippy_detect(text, "lzma")
    zlib_result = _zippy_detect(text, "zlib")

    avg_score = (lzma_result.score + zlib_result.score) / 2
    avg_delta = (lzma_result.delta + zlib_result.delta) / 2

    return ZippyResult(
        score=avg_score,
        label="AI" if avg_score >= 0.5 else "Human",
        method="ensemble",
        delta=avg_delta,
    )


# ---------------------------------------------------------------------------
# Naive baseline — random chance (for comparison)
# ---------------------------------------------------------------------------

def naive_baseline(text: str) -> float:
    """Always returns 0.5 — random chance baseline."""
    return 0.5
