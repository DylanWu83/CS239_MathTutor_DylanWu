# Adaptive Math Tutor

The Adaptive Math Tutor is a local, workflow-oriented multi-agent application for K–12 math practice. Three CrewAI agents, coordinated by a Streamlit UI, choose the next skill, write a multiple-choice item, and diagnose the learner’s answer. A persisted learner profile (`data/learner.json`) carries mastery, difficulty, history, and known misconceptions across sessions.

The application uses **centralized coordination** and **fixed sequential interactions**: the UI starts one agent at a time. Agents do not call each other or delegate. Inference runs on a **local Ollama** model (no hosted LLM API key).

## Purpose

Help a learner practice math at an appropriate difficulty while surfacing specific misconceptions (for example, adding denominators) instead of generic “careless mistake” feedback.

## Supported tasks

- **Start or continue a session.** Load the local learner profile (or create a default profile) and show current topic, difficulty, mastery, and known misconceptions.
- **Request the next practice item.** The curriculum agent selects a canonical topic, skill, difficulty (1–5), and optional target misconception. The question generator then writes one four-choice item for that plan.
- **Submit an answer.** The learner picks A–D. The diagnostic agent checks the work, names a misconception when the answer is wrong, explains the correct reasoning, and recommends the next topic and difficulty.
- **Update the learner model.** After diagnosis, the app records the attempt, adjusts topic mastery, and saves the profile.
- **Reset learner data.** The user may wipe the profile from the sidebar and start over.
