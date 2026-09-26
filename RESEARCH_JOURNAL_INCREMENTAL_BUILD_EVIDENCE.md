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
- `0ba34a2` - Fix Cohere response parsing for thinking and text blocks.
- `03f7428` - Document Cohere structured response parsing result.
- `1c4a27e` - Record successful Cohere validation and freeze final two-chatbot scope.

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

- Cohere was selected because trial-key limits are published and appear sufficient for the planned two-chatbot experiment.
- Chatbot B was changed to `command-a-plus-05-2026` through the official Cohere Python SDK.
- The validation prompt reached Cohere and produced a structured response, confirming that the API key, request and model call were functioning.
- The first parser assumed `response.message.content[0]` would always be a text item and attempted to access `.text` directly.
- Command A+ returned a `thinking` block first, producing: `'ThinkingAssistantMessageResponseContentItem' object has no attribute 'text'`.
- The code was corrected to loop through the returned content and select the item where `content.type == "text"`.
- The same `What is a PLC?` validation prompt was then repeated.
- Chatbot B returned and displayed a correct natural-language response successfully in Streamlit.
- Result: PASS for full end-to-end Chatbot B operation.

## Interpretation

The incremental build revealed that multi-model comparison depends on more than correct Python integration. External API availability, authentication policies, free-tier quotas, structured response formats and upstream-provider reliability directly affect whether an experimental system can be reproduced and tested consistently. This is relevant to the research because a fair comparison requires all selected chatbot systems to be available under sufficiently similar and repeatable testing conditions.

The failed integrations are meaningful validation evidence rather than wasted development. They led to improvements in error handling, response parsing and provider-selection criteria. The Cohere test was particularly useful because it separated successful API/model execution from local response-processing logic: the model responded, but the application initially interpreted the structured response incorrectly. Correcting the parser and repeating the same validation prompt produced a successful end-to-end result.

## Scope decision: two final chatbots rather than three

The original concept considered three chatbot systems. The provider trials showed that adding and maintaining a third independent no-payment provider would increase the risk of incomplete test runs, quota problems and provider-side failures. The final scope has therefore been reduced to two chatbot systems.

This does not remove the comparative nature of the study. A controlled A-versus-B design still permits direct comparison of response quality, groundedness, latency, consistency and failure behaviour. Reducing the number of systems also allows more repetitions per condition and more careful analysis within the available project time.

Gemini 3.5 Flash-Lite and Cohere Command A+ are now frozen as the two final model/provider choices for the experiment.

## Deviations from the original plan

The original plan assumed that several provider APIs could be integrated by following their public documentation and supplying valid credentials. In practice, multiple candidate routes had to be rejected for operational reasons. The original three-chatbot concept was therefore reduced to a two-chatbot design so that the final experiment remains feasible and reproducible. The Cohere implementation also required a minor deviation from the initial parser because the reasoning-capable model can return a thinking block before the final text.

## Historical next steps before Week 12 (superseded)

1. Keep Gemini and Cohere fixed as the two final chatbot systems.
2. Introduce a shared research-safe engineering-document source used by both chatbots.
3. Add consistent response-time logging and common validation prompts for both systems.
4. Run repeated controlled tests and retain outputs for formal comparison.
5. Evaluate response quality, groundedness, consistency, latency and failure behaviour under the same experimental conditions.

## Preliminary 300-400 word journal draft

### Extension description

The incremental build extended my existing Streamlit prototype from one working cloud chatbot to a controlled comparison between two independent LLM providers using the same interface. This was necessary because the research project requires comparison between chatbot systems rather than evaluation of a single model. The intended success criterion was that Chatbot B would accept the same simple prompt as Chatbot A and return a valid response through a no-payment API route.

### Validation method used

I used a basic functional connectivity test before introducing more complex evaluation criteria. The prompt `What is a PLC?` was submitted through the deployed Streamlit interface. I checked whether the API key authenticated, whether the request reached the provider, and whether a usable response was returned. This approach was appropriate because it isolated provider feasibility from later variables such as engineering-document retrieval, latency measurement and answer-quality scoring.

### Results obtained

Chatbot A, using Gemini 3.5 Flash-Lite, responded successfully after an earlier Gemini model returned a temporary HTTP 503 high-demand error. Several alternatives were evaluated for Chatbot B. Groq repeatedly returned HTTP 401 `Invalid API Key`; OpenRouter produced provider-side failures; and Mistral authenticated successfully but returned HTTP 429 `Rate limit exceeded`. Cohere was then tested using Command A+. The request successfully reached the model, but the application initially attempted to read the first response item as plain text. Command A+ returned a structured `thinking` block before the text response, producing a Python attribute error. The parser was corrected to locate the returned item whose type was `text`. Repeating the same validation prompt then produced a correct response in Streamlit, confirming that Chatbot B was fully operational.

