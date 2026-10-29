from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st

from math_tutor.config import DIFFICULTY_LABELS, OLLAMA_MODEL
from math_tutor.crews import diagnose_answer, generate_question, plan_next_item
from math_tutor.learner import LearnerProfile
from math_tutor.schemas import Diagnosis, MultipleChoiceQuestion

st.set_page_config(page_title="Adaptive Math Tutor", page_icon="∫", layout="centered")


def _profile() -> LearnerProfile:
    if "profile" not in st.session_state:
        st.session_state.profile = LearnerProfile.load()
    return st.session_state.profile


def _reset_item() -> None:
    st.session_state.pop("plan", None)
    st.session_state.pop("question", None)
    st.session_state.pop("diagnosis", None)
    st.session_state.pop("picked", None)


def main() -> None:
    profile = _profile()
    st.title("Adaptive Math Tutor")
    st.caption(f"CrewAI agents on local Ollama · model `{OLLAMA_MODEL}`")

    with st.sidebar:
        st.subheader("Learner")
        st.write(f"**Focus:** {profile.current_topic}")
        st.write(
            f"**Difficulty:** {profile.current_difficulty} "
            f"({DIFFICULTY_LABELS[profile.current_difficulty]})"
        )
        st.write(f"**Questions answered:** {len(profile.history)}")
        if profile.history:
            correct = sum(1 for a in profile.history if a.is_correct)
            st.write(f"**Accuracy:** {correct / len(profile.history):.0%}")
        st.markdown("**Mastery**")
        for topic, score in profile.topic_mastery.items():
            st.progress(score, text=f"{topic}: {score:.0%}")
        if profile.known_misconceptions:
            st.markdown("**Misconceptions**")
            for item in profile.known_misconceptions[-5:]:
                st.write(f"- {item}")
        if st.button("Reset learner data"):
            st.session_state.profile = LearnerProfile()
            st.session_state.profile.save()
            _reset_item()
            st.rerun()

    question: MultipleChoiceQuestion | None = st.session_state.get("question")
    diagnosis: Diagnosis | None = st.session_state.get("diagnosis")

    if diagnosis and question:
        _render_feedback(profile, question, diagnosis)
        return

    if question is None:
        st.write(
            "Click 'Next question' to get your next question. "
            "The curriculum agent will choose a skill based on your mastery, "
            "and the question generator will write a new multiple-choice question."
        )
        if st.button("Next question", type="primary"):
            try:
                with st.spinner("Curriculum agent is choosing the next skill…"):
                    plan = plan_next_item(profile)
                    st.session_state.plan = plan
                with st.spinner("Question generator is writing an item…"):
                    st.session_state.question = generate_question(plan)
            except Exception as exc:
                st.error(f"The local agents could not finish this round: {exc}")
                st.info("Ollama must be running. Click Next question to try again.")
                return
            st.rerun()
        return

    plan = st.session_state.get("plan")
    if plan:
        st.info(f"**Why this question:** {plan.rationale}")

    st.markdown(f"**Topic:** {question.topic} · **Skill:** {question.skill}")
    st.markdown(f"### {question.stem}")

    labels = [f"{letter}. {choice}" for letter, choice in zip("ABCD", question.choices)]
    picked = st.radio("Your answer", options=list(range(4)), format_func=lambda i: labels[i])

    if st.button("Submit", type="primary"):
        try:
            with st.spinner("Diagnostic agent is reviewing your answer…"):
                result = diagnose_answer(profile, question, int(picked))
        except Exception as exc:
            st.error(f"The diagnostic agent could not finish: {exc}")
            return
        profile.record(question.model_dump(), int(picked), result.model_dump())
        profile.save()
        st.session_state.diagnosis = result
        st.session_state.picked = int(picked)
        st.rerun()


def _render_feedback(
    profile: LearnerProfile,
    question: MultipleChoiceQuestion,
    diagnosis: Diagnosis,
) -> None:
    picked = st.session_state.get("picked", 0)
    if diagnosis.is_correct:
        st.success("Correct")
    else:
        st.error("Not quite")
        st.write(
            f"You chose **{question.choices[picked]}**. "
            f"The correct answer is **{question.choices[question.correct_index]}**."
        )
    st.markdown("**Explanation**")
    st.write(diagnosis.explanation)
    if diagnosis.misconception:
        st.warning(f"Likely misconception: {diagnosis.misconception}")
    st.markdown("**Next step**")
    st.write(diagnosis.mastery_note)
    st.caption(
        f"Curriculum update → {profile.current_topic} at difficulty {profile.current_difficulty}"
    )
    if st.button("Continue", type="primary"):
        _reset_item()
        st.rerun()


if __name__ == "__main__":
    main()
