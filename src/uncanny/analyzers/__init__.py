from uncanny.analyzers.base import Analyzer
from uncanny.analyzers.compression import CompressionAnalyzer
from uncanny.analyzers.burstiness import BurstinessAnalyzer

__all__ = ["Analyzer", "CompressionAnalyzer", "BurstinessAnalyzer"]

# Perplexity analyzer requires optional ML dependencies
try:
    from uncanny.analyzers.perplexity import PerplexityAnalyzer  # noqa: F401

    __all__.append("PerplexityAnalyzer")
except ImportError:
    pass
