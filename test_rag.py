from coach.rag import answer_question


def test_answer_uses_retrieved_focus_evidence():
    response = answer_question("How should I plan a focus session?")
    assert "Focus blocks" in response.sources
    assert "concrete outcome" in response.answer
    assert response.confidence > 0


def test_answer_has_guardrails_for_missing_context_and_bad_input():
    assert answer_question("What is the weather tomorrow?").guardrail == "insufficient_context"
    assert answer_question("").guardrail == "empty_input"
    assert answer_question("x" * 501).guardrail == "input_too_long"
