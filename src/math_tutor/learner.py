from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator

from math_tutor.config import (
    DATA_DIR,
    LEARNER_PATH,
    TOPICS,
    canonical_topic,
    difficulty_for_mastery,
    next_topic,
)


class Attempt(BaseModel):
    timestamp: str
    topic: str
    difficulty: int
    skill: str
    stem: str
    choices: list[str]
    correct_index: int
    user_index: int
    is_correct: bool
    misconception: str | None = None


class LearnerProfile(BaseModel):
    topic_mastery: dict[str, float] = Field(
        default_factory=lambda: {topic: 0.91 for topic in TOPICS}
    )
    current_topic: str = TOPICS[0]
    current_difficulty: int = 5
    known_misconceptions: list[str] = Field(default_factory=list)
    history: list[Attempt] = Field(default_factory=list)

    @field_validator("current_topic")
    @classmethod
    def normalize_current_topic(cls, value: str) -> str:
        return canonical_topic(value)

    @field_validator("topic_mastery", mode="before")
    @classmethod
    def normalize_mastery_topics(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        totals: dict[str, float] = {}
        counts: dict[str, int] = {}
        for raw_topic, raw_score in value.items():
            topic = canonical_topic(str(raw_topic))
            totals[topic] = totals.get(topic, 0.0) + float(raw_score)
            counts[topic] = counts.get(topic, 0) + 1
        return {topic: total / counts[topic] for topic, total in totals.items()}

    def summary_for_agents(self, last_n: int = 8) -> str:
        recent = self.history[-last_n:]
        if not recent:
            return (
                "New learner. No attempts yet.\n"
                f"Current topic: {self.current_topic}\n"
                f"Current difficulty: {self.current_difficulty}\n"
                f"Current topic mastery: "
                f"{self.topic_mastery.get(self.current_topic, 0.4):.2f}\n"
                "Use the current topic's mastery to determine difficulty."
            )
        lines = [
            f"Current topic: {self.current_topic}",
            f"Current difficulty: {self.current_difficulty}",
            "Topic mastery (0–1): "
            + ", ".join(f"{k}={v:.2f}" for k, v in self.topic_mastery.items()),
        ]
        if self.known_misconceptions:
            lines.append("Known misconceptions: " + "; ".join(self.known_misconceptions[-6:]))
        lines.append("Recent attempts:")
        for attempt in recent:
            mark = "correct" if attempt.is_correct else "WRONG"
            extra = f" | misconception: {attempt.misconception}" if attempt.misconception else ""
            lines.append(
                f"- [{mark}] d{attempt.difficulty} {attempt.topic} / {attempt.skill}: "
                f"chose {attempt.user_index}, correct {attempt.correct_index}{extra}"
            )
        return "\n".join(lines)

    def record(
        self,
        question: dict[str, Any],
        user_index: int,
        diagnosis: dict[str, Any],
    ) -> Attempt:
        is_correct = user_index == question["correct_index"]
        topic = canonical_topic(question["topic"])
        difficulty = int(question["difficulty"])
        delta = 0.08 if is_correct else -0.07
        if difficulty >= 4 and is_correct:
            delta += 0.03
        if difficulty <= 2 and not is_correct:
            delta -= 0.03
        current = self.topic_mastery.get(topic, 0.4)
        self.topic_mastery[topic] = max(0.0, min(1.0, current + delta))

        misconception = diagnosis.get("misconception") if not is_correct else None
        if misconception:
            if misconception not in self.known_misconceptions:
                self.known_misconceptions.append(misconception)
        elif is_correct and self.known_misconceptions:
            # Clear a matching misconception when the learner succeeds on that skill.
            skill = question.get("skill", "")
            self.known_misconceptions = [
                item for item in self.known_misconceptions if skill.lower() not in item.lower()
            ]

        if self.topic_mastery[topic] >= 1.0:
            self.current_topic = next_topic(topic)
        else:
            self.current_topic = canonical_topic(
                diagnosis.get("recommended_topic") or topic
            )
        self.current_difficulty = difficulty_for_mastery(
            self.topic_mastery.get(self.current_topic, 0.4)
        )

        attempt = Attempt(
            timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            topic=topic,
            difficulty=difficulty,
            skill=question.get("skill", ""),
            stem=question["stem"],
            choices=question["choices"],
            correct_index=question["correct_index"],
            user_index=user_index,
            is_correct=is_correct,
            misconception=misconception,
        )
        self.history.append(attempt)
        return attempt

    def save(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        LEARNER_PATH.write_text(self.model_dump_json(indent=2), encoding="utf-8")

    @classmethod
    def load(cls) -> LearnerProfile:
        if LEARNER_PATH.exists():
            return cls.model_validate_json(LEARNER_PATH.read_text(encoding="utf-8"))
        profile = cls()
        profile.save()
        return profile
