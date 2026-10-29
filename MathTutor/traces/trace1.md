# Trace for correct answer

## Curriculum and Adaptive Difficulty Designer

Input:
Using this learner profile, pick the next practice item.

New learner. No attempts yet.
Current topic: whole-number arithmetic
Current difficulty: 5
Current topic mastery: 0.91
Use the current topic's mastery to determine difficulty.

Choose topic using exactly one of these canonical names: ['whole-number arithmetic', 'fractions and decimals', 'percentages and ratios', 'pre-algebra (integers)', 'linear equations', 'geometry (area, perimeter, angles)', 'word problems'].
Do not create a new topic, alter capitalization, or use a synonym.
Difficulty is determined by the selected topic's mastery: 0.0–<0.2 is 1, 0.2–<0.4 is 2, 0.4–<0.6 is 3, 0.6–<0.8 is 4, and 0.8–1.0 is 5. If the current topic has mastery 1.0, choose the following topic in the allowed list.
Return ONLY JSON with keys: topic, difficulty (int 1-5), skill, rationale, target_misconception (string or null).

Output:
```json
{
  "topic": "fractions and decimals",
  "difficulty": 5,
  "skill": "Converting between fractions and decimals",
  "rationale": "The learner has mastered whole-number arithmetic, and since no other topics have been practiced, introducing fractions and decimals is the next step. The difficulty is set to 5 as the learner is new to this topic and needs to build foundational understanding.",
  "target_misconception": null
}
```

## Math Question Generator

Input:
Create one multiple-choice math question that matches this plan:
- topic: fractions and decimals
- difficulty: 5
- skill: Converting between fractions and decimals
- rationale: The learner has mastered whole-number arithmetic, and since no other topics have been practiced, introducing fractions and decimals is the next step. The difficulty is set to 5 as the learner is new to this topic and needs to build foundational understanding.
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
  "topic": "fractions and decimals",
  "difficulty": 5,
  "skill": "Converting between fractions and decimals",
  "stem": "Convert the fraction 3/8 to a decimal.",
  "choices": [
    "0.375",
    "0.38",
    "0.37",
    "0.36"
  ],
  "correct_answer": "0.375",
  "correct_index": 0,
  "explanation": "To convert the fraction 3/8 to a decimal, divide 3 by 8. 3 divided by 8 equals 0.375.",
  "distractor_notes": {
    "0.38": "This is a close approximation but not the exact value.",
    "0.37": "This is a common mistake when rounding too early.",
    "0.36": "This is a result of dividing 3 by 9 instead of 8."
  }
}
```

## Diagnostic and Misconception Analyst

Input:
Diagnose this attempt.

Learner profile:
New learner. No attempts yet.
Current topic: whole-number arithmetic
Current difficulty: 5
Current topic mastery: 0.91
Use the current topic's mastery to determine difficulty.

Question: Convert the fraction 3/8 to a decimal.
Choices: [(0, '0.36'), (1, '0.38'), (2, '0.375'), (3, '0.37')]
Correct choice: C. 0.375
Learner chose: C. 0.375
Author explanation: To convert the fraction 3/8 to a decimal, divide 3 by 8. 3 divided by 8 equals 0.375.
Distractor notes: ['This is a close approximation but not the exact value.', 'This is a common mistake when rounding too early.', 'This is a result of dividing 3 by 9 instead of 8.']

Use exactly one canonical topic from this list when recommending a topic: ['whole-number arithmetic', 'fractions and decimals', 'percentages and ratios', 'pre-algebra (integers)', 'linear equations', 'geometry (area, perimeter, angles)', 'word problems']. If no topic change is needed, recommend 'fractions and decimals'.
Independently calculate the correct answer rather than blindly trusting the answer key. If the key conflicts with the calculation, explain the conflict and return the index of the mathematically correct choice. If the key is correct, return its index unchanged.
If the learner is correct, misconception must be null. recommended_difficulty must be an integer 1-5. If they missed an easy item, keep or lower difficulty. If they got a hard item right, consider raising it. Return ONLY JSON with keys: is_correct, misconception, explanation, recommended_topic, recommended_difficulty, mastery_note, and validated_correct_index (int 0-3), the index of the mathematically correct choice after your independent check.

Output:
``` json
{
  "is_correct": true,
  "misconception": null,
  "explanation": "The learner correctly converted the fraction 3/8 to the decimal 0.375 by dividing 3 by 8. The author's explanation is accurate, and the learner's choice matches the correct answer.",
  "recommended_topic": "fractions and decimals",
  "recommended_difficulty": 5,
  "mastery_note": "The learner's mastery of 0.91 in fractions and decimals is high, and they correctly answered a challenging item.",
  "validated_correct_index": 2
}
```