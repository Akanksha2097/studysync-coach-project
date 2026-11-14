"""Offline retrieval-augmented study coaching for the StudySync app.

The retriever uses a small local knowledge base and transparent term overlap.
The response generator receives the retrieved passages and cites their section
names, so the application can show exactly what evidence shaped each answer.
"""

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


MAX_QUESTION_LENGTH = 500
STOP_WORDS = {"a", "an", "and", "are", "be", "for", "how", "i", "is", "it", "my", "of", "or", "should", "the", "to", "what", "with"}
SYNONYMS = {"remember": "recall", "remembering": "recall", "memorize": "recall", "read": "recall", "reading": "recall", "learn": "recall"}


@dataclass(frozen=True)
class KnowledgeChunk:
    title: str
    text: str


@dataclass(frozen=True)
class CoachResponse:
    answer: str
    sources: tuple[str, ...]
    confidence: float
    guardrail: str | None = None


def _terms(text: str) -> set[str]:
    words = (SYNONYMS.get(word, word) for word in re.findall(r"[a-z0-9]+", text.lower()))
    return {word for word in words if word not in STOP_WORDS and len(word) > 2}


def load_knowledge_base(path: str | Path | None = None) -> list[KnowledgeChunk]:
    source = Path(path) if path else Path(__file__).with_name("knowledge_base.md")
    chunks: list[KnowledgeChunk] = []
    title: str | None = None
    lines: list[str] = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if title and lines:
                chunks.append(KnowledgeChunk(title, " ".join(lines).strip()))
            title, lines = line[3:].strip(), []
        elif title and line.strip():
            lines.append(line.strip())
    if title and lines:
        chunks.append(KnowledgeChunk(title, " ".join(lines).strip()))
    return chunks


def retrieve(question: str, chunks: Iterable[KnowledgeChunk], k: int = 2) -> list[KnowledgeChunk]:
    query_terms = _terms(question)
    scored = []
    for chunk in chunks:
        if chunk.title == "Guardrails" and "guardrail" not in query_terms:
            continue
        overlap = query_terms & _terms(f"{chunk.title} {chunk.text}")
        score = len(overlap) + (2 if query_terms & _terms(chunk.title) else 0)
        if score:
            scored.append((score, chunk.title, chunk))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [chunk for _, _, chunk in scored[:k]]


def _topic_answer(question: str, sources: list[KnowledgeChunk]) -> str:
    lower = question.lower()
    evidence = " ".join(chunk.text for chunk in sources)
    if any(word in lower for word in ("spot", "library", "quiet", "noise", "seat", "distance")):
        return "Choose the highest-ranked spot that satisfies your noise, distance, and seat needs. " + evidence.split(".")[0] + "."
    if any(word in lower for word in ("review", "remember", "memorize", "exam", "learn")):
        return "Use active recall, then schedule a short spaced review. " + evidence.split(".")[0] + "."
    if any(word in lower for word in ("focus", "distract", "session", "study", "plan")):
        return "Start with one concrete outcome, run a focused block, and take a short break. " + evidence.split(".")[0] + "."
    return "I can help plan a focus block, choose a study spot, or schedule review. " + evidence.split(".")[0] + "."


def answer_question(question: str, chunks: Iterable[KnowledgeChunk] | None = None) -> CoachResponse:
    cleaned = question.strip()
    if not cleaned:
        return CoachResponse("Tell me what you want to study or plan.", (), 0.0, "empty_input")
    if len(cleaned) > MAX_QUESTION_LENGTH:
        return CoachResponse("Please shorten your question to 500 characters or fewer.", (), 0.0, "input_too_long")
    knowledge = list(chunks) if chunks is not None else load_knowledge_base()
    sources = retrieve(cleaned, knowledge)
    if not sources:
        return CoachResponse("I do not have enough evidence in my study guide to answer that. Try asking about focus blocks, active recall, spaced review, or study spots.", (), 0.1, "insufficient_context")
    confidence = min(0.95, 0.45 + 0.15 * len(_terms(cleaned) & _terms(" ".join(chunk.text for chunk in sources))))
    return CoachResponse(_topic_answer(cleaned, sources), tuple(chunk.title for chunk in sources), round(confidence, 2))
