from __future__ import annotations

from abc import ABC, abstractmethod

from uncanny.types import AnalyzerResult


class Analyzer(ABC):
    """Base class for all detection analyzers."""

    name: str

    @abstractmethod
    def analyze(self, text: str) -> AnalyzerResult:
        """Analyze text and return a result with overall + sentence scores."""
        ...
