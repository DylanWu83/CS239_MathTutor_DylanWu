# Example 2: Incorrect fraction answer records a misconception

This example is **hypothetical**. It illustrates a full round after the learner already has some history on fractions.

## Initial inputs

- **User request:** Submit choice **C** on the displayed item.
- **Question on screen (after shuffle):**
  - Topic: `fractions and decimals`
  - Skill: `adding fractions with unlike denominators`
  - Stem: `What is 1/2 + 1/3?`
  - Choices: `A. 2/5` · `B. 5/6` · `C. 2/6` · `D. 1/5`
  - `correct_answer`: `5/6` (index 1 after shuffle)
- **Learner profile (excerpt):** `current_topic` = `fractions and decimals`, `current_difficulty` = `2`, no prior misconception about adding numerators and denominators separately.
- **Agents that receive input:** Diagnostic and Misconception Analyst (profile, stem, choices, author key, learner choice). Curriculum and question agents are not run on Submit.

## Trajectory

1. **Application.** Maps the radio selection to `user_index = 2` (`2/6`). Calls `diagnose_answer(profile, question, 2)`.
2. **Diagnostic and Misconception Analyst.** Independently computes `1/2 + 1/3 = 5/6`. Confirms the key. Determines the learner is incorrect. Names the misconception (adding numerators and denominators) based on the response. Recommends staying on `fractions and decimals` at difficulty `1` or `2`.
3. **Application.** Sets `question.correct_index` from `validated_correct_index`, sets `is_correct` from the learner index, then `profile.record(...)` and `profile.save()`.
4. **Application (UI).** Shows “Not quite,” the correct choice `5/6`, the explanation, a warning with the misconception, and the mastery note. Sidebar mastery for fractions decreases slightly; the misconception is listed.

## Policy connection

P1, P2, P3, P4, P5, P6, P7.

## Expected outcome

The application records the attempt as incorrect and may update the learner model under its data rules. The misconception is included because it is supported by the wrong response. The diagnostic recommendation does not directly alter the profile or override application progression rules. Agent context is limited to this attempt and the learner information needed for diagnosis.
