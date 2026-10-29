# Example 3: Invented topic name is rejected

This example is **hypothetical**. It shows a policy rejection, not a successful tutoring round.

## Initial inputs

- **User request:** Click **Next question**.
- **Learner profile:** existing history with low mastery on `pre-algebra (order of operations, integers)`.
- **Agents that receive input:** Curriculum and Adaptive Difficulty Designer.

## Trajectory

1. **Application.** Calls `plan_next_item(profile)`.
2. **Curriculum and Adaptive Difficulty Designer.** Returns JSON with `"topic": "Order of Operations"` (a paraphrase, not a canonical name) and `"difficulty": 3`.
3. **Application.** `LessonPlan` validation runs `canonical_topic("Order of Operations")`. The alias map does not accept this string as a distinct topic; depending on normalization it may map to `pre-algebra (order of operations, integers)` or raise `ValueError`.
4. If the string does not canonicalize, `parse_model` fails and the UI shows an error: the local agents could not finish this round. The question generator is **not** started. The learner profile is **not** updated.
5. If the string does canonicalize (for example a known alias such as `prealgebra`), the plan is accepted as `pre-algebra (order of operations, integers)` and the question generator proceeds. A truly unknown label such as `"calculus"` raises and aborts the round.

## Policy connection

P1, P5.

## Expected outcome

Unknown or paraphrased topics never appear as a new category in `topic_mastery`. Either the name is mapped onto an existing canonical topic, or the round fails closed with no new question and no profile write. The curriculum agent cannot delegate to the question generator to “fix” the topic name.
