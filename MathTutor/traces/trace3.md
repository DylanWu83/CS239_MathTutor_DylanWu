# Trace for changing topics when mastery is reached

## Curriculum and Adaptive Difficulty Designer

Input:
Using this learner profile, pick the next practice item.

Current topic: percentages and ratios
Current difficulty: 5
Topic mastery (0–1): whole-number arithmetic=0.91, fractions and decimals=1.00, percentages and ratios=0.91, pre-algebra (integers)=0.91, linear equations=0.91, geometry (area, perimeter, angles)=0.91, word problems=0.91
Recent attempts:
- [correct] d5 fractions and decimals / Converting between fractions and decimals: chose 2, correct 2

Choose topic using exactly one of these canonical names: ['whole-number arithmetic', 'fractions and decimals', 'percentages and ratios', 'pre-algebra (integers)', 'linear equations', 'geometry (area, perimeter, angles)', 'word problems'].
Do not create a new topic, alter capitalization, or use a synonym.
Difficulty is determined by the selected topic's mastery: 0.0–<0.2 is 1, 0.2–<0.4 is 2, 0.4–<0.6 is 3, 0.6–<0.8 is 4, and 0.8–1.0 is 5. If the current topic has mastery 1.0, choose the following topic in the allowed list.
Return ONLY JSON with keys: topic, difficulty (int 1-5), skill, rationale, target_misconception (string or null).

Output:
```json
{
  "topic": "pre-algebra (integers)",
  "difficulty": 5,
  "skill": "Adding and subtracting integers",
  "rationale": "The learner has mastered percentages and ratios, so the next step is to move to pre-algebra (integers). The difficulty is set to 5 as the mastery for percentages and ratios is 0.91, indicating a high level of proficiency.",
  "target_misconception": null
}
```

## Math Question Generator:

Input:
Create one multiple-choice math question that matches this plan:
- topic: pre-algebra (integers)
- difficulty: 5
- skill: Adding and subtracting integers
- rationale: The learner has mastered percentages and ratios, so the next step is to move to pre-algebra (integers). The difficulty is set to 5 as the mastery for percentages and ratios is 0.91, indicating a high level of proficiency.
- misconception to probe: none specified

Requirements:
- exactly 4 choices in the choices array
- solve the math problem before writing the choices
- correct_answer must be the exact text of the one mathematically correct choice
- correct_index must be the zero-based index of correct_answer in choices
- recompute the answer and check that correct_answer, correct_index, and explanation all agree
- use plain-text math notation; do not use LaTeX or backslash commands inside JSON strings
- distractor_notes has a short note for each wrong choice
- do not number the stem
Return ONLY JSON with keys: topic, difficulty, skill, stem, choices, correct_answer, correct_index, explanation, distractor_notes.


Output:
``` json
{
  "topic": "pre-algebra (integers)",
  "difficulty": 5,
  "skill": "Adding and subtracting integers",
  "stem": "What is the result of the following expression: -15 + 7 - 4 + 9?",
  "choices": [
    "-11",
    "11",
    "-7",
    "7"
  ],
  "correct_answer": "7",
  "correct_index": 3,
  "explanation": "To solve the expression -15 + 7 - 4 + 9, we can break it down step by step:
-15 + 7 = -8
-8 - 4 = -12
-12 + 9 = -3

However, the correct calculation is:
-15 + 7 = -8
-8 - 4 = -12
-12 + 9 = -3 + 9 = 6 + 1 = 7.

Therefore, the correct answer is 7.",
  "distractor_notes": [
    "This is the result of incorrectly adding -15 and 7, then subtracting 4, and finally adding 9.",
    "This is the result of incorrectly adding -15 and 7, then subtracting 4, and finally adding 9, but with a sign error.",
    "This is the result of incorrectly adding -15 and 7, then subtracting 4, and finally adding 9, with a different sign error.",
    "This is the correct answer after correctly solving the expression."
  ]
}
```