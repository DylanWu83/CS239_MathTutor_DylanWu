# Adaptive Math Tutor

Local multi-agent math tutor: **CrewAI** agents talk to **Ollama** on your machine. The Streamlit UI runs an adaptive four-choice practice loop and saves a learner profile on disk.

Application description files for this project live at the repository root (`app.md`, `policy.md`, `tools.md`, `agents/`, `episodes/`). This README covers setup, dependencies, and how to run the implementation.

## External requirements

| Requirement | Notes |
| --- | --- |
| Python 3.12 | Project was developed with 3.12. |
| [Ollama](https://ollama.com) | Local LLM server at `http://localhost:11434`. |
| A pulled chat model | Default in code: `qwen2.5:7b`. `.env.example` uses `llama3.2`. Set `OLLAMA_MODEL` to whichever you pulled. |

No OpenAI, Anthropic, or other hosted LLM API key is required. Agents call `ollama/{OLLAMA_MODEL}` through CrewAI’s `LLM` wrapper.

## Dependencies

From the **repository root**:

```text
crewai>=1.15.0
streamlit>=1.40.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

See `requirements.txt`.

## Setup

### 1. Install and start Ollama

Install Ollama, confirm the service answers at `http://localhost:11434`, and pull a model:

```powershell
winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements
ollama pull llama3.2
```

For stronger JSON and arithmetic, pull `qwen2.5:7b` and set `OLLAMA_MODEL=qwen2.5:7b` in `.env`.

### 2. Python environment

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

On Unix-like shells:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Environment variables

Copy `.env.example` to `.env` (gitignored). Supported variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Local Ollama HTTP API |
| `OLLAMA_MODEL` | `qwen2.5:7b` in `config.py`; `llama3.2` in `.env.example` | Model name **without** the `ollama/` prefix |
| `CREWAI_DISABLE_TELEMETRY` | `true` | Disable CrewAI telemetry |

## Run

Ollama must be running. From the **repository root** (not from `src/`):

```powershell
streamlit run app.py
```

Open the URL Streamlit prints (typically `http://localhost:8501`).

The first question is slow: the curriculum agent and the question generator both run before the item appears. After you submit, the diagnostic agent runs.

## Example invocation

1. Start Ollama and Streamlit as above.
2. Click **Next question**. Wait until a stem and four choices appear.
3. Select A–D and click **Submit**.
4. Read the diagnosis, then click **Continue** for another item.
5. Optional: **Reset learner data** in the sidebar to wipe `data/learner.json`.

Expected behavior: the sidebar shows topic, difficulty, mastery bars, and any known misconceptions. Difficulty follows the selected topic's mastery band (0.0–<0.2: 1, 0.2–<0.4: 2, 0.4–<0.6: 3, 0.6–<0.8: 4, 0.8–1.0: 5). When a topic reaches 1.0 mastery, the next item moves to the following topic in the curriculum list.

## How a round works

1. Curriculum agent reads `data/learner.json` and returns a `LessonPlan`.
2. Question generator returns a `MultipleChoiceQuestion`. The app shuffles choices.
3. The learner picks A–D.
4. Diagnostic agent returns a `Diagnosis`, including `validated_correct_index`.
5. The app updates mastery and saves the profile.

Agents do not use function-calling tools (`tools.md` is `None`). JSON from each agent is parsed with Pydantic schemas in `src/math_tutor/schemas.py`.

## Layout

```
app.py                 Streamlit UI (run from repository root)
src/math_tutor/        Agents, crews, learner state, LLM wrapper
src/README.md          This file
tests/README.md        Described test cases
requirements.txt
.env.example
```
