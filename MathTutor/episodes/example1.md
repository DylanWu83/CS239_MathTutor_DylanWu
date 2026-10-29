# Example 1: New learner requests the first question

This example is **hypothetical**. It follows the implemented workflow for a learner with an empty history.

## Initial inputs

- **User request:** Click **Next question** in the Streamlit app.
- **Learner profile:** new profile — all topic mastery scores `0.4`, `current_topic` = `whole-number arithmetic`, `current_difficulty` = `2`, empty history, no known misconceptions.
- **Agents that receive input:** Curriculum and Adaptive Difficulty Designer (profile summary), then Math Question Generator (the resulting lesson plan). The diagnostic agent is not invoked until the learner submits an answer.

## Trajectory

1. **Application (Streamlit).** Loads `data/learner.json` and passes `profile.summary_for_agents()` into `plan_next_item`.
2. **Curriculum and Adaptive Difficulty Designer.** Reads that the learner is new and should start with introductory whole-number arithmetic at difficulty 2. Returns JSON such as:
   - `topic`: `whole-number arithmetic`
   - `difficulty`: `2`
   - `skill`: `two-digit addition without regrouping`
   - `rationale`: `New learner; check number sense before moving on.`
   - `target_misconception`: `null`
3. **Application.** Validates the plan against the expected output and configured learning constraints (P5). Only an accepted plan is passed to `generate_question(plan)`.
4. **Math Question Generator.** Writes a four-choice item, for example stem `What is 34 + 25?` with choices `59`, `51`, `69`, `58`, `correct_answer` `59`, and distractor notes for place-value slips.
5. **Application.** Shuffles the four choices, recomputes `correct_index` from `correct_answer`, and displays the stem and choices A–D. Shows the plan rationale as “Why this question.”

## Policy connection

P1, P2, P3, P4, P5, P6.

## Expected outcome

The learner sees one original multiple-choice item on whole-number arithmetic at difficulty 2. No diagnosis is produced yet. The profile remains unchanged until the application processes a submitted answer. The curriculum agent proposes a plan, the generator receives only that plan, and neither agent delegates or accesses learner storage.
