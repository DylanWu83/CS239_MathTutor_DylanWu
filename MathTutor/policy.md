P1. Curriculum and diagnostic outputs must use exactly one canonical topic name from this list: whole-number arithmetic; fractions and decimals; percentages and ratios; pre-algebra (integers); linear equations; geometry (area, perimeter, angles); word problems. Agents must not invent a topic, change capitalization, or use a synonym. If a model returns an unknown topic, the application rejects the output. Currently enforced by `canonical_topic` validators on lesson plans, questions, diagnoses, and the learner profile.

P2. Difficulty must be an integer in the closed range 1–5. Values outside that range are invalid. Currently enforced when parsing agent JSON and when writing `current_difficulty` on the learner profile.

P11. Difficulty is determined by the selected topic's mastery: mastery in `[0.0, 0.2)` maps to difficulty 1, `[0.2, 0.4)` to 2, `[0.4, 0.6)` to 3, `[0.6, 0.8)` to 4, and `[0.8, 1.0]` to 5. When the current topic reaches 1.0 mastery, the curriculum advances to the following topic in the canonical topic list, wrapping to the first topic after the last.

P3. Every generated item must have exactly four choices and a `correct_answer` that matches exactly one of those choices. After generation, the application shuffles the choice order and recomputes `correct_index` from `correct_answer` so the correct option is not tied to a fixed letter. Currently enforced.

P4. The diagnostic agent must independently solve the item rather than trusting the generator’s answer key. If the key conflicts with the calculation, the diagnosis must note the inconsistency and grade the learner against the mathematically correct choice (`validated_correct_index`). Currently intended in the diagnostic prompt and applied in `diagnose_answer` when a valid index is returned.

P5. Agents must not delegate tasks to other agents. Coordination is centralized in the Streamlit app, which runs the curriculum, question, and diagnostic crews one after another. Currently enforced with `allow_delegation=False` on each agent.

P6. Learner history, mastery scores, and misconceptions may be stored only in the local file `data/learner.json`. LLM calls must go to the configured local Ollama endpoint, not to a hosted model provider. CrewAI telemetry should remain disabled. Currently enforced by `local_llm()`, `.env` defaults, and local profile I/O.

P7. If the learner’s choice is correct, `misconception` must be null and must not be appended to `known_misconceptions`. Misconceptions are recorded only for incorrect attempts. Currently enforced in `LearnerProfile.record` and required in the diagnostic task prompt.

P8. The question stem must not leak the correct answer or otherwise identify which choice is right. Numbers in items should be original and computable by hand. Currently intended in the question-generator prompt; not checked programmatically.

P9. Learner profile data may be erased only when the user explicitly clicks **Reset learner data**. Agents cannot reset or overwrite history except by appending a diagnosed attempt. Currently enforced in the UI.

P10. After an incorrect answer, the diagnostic may recommend staying on the missed skill unless it names another canonical topic. Difficulty recommendations from the diagnostic do not override the mastery-based difficulty rule in P11.
