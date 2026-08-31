# Research design notes for the assessment

## Experimental object

This repository implements three chatbot systems behind one controlled interface.
The front-end, normalized prompt construction, generation temperature, maximum output,
benchmark set and logging schema are held constant as far as the provider APIs permit.

## Independent variable

Chatbot/model system:

- Chatbot A — Google Gemini 3.1 Flash-Lite.
- Chatbot B — OpenAI GPT-OSS 120B served through GroqCloud.
- Chatbot C — NVIDIA Nemotron 3 Ultra free endpoint through OpenRouter.

For blind manual evaluation, use A/B/C labels and conceal this mapping from the scorer.

## Dependent variables

Primary:
- task-specific rubric score / response quality;
- response latency;
- successful-response rate / API error rate.

Secondary:
- token usage, where exposed consistently enough for comparison;
- qualitative error type;
- response consistency across repeated trials.

## Controls

- identical benchmark prompts;
- same normalized system instruction;
- same temperature (0.2);
- same nominal max output tokens (900);
- same test machine/orchestration code;
- shuffled execution order with fixed seed;
- repeated trials;
- no web-search or external tools intentionally enabled.

## Threats to validity

1. Provider infrastructure differs, so latency is a system-level comparison rather than a pure model-speed comparison.
2. Free-tier capacity and throttling may vary over time.
3. Vendor/model updates can occur; record model IDs and test dates.
4. Token accounting is not perfectly standardized across providers.
5. Manual scores can introduce evaluator bias; use blind labels and explicit rubrics.
6. One benchmark set cannot represent all real-world chatbot tasks.
7. Free endpoints may have different data-processing terms, so only synthetic/public test data should be used.

## Prototype-to-final progression

v0.1 Prototype:
- establish all three API connections;
- run one smoke-test prompt per model;
- verify CSV/JSONL logging;
- verify blind labels.

v0.2 Pilot:
- run 6-8 benchmark prompts;
- inspect failures and scoring clarity;
- freeze prompt wording and rubrics after justified revisions.

v0.9 Evaluation candidate:
- run the complete benchmark with repetitions;
- preserve raw results unchanged;
- analyse metrics separately from application code.

v1.0 Final:
- fix defects only; do not alter the frozen benchmark after final data collection;
- tag the repository release/commit used for the assessment;
- capture architecture, UI and results screenshots;
- export final results and document limitations.
