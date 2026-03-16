from uncanny.analyzers.compression import CompressionAnalyzer


def test_ai_text_scores_high():
    ai_text = (
        "The implementation of this feature requires careful consideration of "
        "several architectural patterns to ensure maintainability and scalability. "
        "By leveraging existing infrastructure components, we can achieve seamless "
        "integration while minimizing technical debt. This approach provides a robust "
        "and comprehensive solution that addresses the identified requirements."
    )
    result = CompressionAnalyzer().analyze(ai_text)
    assert result.score > 0.5, f"Expected AI text to score > 0.5, got {result.score}"


def test_human_text_scores_low():
    human_text = (
        "So I tried like three different approaches before landing on this one. "
        "The weird part was the timeout — still not 100% sure why it happens on "
        "cold starts but whatever, the retry logic handles it. Honestly the code "
        "is kind of ugly in that section, I'll clean it up later maybe."
    )
    result = CompressionAnalyzer().analyze(human_text)
    assert result.score < 0.6, f"Expected human text to score < 0.6, got {result.score}"


def test_has_sentence_scores():
    text = "First sentence here. Second sentence there. Third one too."
    result = CompressionAnalyzer().analyze(text)
    assert len(result.sentence_scores) > 0


def test_scores_in_range():
    text = "Some text to analyze. Another sentence follows."
    result = CompressionAnalyzer().analyze(text)
    assert 0.0 <= result.score <= 1.0
    for ss in result.sentence_scores:
        assert 0.0 <= ss.score <= 1.0