### Interpretation

These results showed that multi-model integration is constrained not only by Python implementation but also by service availability, authentication, quotas and response structure. The evidence justified reducing the planned comparison from three chatbots to two, retaining a valid comparative design while reducing provider-related risk. The successful Cohere retest also demonstrated the value of testing one change at a time and repeating the same validation condition after a fix.

### Next steps

Gemini and Cohere will now remain fixed as the two final chatbot systems. The next build will connect both models to the same research-safe engineering-document source before adding response-time measurement and formal repeated comparison tests.


## Final development phase update - 26 September 2026

The original incremental-build record above describes the point at which the project had only just stabilised the second provider. Subsequent work materially extended the prototype and changed the research interpretation.

### Shared document grounding completed

The two frozen models were connected to the same Google Drive research source. The final ingestion path was simplified to PDF only. PDF text is extracted with `pypdf`, divided into 180-word chunks with a 30-word overlap, and ranked using a deliberately simple keyword-overlap method. The top four passages are inserted into one common grounded prompt and supplied to both Gemini and Cohere. This was chosen over provider-specific retrieval so that retrieval itself would not differ between experimental conditions.

### Results and metrics functionality completed

The application records timestamp, exact question, model/provider, source reference, full raw response, model/API latency and error information for every run. Manual scoring was added for correctness, relevance and faithfulness on 0-2 scales, with a calculated 0-6 total quality score. Consistency across three repetitions is scored 0-2. Results can be downloaded locally and saved as a new timestamped CSV into the same shared Google Drive folder used for PDFs.

### Architecture simplified after an unsuccessful persistence experiment

A GitHub-based cumulative-results design was briefly attempted. It introduced repository-token handling, branch/file update logic and deployment fragility, and the Streamlit application stopped working during this phase. The design was deliberately rolled back. GitHub now remains source/version control only; Streamlit holds current-session results and Google Drive stores exported session evidence. This backtrack is retained as evidence of iterative engineering and scope control.

### Corpus-scale limitation discovered

The PDF-only Drive repository was tested with 883 PDFs totalling approximately 2.08 GB. Although Drive pagination was corrected so the application could enumerate more than the first 100 files, the full architecture became effectively unusable at this scale. Downloading, parsing and repeatedly scoring the resulting corpus creates excessive I/O, memory and retrieval work. This finding changed the interpretation of the artefact: the prototype demonstrates transparent document grounding at small scale, but is not a production-scale document search solution.

The experience also showed that document quantity is not equivalent to usefulness. Many files contributed little to the intended PLC, SCADA, Industrial Automation or OT questions. A curated formal corpus is therefore methodologically stronger and computationally more realistic.

### Preliminary quality/latency observation

During pilot use, Cohere Command A+ appeared to produce more accurate and useful answers than Gemini 3.5 Flash-Lite, while Cohere was noticeably slower. This remains a pilot observation, not a final research conclusion. The formal 20-question x 2-model x 3-repetition benchmark must determine whether the pattern survives controlled scoring.

### Research-focus reflection

The project was initially intended to focus much more heavily on building the document-grounded engineering chatbot itself. Instructor/supervisor feedback clarified that implementation alone was insufficient for the Applied Research Project, so the artefact was reframed as an experimental instrument for empirical comparison. In retrospect, this change improved the academic value of the work because it forced implementation assumptions to be tested rather than merely demonstrated. The scalability failure at 883 PDFs is a good example: it is a limitation of the design, but also a meaningful applied-research result.

### Final frozen experiment

The final benchmark now contains 20 fixed questions: five PLC, five SCADA, five Industrial Automation and five Operational Technology questions. Each is to be run three times on both frozen models, producing 120 planned observations. The exact wording is stored in `TESTING_PROTOCOL.md`. Formal outputs must be preserved even when they contradict the pilot expectation.

### Remaining work

1. Freeze the small curated PDF corpus used for the formal benchmark.
2. Execute all 120 planned model responses or retain documented failures.
3. Save timestamped CSV evidence to Google Drive and keep a local backup.
4. Score every successful response using the frozen rubric.
5. Calculate the descriptive comparison and consistency results.
6. Replace provisional statements in the final IEEE paper and video script with measured numerical findings.
7. Complete the 4-5 minute video and final submission checks.

