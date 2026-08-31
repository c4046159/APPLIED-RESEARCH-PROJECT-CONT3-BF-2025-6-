# Applied Research Project — Controlled AI Chatbot Comparison

A reproducible Streamlit prototype/final system for an MSc Applied Research Project comparing
three current AI chatbot/model systems under a controlled interface.

## Systems

| Blind label | System | Model ID |
|---|---|---|
| Chatbot A | Google Gemini | `gemini-3.1-flash-lite` |
| Chatbot B | OpenAI GPT-OSS 120B via Groq | `openai/gpt-oss-120b` |
| Chatbot C | NVIDIA Nemotron 3 Ultra via OpenRouter | `nvidia/nemotron-3-ultra-550b-a55b:free` |

The blind labels are intended for scoring. Reveal the mapping only after manual evaluation.

## Why one interface?

The research question concerns differences between chatbot systems. If each chatbot had a different
UI, prompt template, temperature or logging method, those differences would become confounding
variables. This application therefore keeps the experimental shell constant and swaps the backend.

## Local setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create API keys

Create free API keys for:
- Google AI Studio / Gemini API
- GroqCloud
- OpenRouter

### 3. Add local Streamlit secrets

Copy:

```text
.streamlit/secrets.toml.example
```

to:

```text
.streamlit/secrets.toml
```

and replace the placeholders.

Never commit the real secret file.

### 4. Launch

```bash
streamlit run streamlit_app.py
```

## Benchmark mode

For batch testing, set the same API keys as environment variables (or in a local `.env` file):

```text
GEMINI_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
```

Verify the three API connections first:

```bash
python -m evaluation.smoke_test
```

Then run the benchmark. See `evaluation/README.md` for the free-tier-safe split-run procedure:

```bash
python -m evaluation.run_benchmark --repetitions 3 --shuffle
```

The default benchmark contains 24 synthetic prompts. With 3 models and 3 repetitions,
that produces 216 responses.

## Research outputs

Runs are appended to:
- `data/chatbot_runs.csv`
- `data/chatbot_runs.jsonl`

Do not edit the raw final-run file after data collection. Make a copy for cleaning/analysis.

## Streamlit Community Cloud

The app can be deployed free from a GitHub repository using Streamlit Community Cloud.
Add API keys through the app's Secrets settings, not the repository.

## Ethics and privacy

This project is designed to avoid personal data collection. Use only synthetic/public prompts.
Never paste client passwords, confidential engineering data, personal identifiers or commercially
sensitive information into free-tier model endpoints.

## Recommended versioning

- `v0.1-prototype`: first working three-backend app.
- `v0.2-pilot`: logging and pilot benchmark validated.
- `v0.9-evaluation`: benchmark frozen and full experiment run.
- `v1.0-final`: assessment version with results/screenshots/documentation.

See `docs/research_design_notes.md` and `evaluation/README.md`.
