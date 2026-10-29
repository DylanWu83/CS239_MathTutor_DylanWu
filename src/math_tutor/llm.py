from crewai import LLM

from math_tutor.config import OLLAMA_BASE_URL, OLLAMA_MODEL


def local_llm() -> LLM:
    return LLM(
        model=f"ollama/{OLLAMA_MODEL}",
        base_url=OLLAMA_BASE_URL,
        temperature=0.3,
    )
