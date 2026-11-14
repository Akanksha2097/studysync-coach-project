"""Run the reproducible StudySync Coach reliability checks."""

from coach.rag import answer_question


CASES = [
    ("How should I plan a focus session?", "Focus blocks", True),
    ("How can I remember what I read?", "Active recall", True),
    ("Which study spot should I choose?", "Choosing a study spot", True),
    ("What is the weather tomorrow?", "insufficient_context", False),
    ("", "empty_input", False),
    ("x" * 501, "input_too_long", False),
]


def main() -> int:
    passed = 0
    print("StudySync Coach reliability evaluation")
    for question, expected, should_retrieve in CASES:
        response = answer_question(question)
        if should_retrieve:
            ok = expected in response.sources and response.confidence > 0
        else:
            ok = response.guardrail == expected
        passed += int(ok)
        label = question[:42] or "<empty>"
        print(f"{'PASS' if ok else 'FAIL'} | {label!r} | sources={list(response.sources)} | guardrail={response.guardrail}")
    print(f"Result: {passed}/{len(CASES)} checks passed")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
