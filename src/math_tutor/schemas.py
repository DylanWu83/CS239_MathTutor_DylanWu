from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from math_tutor.config import canonical_topic


def _as_int(value: Any) -> int:
    if isinstance(value, bool):
        raise TypeError("boolean is not an int")
    if isinstance(value, str):
        value = value.strip().rstrip(".")
        if value in {"A", "B", "C", "D"}:
            return "ABCD".index(value)
        value = value.lower().removeprefix("choice ").strip()
    return int(value)


def _as_notes(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, dict):
        return [str(item) for item in value.values()]
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value]


class LessonPlan(BaseModel):
    topic: str = Field(description="Math topic to practice next")
    difficulty: int = Field(ge=1, le=5, description="Difficulty from 1 (intro) to 5 (stretch)")
    skill: str = Field(description="Specific skill within the topic")
    rationale: str = Field(description="Why this topic and difficulty were chosen")
    target_misconception: str | None = Field(
        default=None,
        description="Misconception to probe, if any",
    )

    @field_validator("topic")
    @classmethod
    def normalize_topic(cls, value: str) -> str:
        return canonical_topic(value)

    @field_validator("difficulty", mode="before")
    @classmethod
    def parse_difficulty(cls, value: Any) -> int:
        return max(1, min(5, _as_int(value)))


class MultipleChoiceQuestion(BaseModel):
    topic: str
    difficulty: int = Field(ge=1, le=5)
    skill: str
    stem: str = Field(description="Question text only; do not include choices")
    choices: list[str] = Field(min_length=4, max_length=4, description="Exactly four answer choices")
    correct_answer: str = Field(description="Exact text of the mathematically correct choice")
    correct_index: int = Field(ge=0, le=3, description="Index of the correct choice")
    explanation: str = Field(description="Why the correct choice is right")
    distractor_notes: list[str] = Field(
        default_factory=list,
        description="What misconception each wrong choice represents",
    )

    @field_validator("topic")
    @classmethod
    def normalize_topic(cls, value: str) -> str:
        return canonical_topic(value)

    @field_validator("difficulty", "correct_index", mode="before")
    @classmethod
    def parse_ints(cls, value: Any) -> int:
        return _as_int(value)

    @field_validator("choices", mode="before")
    @classmethod
    def parse_choices(cls, value: Any) -> list[str]:
        if isinstance(value, dict):
            value = list(value.values())
        items = [str(item).strip() for item in value]
        if len(items) != 4:
            raise ValueError("Need exactly four choices")
        return items

    @field_validator("distractor_notes", mode="before")
    @classmethod
    def parse_notes(cls, value: Any) -> list[str]:
        return _as_notes(value)

    @model_validator(mode="after")
    def set_correct_index_from_answer(self) -> MultipleChoiceQuestion:
        answer = self.correct_answer.strip().casefold()
        matching_indices = [
            index
            for index, choice in enumerate(self.choices)
            if choice.strip().casefold() == answer
        ]
        if len(matching_indices) != 1:
            raise ValueError("correct_answer must match exactly one choice")
        self.correct_index = matching_indices[0]
        return self


class Diagnosis(BaseModel):
    is_correct: bool
    misconception: str | None = None
    explanation: str
    recommended_topic: str
    recommended_difficulty: int = Field(ge=1, le=5)
    mastery_note: str = Field(description="One sentence on what the learner should do next")
    validated_correct_index: int = Field(
        ge=0,
        le=3,
        description="Index of the mathematically correct choice after independently checking it",
    )

    @field_validator("recommended_topic")
    @classmethod
    def normalize_recommended_topic(cls, value: str) -> str:
        return canonical_topic(value)

    @field_validator("recommended_difficulty", mode="before")
    @classmethod
    def parse_difficulty(cls, value: Any) -> int:
        return max(1, min(5, _as_int(value)))

    @field_validator("validated_correct_index", mode="before")
    @classmethod
    def parse_correct_index(cls, value: Any) -> int:
        return _as_int(value)

    @field_validator("is_correct", mode="before")
    @classmethod
    def parse_bool(cls, value: Any) -> bool:
        if isinstance(value, str):
            return value.strip().lower() in {"true", "yes", "correct", "1"}
        return bool(value)
