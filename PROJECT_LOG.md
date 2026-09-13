# Applied Research Project - Development Log

## 12 September 2026 - Initial cloud prototype

- Created a simple Streamlit application and deployed it from GitHub using Streamlit Community Cloud.
- Docker was considered but removed from the implementation because Streamlit Community Cloud already provides the hosted execution environment needed for the project.
- Chatbot A was connected to the Google Gemini API.
- The first attempted Gemini model returned a temporary 503 high-demand error, so the prototype was changed to `gemini-3.5-flash-lite`.
- Chatbot A then responded successfully through the deployed Streamlit application.

## 13 September 2026 - Groq provider trial discontinued

- Chatbot B was initially planned to use `openai/gpt-oss-120b` through Groq.
- The Streamlit application successfully reached the Groq API but repeatedly received `401 Invalid API Key` responses.
- A new API key was attempted, but the account/key setup presented a billing/payment path that was not suitable for this project.
- The project requirement is to use services that can be implemented without paid API access, so further time was not spent troubleshooting Groq.
- Groq is therefore recorded as an attempted but discontinued provider rather than as a programming failure.
- Although Groq currently documents a Free plan, the implementation decision was based on the actual account/setup experience and the project's no-payment constraint.

## 13 September 2026 - OpenRouter provider trial discontinued

- Chatbot B was then tested through OpenRouter using fixed free-model endpoints.
- The first model tested was `nvidia/nemotron-3-ultra-550b-a55b:free`.
- The request reached OpenRouter but returned a response without the expected `choices` field.
- A second free model, `poolside/laguna-s-2.1:free`, was then tested.
- This request returned `Provider returned error` from OpenRouter.
- These failures were treated as free-endpoint/provider availability issues rather than as failures of the Streamlit application itself.
- OpenRouter was therefore discontinued for Chatbot B because repeated upstream-provider failures made it unsuitable for a simple and reproducible prototype at this stage.

## 13 September 2026 - Chatbot B moved to Mistral

- Chatbot B was changed to use the official Mistral API directly.
- Mistral Studio currently provides a Free mode intended for evaluation and prototyping, with no credit card required according to the official setup documentation.
- The implementation uses the official `mistralai` Python SDK and the `mistral-small-latest` model.
- This keeps the code simple and removes the additional OpenRouter routing layer.

## Current prototype status

- Chatbot A: Google Gemini 3.5 Flash-Lite - working.
- Chatbot B: Mistral Small through the official Mistral API - implementation ready for testing.
- Chatbot C: not yet implemented.
- Shared Google Drive engineering-document source: planned for a later milestone after the model connections are working.
