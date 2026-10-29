# Example 3: Unsupported learning objective is rejected

This example is **hypothetical**. It shows a policy rejection, not a successful tutoring round.

## Initial inputs

- **User request:** Click **Next question**.
- **Learner profile:** existing history with low mastery on `pre-algebra (integers)`.
- **Agents that receive input:** Curriculum and Adaptive Difficulty Designer.

## Trajectory

1. **Application.** Calls `plan_next_item(profile)`.
2. **Curriculum and Adaptive Difficulty Designer.** Returns a plan for an unsupported objective such as `"calculus"`.
3. **Application.** Validates the plan against the configured learning objectives and expected output. Because the objective is not supported, the plan is rejected and the application reports that it could not prepare the next item.
4. The question generator is **not** started because it has no accepted plan. The learner profile is **not** updated.

## Policy connection

P1, P2, P3, P4, P5.

## Expected outcome

An unsupported objective does not become a new learner category or proceed to question generation. The application rejects the plan and leaves learner data unchanged. The curriculum agent cannot ask the question generator to repair or reinterpret its output.
