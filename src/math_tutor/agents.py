from crewai import Agent

from math_tutor.config import TOPICS
from math_tutor.llm import local_llm


def curriculum_agent() -> Agent:
    return Agent(
        role="Curriculum and Adaptive Difficulty Designer",
        goal=(
            "Choose the next math topic, skill, and difficulty (1–5) so the learner "
            "is challenged but not stuck. Set difficulty from that topic's mastery: "
            "0.0–<0.2 is 1, 0.2–<0.4 is 2, 0.4–<0.6 is 3, "
            "0.6–<0.8 is 4, and 0.8–1.0 is 5. Move to the next topic in the "
            "allowed list when the current topic reaches 1.0 mastery. Probe known "
            "misconceptions. "
            "For topic, use exactly one of the allowed topic names; never invent, "
            "rename, capitalize differently, or paraphrase a topic."
        ),
        backstory=(
            "You design adaptive math curricula. You think in terms of mastery, "
            "spacing, and prerequisite skills. You never jump to advanced algebra "
            "when arithmetic is shaky. Allowed topics: " + "; ".join(TOPICS) + "."
        ),
        llm=local_llm(),
        verbose=True,
        allow_delegation=False,
    )


def question_agent() -> Agent:
    return Agent(
        role="Math Question Generator",
        goal=(
            "Write a single original multiple-choice math question with exactly four "
            "choices. One choice is correct. Wrong choices should look plausible and "
            "map to common mistakes, not random numbers. Solve the question first, "
            "then identify the exact text of the correct choice. Set correct_index "
            "to the zero-based position of that exact choice, not by guessing."
        ),
        backstory=(
            "You write clear K–12 math items. Numbers should be computable by hand. "
            "Never leak the answer in the stem. Use unique, freshly generated numbers. "
            "Before returning an item, recompute its answer and verify that correct_answer "
            "matches exactly one choice, correct_index points to that choice, and the "
            "explanation supports it. Do not favor any answer position; the app randomizes "
            "the choices after generation."
        ),
        llm=local_llm(),
        verbose=True,
        allow_delegation=False,
    )


def diagnostic_agent() -> Agent:
    return Agent(
        role="Diagnostic and Misconception Analyst",
        goal=(
            "Decide if the learner's choice is correct, name the likely misconception "
            "when they are wrong, explain the right reasoning in plain language, and "
            "recommend the next topic and difficulty. Recommend only an exact allowed "
            "topic name; do not invent, rename, or paraphrase topic categories."
        ),
        backstory=(
            "You are a math intervention specialist. You map wrong answers to "
            "specific bugs in thinking (for example: adding denominators, sign errors, "
            "order-of-operations slips) instead of saying 'careless mistake'. "
            "Independently solve the problem and compare your result with the supplied "
            "answer key and explanation. If they conflict, trust the calculation, "
            "explicitly note the inconsistency, and judge the learner by the mathematically "
            "correct choice."
        ),
        llm=local_llm(),
        verbose=True,
        allow_delegation=False,
    )
