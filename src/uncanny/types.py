from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SentenceScore:
    text: str
    score: float  # 0.0 = human, 1.0 = AI
    start: int
    end: int


@dataclass
class AnalyzerResult:
    name: str
    score: float  # 0.0 = human, 1.0 = AI
    sentence_scores: list[SentenceScore] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class ScanResult:
    source: str | None
    score: float
    label: str
    analyzers: dict[str, AnalyzerResult] = field(default_factory=dict)
    sentences: list[SentenceScore] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "score": round(self.score, 2),
            "label": self.label,
            "analyzers": {
                name: {
                    "score": round(r.score, 2),
                    **r.metadata,
                }
                for name, r in self.analyzers.items()
            },
            "sentences": [
                {
                    "text": s.text,
                    "score": round(s.score, 2),
                    "offset": {"start": s.start, "end": s.end},
                }
                for s in self.sentences
            ],
        }
