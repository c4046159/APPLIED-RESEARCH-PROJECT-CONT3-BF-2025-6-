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

### Design decision

Chatbot B was moved to OpenRouter so that a specific free model could be called through a simple REST API while keeping the experimental model identity known.

## 13 September 2026 - OpenRouter model revised

- The first OpenRouter model tested for Chatbot B was `nvidia/nemotron-3-ultra-550b-a55b:free`.
- The API request reached OpenRouter, but the application received a response without the expected `choices` field, producing the Python `KeyError: 'choices'` message.
- OpenRouter's current public model page showed relatively low recent availability for this free endpoint (approximately 73-75%), so the problem was treated as a provider/model availability issue rather than an authentication failure.
- Chatbot B was therefore changed to `poolside/laguna-s-2.1:free`, another fixed free OpenRouter model with much higher recent availability.
- Error handling was also improved so that future OpenRouter API errors display the provider's real error message rather than only a Python dictionary-key error.

## Current prototype status

- Chatbot A: Google Gemini 3.5 Flash-Lite - working.
- Chatbot B: OpenRouter / Poolside Laguna S 2.1 (free) - implementation updated, testing required.
- Chatbot C: not yet implemented.
- Shared Google Drive engineering-document source: planned for a later milestone after the model connections are working.
