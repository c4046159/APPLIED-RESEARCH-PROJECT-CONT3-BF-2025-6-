# Research Journal - Incremental Build Evidence Record

Date: 13 September 2026

## Planned incremental extension

Add a second independent chatbot provider to the existing Streamlit prototype so that two different LLM systems can be tested through the same interface; this matters because the research requires a controlled multi-model comparison, and success would mean Chatbot B can accept the same prompt as Chatbot A and return a valid response without paid API access.

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

## Interpretation

The incremental build revealed that multi-model comparison depends on more than correct Python integration. External API availability, authentication policies, free-tier quotas and upstream-provider reliability directly affect whether an experimental system can be reproduced and tested consistently. This is relevant to the research because a fair comparison requires all selected chatbot systems to be available under sufficiently similar and repeatable testing conditions.

The failed integrations are therefore meaningful validation evidence rather than wasted development. They led to improvements in error handling and refined the provider-selection criteria: the final systems must offer stable, documented and genuinely usable no-payment access for the expected experimental workload.

## Deviations from the original plan

The original plan assumed that a second provider could be added by following its API documentation and supplying a valid key. In practice, three candidate routes had to be rejected for different operational reasons. The implementation scope was kept deliberately small and no additional features were introduced while provider feasibility remained unresolved.

## Next steps before Week 12

1. Test Cohere as the next candidate for Chatbot B.
2. Once Chatbot B returns reliably, freeze that provider/model rather than continuing to switch systems.
3. Add Chatbot C only after A and B are stable.
4. Introduce consistent response-time logging and common validation prompts.
5. Connect all final chatbots to the same research-safe engineering-document source only after model connectivity is stable.

## Preliminary 300-400 word journal draft

### Extension description

The incremental build aimed to extend my existing Streamlit prototype from one working cloud chatbot to two independent LLM providers using the same interface. This was necessary because the research project requires a controlled comparison between different chatbot systems rather than the evaluation of a single model. The intended success criterion was that Chatbot B would accept the same simple prompt as Chatbot A and return a valid response using a no-payment API route.

### Validation method used

I used a basic functional connectivity test before introducing more complex evaluation criteria. The prompt `What is a PLC?` was submitted through the deployed Streamlit interface. I checked whether the API key authenticated, whether the request reached the provider, and whether a usable response was returned. This approach was appropriate because it isolated provider feasibility from later variables such as engineering-document retrieval, latency measurement and answer-quality scoring.

### Results obtained

Chatbot A, using Gemini 3.5 Flash-Lite, responded successfully after an earlier Gemini model returned a temporary HTTP 503 high-demand error. Several alternatives were then evaluated for Chatbot B. Groq repeatedly returned HTTP 401 `Invalid API Key` and the available account setup did not satisfy the project's no-payment requirement. OpenRouter was tested with two free models; the first returned a response without the expected `choices` field and the second returned `Provider returned error`. Mistral authenticated successfully, but the first simple test returned HTTP 429 `Rate limit exceeded`.

### Interpretation

These results showed that multi-model integration is constrained not only by Python implementation but also by external service availability, authentication and free-tier quotas. This is relevant to the research because reliable access is necessary for a reproducible comparison. The failed trials also led me to improve API error handling and refine the provider-selection criteria.

### Next steps

The next step is to test a further provider with clearly documented free trial limits. Once a stable Chatbot B is confirmed, I will freeze that implementation, add Chatbot C, and then introduce common engineering-document retrieval and formal performance measurements.
