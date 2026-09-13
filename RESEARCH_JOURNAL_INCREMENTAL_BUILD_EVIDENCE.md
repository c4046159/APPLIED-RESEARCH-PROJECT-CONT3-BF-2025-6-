# Research Journal - Incremental Build Evidence Record

Date: 13 September 2026

## Planned incremental extension

Add a second independent chatbot provider to the existing Streamlit prototype so that two different LLM systems can be tested through the same interface; this matters because the research requires a controlled comparison, and success would mean Chatbot B can accept the same prompt as Chatbot A and return a valid response without paid API access.

## Why this extension is research-motivated

The research is intended to compare AI chatbot systems under common conditions rather than evaluate a single model. Adding Chatbot B is therefore a necessary methodological extension, not a cosmetic feature. It tests the practical assumption that multiple independent cloud LLMs can be integrated into one controlled prototype using the same deployment environment.

## Build and version-control evidence

The prototype was already deployed from GitHub through Streamlit Community Cloud, with Chatbot A using Google Gemini successfully. The second-provider build was then attempted incrementally and committed in small changes.

Relevant commits include:

- `cb6f05e` - Document Groq trial and free-provider decision.
- `4219ba1` - Replace Groq dependency with requests for OpenRouter.
- `a3eb6ac` - Replace Groq Chatbot B with free OpenRouter Nemotron model.
- `4a2470f` - Use more reliable free OpenRouter model and improve error handling.
- `651b2d7` - Document OpenRouter model availability issue and Chatbot B revision.
- `7566a97` - Replace OpenRouter Chatbot B with Mistral free-mode API.
- `af01d2d` - Use official Mistral Python SDK for Chatbot B.
- `88217b4` - Document OpenRouter trial and switch Chatbot B to Mistral.
- `f93ed33` - Document Mistral 429 result and incremental build evidence.
- `703f0ea` - Replace Mistral dependency with Cohere for Chatbot B.
- `11191c2` - Use Cohere Command A Plus for Chatbot B.
- `3f45b8a` - Document two-chatbot scope decision and Cohere candidate.

## Validation method

A simple functional validation prompt was used: `What is a PLC?`

The purpose was not yet to compare answer quality. At this stage the validation criterion was basic connectivity and operational feasibility:

1. Did Streamlit accept the user prompt?
2. Did the API credential authenticate?
3. Did the request reach the external model provider?
4. Did the provider return a usable chatbot response?
5. Could this be achieved without paid API access?

This simple test was appropriate because it isolated provider connectivity before introducing more complex research variables such as shared engineering documentation, response-time measurement or formal scoring.

## Observed validation results

### Baseline: Chatbot A - Google Gemini

- Initial Gemini model returned `503 UNAVAILABLE` because of high demand.
- Model changed to `gemini-3.5-flash-lite`.
- The same Streamlit application then returned valid answers successfully.
- Result: PASS for basic end-to-end cloud chatbot operation.

### Chatbot B attempt 1 - Groq

- Repeated response: `401 Invalid API Key`.
- A new key was attempted.
- The account/key path did not meet the project's no-payment requirement.
- Result: FAIL for project feasibility; discontinued.

### Chatbot B attempt 2 - OpenRouter / Nemotron

- Request reached OpenRouter.
- Response did not contain the expected `choices` field, producing `KeyError: 'choices'` in the initial implementation.
- Error handling was then improved.
- Result: FAIL for reliable operation.

### Chatbot B attempt 3 - OpenRouter / Poolside Laguna

- Response: `Provider returned error`.
- Result: FAIL for reliable operation; OpenRouter discontinued for Chatbot B.

### Chatbot B attempt 4 - Mistral

- API authentication succeeded and the request reached Mistral.
- Validation prompt returned HTTP `429` with `Rate limit exceeded`, error code `1300`.
- Result: FAIL for practical repeated testing under the current free-account limits.

### Chatbot B attempt 5 - Cohere

