import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
LEARNER_PATH = DATA_DIR / "learner.json"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PYTHONUTF8", "1")

TOPICS = [
    "whole-number arithmetic",
    "fractions and decimals",
    "percentages and ratios",
    "pre-algebra (integers)",
    "linear equations",
    "geometry (area, perimeter, angles)",
    "word problems",
]


def canonical_topic(value: str) -> str:
    normalized = "".join(character for character in value.casefold() if character.isalnum())
    for topic in TOPICS:
        candidate = "".join(character for character in topic.casefold() if character.isalnum())
        if normalized == candidate:
            return topic
    aliases = {
        "integers": "pre-algebra (integers)",
        "prealgebra": "pre-algebra (integers)",
        "geometry": "geometry (area, perimeter, angles)",
    }
    if normalized in aliases:
        return aliases[normalized]
    raise ValueError(f"Unknown topic {value!r}. Expected one of: {', '.join(TOPICS)}")


def difficulty_for_mastery(mastery: float) -> int:
    if not 0.0 <= mastery <= 1.0:
        raise ValueError(f"Mastery must be between 0 and 1, got {mastery!r}")
    return min(5, int(mastery * 5) + 1)


def next_topic(topic: str) -> str:
    index = TOPICS.index(canonical_topic(topic))
    return TOPICS[(index + 1) % len(TOPICS)]


DIFFICULTY_LABELS = {
    1: "introductory",
    2: "easy",
    3: "on-level",
    4: "challenging",
    5: "stretch",
}
