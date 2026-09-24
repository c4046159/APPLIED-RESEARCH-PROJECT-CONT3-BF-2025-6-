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

### Scope decision - reduce final comparison from three chatbots to two

- The original implementation plan considered three chatbot systems.
- Repeated provider-access, rate-limit and free-endpoint reliability problems showed that maintaining three independent no-payment cloud providers would add substantial operational risk to the experiment.
- The project scope has therefore been deliberately reduced to two final chatbot systems: Chatbot A and Chatbot B.
- This is a research-driven scope reduction rather than a removal of the comparison itself. Two independent systems are sufficient to perform a controlled comparative study while allowing more time for repeated trials, shared document retrieval, response-time measurement, answer scoring and analysis.
- The change also improves reproducibility by avoiding a third provider whose availability could prevent completion of the planned test set.
- Chatbot C is no longer planned for the final implementation.

### Chatbot B moved to Cohere

- Cohere was selected as the next Chatbot B candidate because its trial API key has published limits suitable for prototyping and repeated testing.
- Cohere currently documents a 20 requests/minute Chat limit for trial keys and a 1,000 API calls/month trial allowance.
- `command-a-plus-05-2026` is being used because it is a current live Command model and Cohere documents it as free for trial-key usage until trial rate limits are reached.
- The implementation uses the official `cohere` Python SDK, `ClientV2`, and the Chat API.
- Commit `703f0ea` replaces the Mistral dependency with Cohere.
- Commit `11191c2` changes Chatbot B to Cohere Command A+.

### Cohere validation - structured response parsing issue

- The validation prompt `What is a PLC?` successfully reached Cohere and produced a structured assistant response.
- The initial code attempted to read `response.message.content[0].text`.
- Command A+ can return a `thinking` block before the final `text` block, so the first returned item was a `ThinkingAssistantMessageResponseContentItem` rather than a text item.
- Streamlit therefore displayed: `'ThinkingAssistantMessageResponseContentItem' object has no attribute 'text'`.
- This is not an authentication, quota or provider-availability failure. It confirms that Cohere responded, but the response parser made an incorrect assumption about item order.
- The parsing code was changed to loop through `response.message.content` and select the item where `content.type == "text"`.
- Commit `0ba34a2` records this fix (`Fix Cohere response parsing for thinking and text blocks`).

### Cohere validation - successful end-to-end result

- The corrected parser was retested using the same validation prompt: `What is a PLC?`.
- Chatbot B returned and displayed the expected natural-language response successfully in the deployed Streamlit application.
- This confirms the full Chatbot B path is operational: Streamlit -> Cohere API -> Command A+ -> structured response -> text extraction -> browser display.
- Result: PASS for end-to-end Chatbot B operation.
- Gemini and Cohere are now frozen as the two final chatbot systems for the comparative experiment.
- No Chatbot C will be implemented.

### Reflection from the incremental build

The extension showed that adding a second model is not only a coding problem. Authentication, provider availability, free-tier quotas, structured API responses and upstream service reliability are practical constraints that can directly affect the feasibility and reproducibility of an empirical chatbot comparison. The failed provider trials and parsing correction are therefore retained as development and validation evidence rather than removed from the record.

The provider problems also caused a useful methodological refinement. The final study will compare two stable chatbot systems rather than three less reliable systems. This keeps the core comparative research question intact while reducing external-provider risk and creating more capacity for systematic repeated testing and analysis.

The successful Cohere retest closes this incremental build cycle with both final chatbot providers operational.

## 13 September 2026 - User interface refinement

- The Streamlit interface was polished after both final model integrations had been frozen.
- The page now displays the formal module title `APPLIED RESEARCH PROJECT (CONT3 BF-2025/6)` and module code `55-709708-BF-20256`.
- Student identification information was added to the prototype as requested.
- A short project overview and usage explanation were added so that supervisors, markers and other users can understand the purpose of the prototype and how to run a simple A-versus-B comparison.
- A non-commercial academic research disclaimer was added. It explains that the prototype depends on third-party AI services and remains subject to their individual terms, availability, usage limits and policies, and that the project is not operated for commercial profit.
- Basic provider/model information and operational status are displayed consistently for both Chatbot A and Chatbot B.
- Each interaction area is grouped inside a bordered Streamlit container.
- Model outputs are now displayed using Streamlit's native assistant chat-message presentation rather than plain text output.
- The underlying Gemini and Cohere API calls were deliberately left unchanged so that this presentation refinement does not alter the validated experimental provider configuration.
- Commit `0ecdcf7` records the interface update (`Polish research prototype interface and add project information`).

