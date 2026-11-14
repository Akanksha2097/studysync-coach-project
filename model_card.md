# StudySync Coach model card

## System summary

StudySync Coach is a local retrieval-augmented study planner built on the original
StudySync project. It retrieves relevant passages from a committed study guide and
uses those passages to produce a short recommendation with source titles and a
confidence estimate.

## Intended use

The system supports study planning, focus-block selection, active-recall reminders,
spaced-review planning, and study-spot decisions. It is educational support and
does not replace an instructor, counselor, clinician, or academic-integrity policy.

## Limitations and bias

The knowledge base is small, English-only, and written around common individual
study habits. It may under-serve students with accessibility needs, different
learning contexts, or schedules that do not match the examples. Retrieval confidence
measures term overlap, not truth or student success. A human should decide whether a
recommendation fits their actual situation.

## Misuse prevention

The input length limit, insufficient-context response, visible sources, and scope
guardrail reduce confident answers outside the study-planning domain. The application
does not claim medical or mental-health expertise and does not provide answers that
would facilitate academic dishonesty.

## Reliability findings

The evaluation harness checks retrieval for three supported topics, a missing-context
question, empty input, and an overlong input. The latest committed run is recorded in
`evidence/evaluation.txt` and the same checks are available through `python evaluate.py`.

## AI collaboration reflection

I used AI to help turn the earlier StudySync tabs into a cohesive applied system and
to suggest a retrieval module with source citations. I accepted the suggestion to
keep the knowledge base local because it makes grading reproducible and keeps the
system usable without an API key.

I revised a suggestion to add a multi-agent orchestration layer. That would have
added complexity without improving this small study-planning task, so I kept one
transparent retriever and one response generator. The choice made the evidence path
easier to inspect and test.

## What surprised me

The system can produce a fluent-looking response even when retrieval finds no useful
passage, which is why the insufficient-context guardrail matters more than a polished
template. Small vocabulary changes also lower term-overlap confidence, so confidence
should be treated as a debugging signal rather than a guarantee.
