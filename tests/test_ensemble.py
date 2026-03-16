from uncanny.ensemble import combine
from uncanny.types import AnalyzerResult, SentenceScore


def test_combine_single():
    result = combine(
        [AnalyzerResult(name="compression", score=0.8, sentence_scores=[], metadata={})],
        source="test.txt",
    )
    assert abs(result.score - 0.8) < 0.01
    assert result.source == "test.txt"
    assert result.label == "likely_ai"


def test_combine_weighted():
    results = [
        AnalyzerResult(name="compression", score=0.9, sentence_scores=[], metadata={}),
        AnalyzerResult(name="burstiness", score=0.5, sentence_scores=[], metadata={}),
    ]
    result = combine(results)
    # compression weight 0.65, burstiness dynamically weighted
    # When compression=0.9, confidence = abs(0.9-0.5)*2 = 0.8
    # burstiness weight = 0.20 * (1 - 0.8*0.6) = 0.20 * 0.52 = 0.104
    burst_w = 0.20 * (1.0 - abs(0.9 - 0.5) * 2 * 0.6)
    expected = (0.9 * 0.65 + 0.5 * burst_w) / (0.65 + burst_w)
    assert abs(result.score - expected) < 0.01


def test_labels():
    for score, expected in [
        (0.9, "ai_generated"),
        (0.7, "likely_ai"),
        (0.5, "mixed"),
        (0.3, "likely_human"),
        (0.1, "human"),
    ]:
        result = combine(
            [AnalyzerResult(name="test", score=score, sentence_scores=[], metadata={})]
        )
        assert result.label == expected


def test_sentence_merging():
    ss = SentenceScore("Hello world.", 0.8, 0, 12)
    results = [
        AnalyzerResult(name="compression", score=0.8, sentence_scores=[ss], metadata={}),
        AnalyzerResult(
            name="burstiness",
            score=0.6,
            sentence_scores=[SentenceScore("Hello world.", 0.4, 0, 12)],
            metadata={},
        ),
    ]
    result = combine(results)
    assert len(result.sentences) == 1
    # Weighted average of sentence scores
    assert 0.4 < result.sentences[0].score < 0.8