## 13 September 2026 - Sheffield Hallam inspired visual theme

- The Sheffield Hallam Online website (`online.shu.ac.uk`) and the University's publicly available brand guidance were reviewed as visual inspiration for the prototype.
- Browser-inspected CSS supplied during development showed a 16px/1rem body-text scale, approximately 1.5 line-height, sans-serif typography and body text colour around `#445063`.
- The University's current public brand guidance was used to identify Hallam Maroon (`#672146`), Collegiate Crimson (`#AC145A`), Hallam Pink (`#E31C79`) and HUBS Silver (`#D0D3D4`) as suitable interface colours.
- Generic WordPress preset gradients, Tailwind variables and browser-reset rules found in the inspected CSS were deliberately excluded because they are implementation scaffolding rather than meaningful Sheffield Hallam visual identity.
- Meta Pro was identified as Sheffield Hallam's primary typeface, but it is proprietary. The prototype does not copy, embed or redistribute that font; a standard sans-serif configuration is used instead, consistent with the University's published fallback guidance.
- A project-level `.streamlit/config.toml` was added to apply the colour palette, 16px base scale, light surfaces, visible borders and restrained corner radii.
- The application header now includes a simple three-part Hallam-colour accent strip, and the primary chatbot buttons use the Hallam Maroon theme colour.
- The interface contains a visible attribution stating that its theme is inspired by Sheffield Hallam's online site and public brand guidance and that the application is an independent student research prototype rather than an official University digital service.
- A dedicated `UI_THEME_NOTES.md` file records the design sources, extracted values, implementation choices, exclusions and accessibility rationale.
- Commits `2b43615`, `c9b9a7b` and `bb72876` record the theme configuration, application treatment and theme documentation respectively.

## Current prototype status

- Chatbot A: Google Gemini 3.5 Flash-Lite - working and frozen for the experiment.
- Chatbot B: Cohere Command A+ - working and frozen for the experiment.
- Chatbot C: removed from final scope.
- Final comparison scope: two chatbot systems.
- User interface: research/module identity, student information, instructions, disclaimer, model information, bordered input areas and chat-style response display added.
- Visual theme: Sheffield Hallam inspired, with provenance and limitations documented separately in `UI_THEME_NOTES.md`.
- Next implementation milestone: shared research-safe engineering-document source for both chatbots, followed by controlled response-time and answer-quality testing.


## 24 September 2026 - Google Drive research-document connection

- Work began on connecting the frozen two-chatbot prototype to the shared research-safe Google Drive document source.
- The project dependencies were extended with the Google Drive API/authentication packages and the planned PDF/DOCX extraction libraries: `google-api-python-client`, `google-auth`, `google-auth-httplib2`, `pypdf` and `python-docx`.
- A new `google_drive.py` module was created using a Google service account and the read-only scope `https://www.googleapis.com/auth/drive.readonly`.
- The module reads the service-account credentials from the Streamlit `gcp_service_account` secret and the target folder from `GOOGLE_DRIVE_FOLDER_ID`.
- A `list_folder_files()` function was implemented to query the configured folder and return file ID, filename and MIME type.
- The folder-listing query was refined to ignore deleted items and subfolders, sort results by filename and limit the initial research-folder listing to 100 files.
- The initial Streamlit integration contained a stale `drive_reader` import as well as the new `google_drive` import. This duplication could prevent the application from starting because `drive_reader.py` does not form part of the current implementation.
- The stale import was removed so the application now uses `google_drive.py` as the single Drive integration module.
- The Drive folder query was also moved out of the top-level application startup path. A Drive configuration or permission problem will therefore no longer prevent the Gemini and Cohere tabs from loading.
- The existing `TESTS and METRICS` tab is now used to validate the Drive connection and list the research documents available to the prototype.
- The interface explicitly states that this stage validates Drive access only. The listed files are not yet being supplied to either chatbot.
- The frozen visual design and the frozen Gemini/Cohere provider configuration were preserved. These changes are functional additions required by the research method rather than aesthetic redesign.
- Relevant commits include `7485526` (harden Drive folder listing), `48ec82a` (add Drive status to tests tab) and `2fb414d` (remove stale Drive import and defer the Drive check to the tests tab).

### Current Drive milestone status