- Cohere selected because trial-key limits are published and appear sufficient for the planned two-chatbot experiment.
- Current documented trial limits include 20 Chat requests/minute and 1,000 API calls/month.
- Chatbot B has been changed to `command-a-plus-05-2026` through the official Cohere Python SDK.
- Validation result: pending the next deployment test with `What is a PLC?`.

## Interpretation

The incremental build revealed that multi-model comparison depends on more than correct Python integration. External API availability, authentication policies, free-tier quotas and upstream-provider reliability directly affect whether an experimental system can be reproduced and tested consistently. This is relevant to the research because a fair comparison requires all selected chatbot systems to be available under sufficiently similar and repeatable testing conditions.

The failed integrations are therefore meaningful validation evidence rather than wasted development. They led to improvements in error handling and refined the provider-selection criteria: the final systems must offer stable, documented and genuinely usable no-payment access for the expected experimental workload.

## Scope decision: two final chatbots rather than three

The original concept considered three chatbot systems. The provider trials showed that adding and maintaining a third independent no-payment provider would increase the risk of incomplete test runs, quota problems and provider-side failures. The final scope has therefore been reduced to two chatbot systems.

This does not remove the comparative nature of the study. A controlled A-versus-B design still permits direct comparison of response quality, groundedness, latency, consistency and failure behaviour. Reducing the number of systems also allows more repetitions per condition and more careful analysis within the available project time.

## Deviations from the original plan

The original plan assumed that several provider APIs could be integrated by following their public documentation and supplying valid credentials. In practice, multiple candidate routes had to be rejected for operational reasons. The original three-chatbot concept was therefore reduced to a two-chatbot design so that the final experiment remains feasible and reproducible.

## Next steps before Week 12

1. Validate Cohere as Chatbot B using the same simple functional prompt.
2. Once Chatbot B returns reliably, freeze both final provider/model choices.
3. Introduce consistent response-time logging and common validation prompts for both systems.
4. Connect both final chatbots to the same research-safe engineering-document source.
5. Run repeated controlled tests and retain outputs for formal comparison.

## Preliminary 300-400 word journal draft

### Extension description

The incremental build aimed to extend my existing Streamlit prototype from one working cloud chatbot to a controlled comparison between two independent LLM providers using the same interface. This was necessary because the research project requires comparison between chatbot systems rather than evaluation of a single model. The intended success criterion was that Chatbot B would accept the same simple prompt as Chatbot A and return a valid response through a no-payment API route.

### Validation method used

I used a basic functional connectivity test before introducing more complex evaluation criteria. The prompt `What is a PLC?` was submitted through the deployed Streamlit interface. I checked whether the API key authenticated, whether the request reached the provider, and whether a usable response was returned. This approach was appropriate because it isolated provider feasibility from later variables such as engineering-document retrieval, latency measurement and answer-quality scoring.

### Results obtained

Chatbot A, using Gemini 3.5 Flash-Lite, responded successfully after an earlier Gemini model returned a temporary HTTP 503 high-demand error. Several alternatives were evaluated for Chatbot B. Groq repeatedly returned HTTP 401 `Invalid API Key` and the available account setup did not satisfy the project's no-payment requirement. OpenRouter was tested with two free models; one returned a response without the expected `choices` field and the other returned `Provider returned error`. Mistral authenticated successfully, but the first test returned HTTP 429 `Rate limit exceeded`. Cohere was therefore selected as the next candidate because its trial limits are explicitly published and appear sufficient for the planned test workload.

### Interpretation

These results showed that multi-model integration is constrained not only by Python implementation but also by service availability, authentication and free-tier quotas. This directly affects experimental reproducibility. The evidence also justified reducing the planned comparison from three chatbots to two, retaining a valid comparative design while reducing provider-related risk and allowing more rigorous repeated testing.

### Next steps

The next step is to validate Cohere as Chatbot B. If stable, both provider/model choices will be frozen before adding shared engineering-document retrieval, response-time measurement and formal repeated comparison tests.
