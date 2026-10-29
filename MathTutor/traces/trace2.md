# Trace for incorrect answer

## Math Question Generator

Input:
Create one multiple-choice math question that matches this plan:
- topic: geometry (area, perimeter, angles)
- difficulty: 5
- skill: Calculating the area of a rectangle
- rationale: The learner has mastered linear equations and all other prerequisite topics. Moving to geometry ensures a balanced curriculum and helps in applying algebraic skills in a geometric context.
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
  "topic": "geometry",
  "difficulty": 5,
  "skill": "Calculating the area of a rectangle",
  "stem": "A rectangular garden has a length of 12 meters and a width of 8 meters. What is the area of the garden?",
  "choices": [
    "64 square meters",
    "96 square meters",
    "100 square meters",
    "112 square meters"
  ],
  "correct_answer": "96 square meters",
  "correct_index": 1,
  "explanation": "The area of a rectangle is calculated by multiplying the length by the width. Here, the length is 12 meters and the width is 8 meters. Therefore, the area is 12 * 8 = 96 square meters.",
  "distractor_notes": {
    "0": "This is the area of a square with side length 8 meters, which is not the correct shape for the garden.",
    "2": "This is the area of a square with side length 10 meters, which is not the correct dimensions for the garden.",
    "3": "This is the area of a rectangle with length 14 meters and width 8 meters, which is not the correct dimensions for the garden."
  }
}
```

## Diagnostic and Misconception Analyst

Input:
Diagnose this attempt.

Learner profile:
Current topic: linear equations
Current difficulty: 5
Topic mastery (0–1): whole-number arithmetic=0.91, fractions and decimals=1.00, percentages and ratios=0.91, pre-algebra (integers)=1.00, linear equations=0.91, geometry (area, perimeter, angles)=0.91, word problems=0.91
Recent attempts:
- [correct] d5 fractions and decimals / Converting between fractions and decimals: chose 2, correct 2
- [correct] d5 pre-algebra (integers) / Understanding and applying integer operations: chose 2, correct 2

Question: A rectangular garden has a length of 12 meters and a width of 8 meters. What is the area of the garden?
Choices: [(0, '112 square meters'), (1, '64 square meters'), (2, '100 square meters'), (3, '96 square meters')]
Correct choice: D. 96 square meters
Learner chose: A. 112 square meters
Author explanation: The area of a rectangle is calculated by multiplying the length by the width. Here, the length is 12 meters and the width is 8 meters. Therefore, the area is 12 * 8 = 96 square meters.
Distractor notes: ['This is the area of a square with side length 8 meters, which is not the correct shape for the garden.', 'This is the area of a square with side length 10 meters, which is not the correct dimensions for the garden.', 'This is the area of a rectangle with length 14 meters and width 8 meters, which is not the correct dimensions for the garden.']

Use exactly one canonical topic from this list when recommending a topic: ['whole-number arithmetic', 'fractions and decimals', 'percentages and ratios', 'pre-algebra (integers)', 'linear equations', 'geometry (area, perimeter, angles)', 'word problems']. If no topic change is needed, recommend 'geometry (area, perimeter, angles)'.
Independently calculate the correct answer rather than blindly trusting the answer key. If the key conflicts with the calculation, explain the conflict and return the index of the mathematically correct choice. If the key is correct, return its index unchanged.
If the learner is correct, misconception must be null. recommended_difficulty must be an integer 1-5. If they missed an easy item, keep or lower difficulty. If they got a hard item right, consider raising it. Return ONLY JSON with keys: is_correct, misconception, explanation, recommended_topic, recommended_difficulty, mastery_note, and validated_correct_index (int 0-3), the index of the mathematically correct choice after your independent check.

Output:
{
  "is_correct": false,
  "misconception": "Incorrect formula for area",
  "explanation": "The learner used the formula for the perimeter of a rectangle (2 * (length + width)) instead of the correct formula for the area (length * width). This is a common mistake where the learner confuses the two similar formulas.",
  "recommended_topic": "geometry (area, perimeter, angles)",
  "recommended_difficulty": 5,
  "mastery_note": "The learner has a strong grasp of linear equations and related topics, but a gap in understanding the correct formula for the area of a rectangle.",
  "validated_correct_index": 3
}

## Curriculum and Adaptive Difficulty Designer

Input:
Using this learner profile, pick the next practice item.

Current topic: geometry (area, perimeter, angles)
Current difficulty: 5
Topic mastery (0–1): whole-number arithmetic=0.91, fractions and decimals=1.00, percentages and ratios=0.91, pre-algebra (integers)=1.00, linear equations=0.91, geometry (area, perimeter, angles)=0.84, word problems=0.91
Known misconceptions: Incorrect formula for area
Recent attempts:
- [correct] d5 fractions and decimals / Converting between fractions and decimals: chose 2, correct 2
- [correct] d5 pre-algebra (integers) / Understanding and applying integer operations: chose 2, correct 2
- [WRONG] d5 geometry (area, perimeter, angles) / Calculating the area of a rectangle: chose 0, correct 3 | misconception: Incorrect formula for area

Choose topic using exactly one of these canonical names: ['whole-number arithmetic', 'fractions and decimals', 'percentages and ratios', 'pre-algebra (integers)', 'linear equations', 'geometry (area, perimeter, angles)', 'word problems'].
Do not create a new topic, alter capitalization, or use a synonym.
Difficulty is determined by the selected topic's mastery: 0.0–<0.2 is 1, 0.2–<0.4 is 2, 0.4–<0.6 is 3, 0.6–<0.8 is 4, and 0.8–1.0 is 5. If the current topic has mastery 1.0, choose the following topic in the allowed list.
Return ONLY JSON with keys: topic, difficulty (int 1-5), skill, rationale, target_misconception (string or null).

Output:
```json
{
  "topic": "geometry (area, perimeter, angles)",
  "difficulty": 4,
  "skill": "Calculating the area of a rectangle using the correct formula",
  "rationale": "The learner has a 0.84 mastery in geometry, which is slightly below 0.8, placing them in difficulty level 4. The recent wrong attempt indicates a misconception with the area formula, so this skill will help correct that.",
  "target_misconception": "Incorrect formula for area"
}
```