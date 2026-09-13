# Applied Research Project - Development Log

## 12 September 2026 - Initial cloud prototype

- Created a simple Streamlit application and deployed it from GitHub using Streamlit Community Cloud.
- Docker was considered but removed from the implementation because Streamlit Community Cloud already provides the hosted execution environment needed for the project.
- Chatbot A was connected to the Google Gemini API.
- The first attempted Gemini model returned a temporary `503 UNAVAILABLE` high-demand error.
- The prototype was changed to `gemini-3.5-flash-lite`.
- Chatbot A then responded successfully through the deployed Streamlit application.

### Validation result

The successful Gemini response confirmed the basic cloud path was working end-to-end: GitHub source code -> Streamlit Community Cloud -> external LLM API -> response displayed in the browser.

## 13 September 2026 - Incremental build: adding a second independent chatbot provider

### Plan

The incremental extension was to add a second independent LLM provider to the existing Streamlit prototype so that the same interface could later be used to compare different chatbot systems under controlled conditions. A successful outcome would be a second chatbot that accepted the same test prompt as Chatbot A and returned a valid response without requiring paid API access.

### Groq provider trial discontinued

- Chatbot B was initially planned to use `openai/gpt-oss-120b` through Groq.
- The Streamlit application reached the Groq API but repeatedly received `401 Invalid API Key` responses.
- A new API key was attempted.
- The account/key setup presented a billing/payment path that was not suitable for this project's no-payment requirement.
- Groq was therefore recorded as an attempted but discontinued provider rather than as a programming failure.
- Commit evidence includes `cb6f05e` (Document Groq trial and free-provider decision), `4219ba1` (Replace Groq dependency with requests for OpenRouter), and `a3eb6ac` (Replace Groq Chatbot B with free OpenRouter Nemotron model).

### OpenRouter provider trial discontinued

- Chatbot B was then tested through OpenRouter using fixed free-model endpoints.
- The first model tested was `nvidia/nemotron-3-ultra-550b-a55b:free`.
- The request reached OpenRouter but returned a response without the expected `choices` field, initially producing a Python `KeyError: 'choices'`.
- Error handling was improved so that provider/API errors would be displayed rather than hidden by a dictionary-key error.
- A second free model, `poolside/laguna-s-2.1:free`, was then tested.
- This request returned `Provider returned error`.
- These results indicated that free upstream endpoint availability could affect reproducibility even when the application code and API authentication path were functioning.
- OpenRouter was discontinued for Chatbot B at this stage because repeated provider-side failures made it unsuitable for a simple, repeatable prototype.
- Commit evidence includes `4a2470f` (Use more reliable free OpenRouter model and improve error handling) and `651b2d7` (Document OpenRouter model availability issue and Chatbot B revision).

### Mistral provider trial discontinued

- Chatbot B was next changed to use the official Mistral API directly through the `mistralai` Python SDK.
- The API key was accepted and the request reached Mistral.
- The first simple validation prompt, `What is a PLC?`, returned HTTP `429` with: `Rate limit exceeded`, code `1300`.
- This was different from the Groq authentication failure because authentication had succeeded; the limiting factor was free-tier service quota/rate availability.
- Because the project requires repeated test calls for an empirical comparison and must avoid paid API access, Mistral was judged unsuitable for Chatbot B in its current free-account configuration.
- Commit evidence includes `7566a97` (Replace OpenRouter Chatbot B with Mistral free-mode API), `af01d2d` (Use official Mistral Python SDK for Chatbot B), and `88217b4` (Document OpenRouter trial and switch Chatbot B to Mistral).

### Reflection from the incremental build so far

The extension has shown that adding a second model is not only a coding problem. Authentication, provider availability, free-tier quotas and upstream service reliability are practical constraints that can directly affect the feasibility and reproducibility of an empirical chatbot comparison. The failed provider trials are therefore retained as development and validation evidence rather than removed from the record.

### Next planned provider

- Cohere is the next candidate for Chatbot B because it offers trial API access suitable for prototyping and provides published usage limits.
- The objective remains unchanged: obtain one stable, no-payment second chatbot before adding Chatbot C or the shared Google Drive knowledge source.

## Current prototype status

- Chatbot A: Google Gemini 3.5 Flash-Lite - working.
- Chatbot B: second-provider implementation under validation; Groq, OpenRouter and Mistral have been trialled and discontinued for documented reasons.
- Chatbot C: not yet implemented.
- Shared Google Drive engineering-document source: planned for a later milestone after the model connections are stable.