- Google Drive service-account integration: implemented in code.
- Research-folder file listing: implemented in code.
- Deployed connection/permissions: must be confirmed in Streamlit using the configured secrets and shared-folder permissions.
- PDF/DOCX/TXT/Google Docs text extraction: not yet implemented.
- Common chunking/retrieval: not yet implemented.
- Supplying identical document context to Gemini and Cohere: not yet implemented.
- Formal experimental data collection: must not begin until the shared document-grounding path is complete and validated.


## 24 September 2026 - Research results capture and metrics dashboard

- The purpose of the existing `TESTS and METRICS` tab was clarified: it is the research-results area for recording, reviewing and visualising chatbot performance rather than primarily a Google Drive status page.
- A new `research_results.py` module was added using the exact field structure already defined in `research_data/results_template.csv`.
- Each successful or failed chatbot call now records a result row containing the run ID, chatbot/provider/model, question, timestamp, observed end-to-end latency, full response text, error status and error message.
- Current manual chatbot interactions are deliberately labelled `PILOT` and `Pilot` in the test/domain fields. These rows validate the recording workflow but must not be included in the final formal analysis because shared document grounding and the fixed formal question set are not yet complete.
- Correctness, relevance, faithfulness, consistency, qualitative notes and scorer identity are not generated automatically. They are entered manually in the results tab so that evaluation remains transparent and based on the documented rubric/reference answers rather than self-scoring by the tested systems.
- The application automatically calculates `total_quality_0_6` only when correctness, relevance and faithfulness have all been scored.
- The results dashboard now shows run counts, error counts, mean observed response-time comparison and mean correctness/relevance/faithfulness scores when scoring data is available.
- The full recorded dataset is displayed in the application and can be exported using the same CSV field structure as `results_template.csv`.
- A previously exported research-results CSV can be loaded back into the dashboard for continued review.
- The Google Drive connection check remains available as a secondary expandable technical-status section rather than occupying the primary metrics view.
- Research results are currently stored in Streamlit session state while the app is running. Because Streamlit session state is not durable research storage, the interface explicitly requires the CSV to be downloaded at the end of each testing session. Durable automatic storage in the research Google Drive folder can be added later once a deliberate write-access design is approved.
- `pandas` was added as an explicit project dependency for CSV handling and descriptive result summaries.
- Relevant commits include `418f230` (research results helpers), `aa11c7f` (pandas dependency) and `10558b2` (automatic run capture and research metrics dashboard).


## 24 September 2026 - Cumulative GitHub results dataset

- The research-results workflow was refined so that `research_data/results.csv` is the single cumulative dataset used by the application.
- The manual CSV upload workflow was removed from the `TESTS and METRICS` tab.
- A dedicated GitHub branch named `research-data` was created for the cumulative results file. This prevents every recorded chatbot response from changing the deployed `main` branch and triggering unnecessary Streamlit redeployments during repeated testing.
- The dashboard now reads `research_data/results.csv` directly from the `research-data` branch using the GitHub Contents API.
- Every chatbot run appends one new row to the cumulative CSV. The row includes a unique run ID, UK timestamp, chatbot/provider/model, exact question, observed latency, full raw response text and any error information.
- Normal result capture is append-only: previous raw responses and timestamps are not replaced when new runs are recorded.
- Manual evaluation later updates only the scoring/interpretation fields for the matching `run_id`: correctness, relevance, faithfulness, calculated total quality, consistency, qualitative notes and scorer identity.
- Sequential run IDs continue from the highest existing `RUN-xxxx` identifier in the cumulative GitHub dataset.
- The results dashboard provides a refresh control that reloads the canonical dataset directly from GitHub and no longer requires the user to upload a file.
- A local CSV download remains available only as a backup/export mechanism; it is not the primary source of truth.
- The deployed Streamlit application requires a `GITHUB_RESULTS_TOKEN` secret to write to the cumulative dataset. This token should be a fine-grained GitHub token restricted to this repository with Contents read/write permission and should never be committed to the repository.
- The `research-data` branch is intentionally separate from `main` so repeated experimental data commits do not repeatedly redeploy the application.
- Relevant commits include `7e15f5e` (canonical results file), `6735b9c` (automatic repository loading), `800a7ba` (persistent cumulative GitHub storage), `aad9a84` (persistence failure warning), `42f1f8e` (GitHub HTTP dependency) and `415c9e3` (automatic dashboard loading with no upload control).
