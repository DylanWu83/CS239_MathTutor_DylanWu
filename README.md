# CS239 Adaptive Math Tutor

Local multi-agent study app: **CrewAI** agents talk to **Ollama** on your machine and run an adaptive multiple-choice math tutor.

This repository is laid out for the CS239 submission format.

## Application description (requirements archive)

| File | Contents |
| --- | --- |
| [`app.md`](app.md) | Purpose and supported tasks |
| [`policy.md`](policy.md) | Policies P1–P10 |
| [`tools.md`](tools.md) | Agent tools (none) |
| [`agents/`](agents/) | One spec per agent, including the actual system and task prompts |
| [`episodes/`](episodes/) | Example episodes with policy IDs |

## Source and tests (whole archive)

Setup, dependencies, run instructions, example usage, and external requirements are in [`src/README.md`](src/README.md).

Test-case descriptions are in [`tests/README.md`](tests/README.md).

```
app.py                 Streamlit UI
src/math_tutor/        Agents, crews, learner state
src/README.md          Setup and run
tests/README.md        Test cases
requirements.txt
.env.example
```

## Quick start

Ollama must be running at `http://localhost:11434` with a pulled chat model.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Change the model with `OLLAMA_MODEL` in `.env`. Full setup notes, including Unix commands and environment variables, are in [`src/README.md`](src/README.md).
