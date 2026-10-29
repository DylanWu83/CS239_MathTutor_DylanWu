import random

from crewai import Crew, Process, Task

from math_tutor.agents import curriculum_agent, diagnostic_agent, question_agent
from math_tutor.config import TOPICS, difficulty_for_mastery, next_topic
from math_tutor.jsonutil import parse_model
from math_tutor.learner import LearnerProfile
from math_tutor.schemas import Diagnosis, LessonPlan, MultipleChoiceQuestion


def plan_next_item(profile: LearnerProfile) -> LessonPlan:
    planner = curriculum_agent()
    task = Task(
        description=(
            "Using this learner profile, pick the next practice item.\n\n"
            f"{profile.summary_for_agents()}\n\n"
            f"Choose topic using exactly one of these canonical names: {TOPICS}.\n"
            "Do not create a new topic, alter capitalization, or use a synonym.\n"
            "Difficulty is determined by the selected topic's mastery: "
            "0.0–<0.2 is 1, 0.2–<0.4 is 2, 0.4–<0.6 is 3, "
            "0.6–<0.8 is 4, and 0.8–1.0 is 5. If the current topic has "
            "mastery 1.0, choose the following topic in the allowed list.\n"
            "Return ONLY JSON with keys: topic, difficulty (int 1-5), skill, "
            "rationale, target_misconception (string or null)."
        ),
        expected_output="A JSON object matching the LessonPlan schema.",
        agent=planner,
    )
    crew = Crew(agents=[planner], tasks=[task], output_log_file="traces.txt", process=Process.sequential, verbose=True)
    result = crew.kickoff()
    plan = parse_model(result, LessonPlan)
    if profile.topic_mastery.get(profile.current_topic, 0.4) >= 1.0:
        plan.topic = next_topic(profile.current_topic)
    plan.difficulty = difficulty_for_mastery(
        profile.topic_mastery.get(plan.topic, 0.4)
    )
    return plan  # type: ignore[return-value]


def generate_question(plan: LessonPlan) -> MultipleChoiceQuestion:
    writer = question_agent()
    target = plan.target_misconception or "none specified"
    task = Task(
        description=(
            "Create one multiple-choice math question that matches this plan:\n"
            f"- topic: {plan.topic}\n"
            f"- difficulty: {plan.difficulty}\n"
            f"- skill: {plan.skill}\n"
            f"- rationale: {plan.rationale}\n"
            f"- misconception to probe: {target}\n\n"
            "Requirements:\n"
            "- exactly 4 choices in the choices array\n"
            "- solve the math problem before writing the choices\n"
            "- correct_answer must be the exact text of the one mathematically correct choice\n"
            "- correct_index must be the zero-based index of correct_answer in choices\n"
            "- recompute the answer and check that correct_answer, correct_index, and "
            "explanation all agree\n"
            "- use plain-text math notation; do not use LaTeX or backslash commands "
            "inside JSON strings\n"
            "- distractor_notes has a short note for each wrong choice\n"
            "- do not number the stem\n"
            "Return ONLY JSON with keys: topic, difficulty, skill, stem, choices, "
            "correct_answer, correct_index, explanation, distractor_notes."
        ),
        expected_output="A JSON object matching the MultipleChoiceQuestion schema.",
        agent=writer,
    )
    crew = Crew(agents=[writer], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    question = parse_model(result, MultipleChoiceQuestion)

    choices = question.choices.copy()
    random.SystemRandom().shuffle(choices)
    question.choices = choices
    question.correct_index = next(
        index
        for index, choice in enumerate(choices)
        if choice.strip().casefold() == question.correct_answer.strip().casefold()
    )
    return question  # type: ignore[return-value]


def diagnose_answer(
    profile: LearnerProfile,
    question: MultipleChoiceQuestion,
    user_index: int,
) -> Diagnosis:
    analyst = diagnostic_agent()
    letters = "ABCD"
    chosen = question.choices[user_index]
    correct = question.choices[question.correct_index]
    task = Task(
        description=(
            "Diagnose this attempt.\n\n"
            f"Learner profile:\n{profile.summary_for_agents()}\n\n"
            f"Question: {question.stem}\n"
            f"Choices: {list(enumerate(question.choices))}\n"
            f"Correct choice: {letters[question.correct_index]}. {correct}\n"
            f"Learner chose: {letters[user_index]}. {chosen}\n"
            f"Author explanation: {question.explanation}\n"
            f"Distractor notes: {question.distractor_notes}\n\n"
            f"Use exactly one canonical topic from this list when recommending a topic: "
            f"{TOPICS}. If no topic change is needed, recommend {question.topic!r}.\n"
            "Independently calculate the correct answer rather than blindly trusting the "
            "answer key. If the key conflicts with the calculation, explain the conflict "
            "and return the index of the mathematically correct choice. If the key is "
            "correct, return its index unchanged.\n"
            "If the learner is correct, misconception must be null. "
            "recommended_difficulty must be an integer 1-5. "
            "If they missed an easy item, keep or lower difficulty. "
            "If they got a hard item right, consider raising it. "
            "Return ONLY JSON with keys: is_correct, misconception, explanation, "
            "recommended_topic, recommended_difficulty, mastery_note, and "
            "validated_correct_index (int 0-3), the index of the mathematically "
            "correct choice after your independent check."
        ),
        expected_output="A JSON object matching the Diagnosis schema.",
        agent=analyst,
    )
    crew = Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    diagnosis = parse_model(result, Diagnosis)
    question.correct_index = diagnosis.validated_correct_index
    question.correct_answer = question.choices[question.correct_index]
    diagnosis.is_correct = user_index == question.correct_index
    return diagnosis  # type: ignore[return-value]
