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

Chatbot B will instead use a specific free model through OpenRouter. A fixed model endpoint will be used rather than OpenRouter's random free-model router so that the experimental model identity remains known and reproducible.

Planned model:

`nvidia/nemotron-3-ultra-550b-a55b:free`

## Current prototype status

- Chatbot A: Google Gemini - working.
- Chatbot B: Groq trial discontinued; OpenRouter replacement in progress.
- Chatbot C: not yet implemented.
- Shared Google Drive engineering-document source: planned for a later milestone after the model connections are working.
