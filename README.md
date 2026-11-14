# StudySync Coach

StudySync Coach is an applied AI system for turning a student's study goal into a
small, evidence-backed next step. It extends the original **StudySync Tinker
Starter** from Module 1-3, which began as a Streamlit app for scoring sessions,
logging study sessions, and ranking campus study spots. The final system keeps those
features and adds a transparent retrieval-augmented coach with source citations,
confidence scoring, and input guardrails.

## What it does

The AI Study Coach retrieves relevant sections from `coach/knowledge_base.md` before
generating a recommendation. This makes the evidence path inspectable and keeps the
demo reproducible without an API key. The app also includes the original session
scorer, validated session log, recurring-date helpers, conflict detection, and
weighted study-spot ranking.

## Architecture

The system flow is documented in [diagrams/architecture.mmd](diagrams/architecture.mmd).
The student question passes through length and scope guardrails, the term-overlap
retriever selects local evidence, and the response generator returns a recommendation
with source titles and a confidence estimate. A human reviews the recommendation
before acting on it, while the evaluation harness checks supported and unsupported
inputs.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Run the reliability checks and tests:

```bash
python evaluate.py
pytest -q
```

## Reproducible execution evidence

The following examples are from the offline coach and can be reproduced with
`python -c` or through the Streamlit interface.

### Example 1: retrieved focus guidance

```text
Input: How should I plan a focus session?
Output: Start with one concrete outcome, run a focused block, and take a short break. Use a 25 to 50 minute focus block followed by a short break.
Sources: Focus blocks, Spaced review
Confidence: 0.75
```

### Example 2: retrieved learning guidance

```text
Input: How can I remember what I read?
Output: Use active recall, then schedule a short spaced review. After reviewing material, close the notes and explain the idea from memory.
Sources: Active recall, Choosing a study spot
Confidence: 0.75
```

### Example 3: missing-context guardrail

```text
Input: What is the weather tomorrow?
Output: I do not have enough evidence in my study guide to answer that. Try asking about focus blocks, active recall, spaced review, or study spots.
Guardrail: insufficient_context
Sources: none
```

The complete six-case evaluation output is saved in [evidence/evaluation.txt](evidence/evaluation.txt).

## Testing summary

The project includes unit tests for the original scoring logic, dataclass and
recurring-session behavior, conflict detection, typed CSV loading, ranked results,
retrieval, confidence, and guardrails. The evaluation harness covers three supported
topics plus missing context, empty input, and overlong input. A successful run is six
out of six evaluation checks and all project tests passing.

## Design decisions and trade-offs

The knowledge base is local Markdown so a grader can run the full system offline and
inspect the evidence. Term overlap is less capable than an embedding model, but it is
small, deterministic, easy to debug, and sufficient for this focused domain. The
response generator is intentionally short and source-aware; it does not pretend that
confidence from word overlap is the same as factual certainty.

## Original project and extension

The original StudySync project taught cross-file refactoring, Streamlit session state,
input validation, dataclasses, recurring dates, CSV parsing, weighted scoring, and
data-flow diagrams. This final extension preserves those learning goals and connects
them to a retrieval and evaluation workflow that addresses a real student planning
problem.

## Portfolio note

This project shows that I can take a small prototype, add an AI feature that changes
the main user flow, expose its evidence, and measure failure behavior. It also shows
that I can make scope and reliability decisions that keep an AI system understandable
and reproducible.
