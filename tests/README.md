# Test cases

Automated tests are not shipped in this repository. The cases below describe checks that match the policies in `policy.md` and the schemas in `src/math_tutor/schemas.py`. They can be run as unit tests against the Pydantic models and `LearnerProfile.record`, or as manual Streamlit sessions.

## T1. Canonical topics only (P1)

- **Input:** `LessonPlan` / `Diagnosis` JSON with `topic` or `recommended_topic` set to `calculus`, `Algebra II`, or another unknown label.
- **Expected:** Validation raises; the UI does not show a new topic category and does not write a new mastery key.

## T2. Topic aliases (P1)

- **Input:** `topic` = `prealgebra`, `integers`, or `geometry`.
- **Expected:** Canonicalized to `pre-algebra (integers)` or `geometry (area, perimeter, angles)`, respectively.

## T3. Difficulty bounds (P2)

- **Input:** `difficulty` = `0`, `6`, or a non-integer that cannot be parsed.
- **Expected:** Parsed values are clamped to 1–5 when `_as_int` succeeds; invalid payloads fail `LessonPlan` / `Diagnosis` validation.

## T4. Four choices and unique correct answer (P3)

- **Input:** Question JSON with three choices, or with `correct_answer` that matches zero or two choices.
- **Expected:** `MultipleChoiceQuestion` validation fails. A valid four-choice item with a unique matching `correct_answer` is accepted, and `correct_index` is set from that match.

## T5. Choice shuffle (P3)

- **Input:** A valid generated question whose original `correct_index` is `0`.
- **Expected:** After `generate_question`, `choices` may be in a new order and `correct_index` still points at the same `correct_answer` text.

## T6. Correct attempt clears misconception field (P7)

- **Input:** `LearnerProfile.record` with `user_index` equal to `correct_index` and a diagnosis that still includes a misconception string.
- **Expected:** Stored attempt has `misconception` = `null`; `known_misconceptions` is not appended.

## T7. Incorrect attempt records misconception (P7, P10)

- **Input:** Wrong `user_index`, diagnosis with a non-empty misconception and `recommended_difficulty` ≤ current difficulty.
- **Expected:** History row is incorrect; misconception is appended if new; `current_difficulty` does not increase.

## T8. Diagnostic override of the answer key (P4)

- **Input:** Generator key says index 0 is correct; diagnostic returns `validated_correct_index` = `2`; learner picked `2`.
- **Expected:** After `diagnose_answer`, the learner is marked correct and the displayed key follows index 2.

## T9. No agent tools (tools.md)

- **Input:** Inspect `curriculum_agent`, `question_agent`, and `diagnostic_agent`.
- **Expected:** No CrewAI tools attached; `allow_delegation` is false (P5).

## T10. Local persistence and reset (P6, P9)

- **Input:** Complete one round, then click **Reset learner data**.
- **Expected:** After the round, `data/learner.json` contains the attempt. After reset, mastery returns to defaults, history is empty, and misconceptions are cleared. LLM calls use `ollama/{OLLAMA_MODEL}` at `OLLAMA_BASE_URL`.

## T11. Mastery-based difficulty and progression (P11)

- **Input:** Plan for a topic with mastery scores `0.0`, `0.2`, `0.4`, `0.6`, `0.8`, and `1.0`.
- **Expected:** Difficulties are respectively `1`, `2`, `3`, `4`, `5`, and `5`, independent of the model's recommended difficulty.
- **Input:** The current topic has mastery `1.0`, or an attempt raises its mastery to `1.0`.
- **Expected:** The curriculum chooses the following canonical topic in `TOPICS`; after the last topic, it wraps to the first.
