# Formal Chatbot Testing Protocol

Date established: 13 September 2026
Module: APPLIED RESEARCH PROJECT (CONT3 BF-2025/6) - 55-709708-BF-20256

## 1. Purpose

This protocol converts the submitted formative research proposal into a repeatable test procedure for the final two-chatbot experiment.

The submitted proposal requires a controlled technical question set derived from an engineering document corpus, expected answers or source passages, execution of the same questions, recording of responses and response times, and comparison using correctness, relevance, faithfulness, consistency and latency.

The final prototype scope has subsequently been reduced from several candidate chatbots to two validated systems for feasibility and reproducibility:

- Chatbot A: Google Gemini 3.5 Flash-Lite
- Chatbot B: Cohere Command A+ (`command-a-plus-05-2026`)

The provider/model choices and the user-interface design are frozen before formal data collection.

## 2. Important distinction: pilot testing versus formal testing

Current connectivity checks such as `What is a PLC?` are pilot/validation tests only.

Formal research data must not be collected until both chatbots receive the same retrieved context from the same approved engineering document corpus. This is necessary because the submitted research questions concern document-grounded answers and faithfulness to supplied documentation.

## 3. Formal benchmark size

The submitted proposal specifies a restricted controlled test set but does not prescribe a number of questions. For implementation, the initial formal benchmark will use 20 questions:

- 5 PLC questions
- 5 SCADA questions
- 5 Industrial Automation questions
- 5 Operational Technology (OT) questions

Each question will be executed three times on each chatbot to assess output consistency.

Total planned formal responses:

20 questions x 2 chatbots x 3 repetitions = 120 responses.

This size is deliberately restricted so the study remains feasible while still producing repeated observations for each question/model combination.

## 4. Preparing the document corpus

Before creating test questions:

1. Select only research-safe engineering documents that the researcher is authorised to use.
2. Remove confidential, client-identifying, credential, security-sensitive or operationally sensitive information.
3. Store the approved corpus in the final shared document source.
4. Record the document filename, section/page and version/date where practical.
5. Do not change the formal document corpus after formal data collection begins unless the experiment is restarted and the change is documented.

## 5. Creating the controlled question set

For each of the 20 questions:

1. Derive the question directly from the approved document corpus.
2. Assign a unique test ID, for example `PLC-01` or `SCADA-03`.
3. Record the domain.
4. Record the exact wording of the question.
5. Record the source document and page/section.
6. Write an expected answer as a short set of essential facts or key points.
7. Copy or summarise the relevant reference passage from the source document.
8. Give the question a simple type label such as factual, interpretation, troubleshooting, application or safety/limitation.
9. Do not create questions whose answer is absent from the supplied corpus unless the deliberate purpose is to test whether the chatbot correctly admits that the answer is not available.

The expected answer should focus on required facts rather than exact wording. This avoids unfairly penalising a correct answer simply because it is phrased differently.

## 6. Freeze the experimental conditions

Immediately before formal testing, record:

- Date and time testing begins.
- Chatbot A provider and model ID.
- Chatbot B provider and model ID.
- Streamlit application commit/version.
- Document corpus version.
- Retrieval method/version.
- Shared system/instruction prompt.
- Temperature or generation settings where configurable.
- Maximum response/token settings where configurable.
- Number of retrieved chunks/passages supplied to each model.

Both systems must receive the same question and the same retrieved document context for a given test run.

Do not modify prompts, retrieval rules, scoring criteria or model selections during the formal run.



## 6A. Shared document retrieval implementation

The final prototype uses one retrieval method for both chatbot systems. This is deliberately implemented in the Streamlit application rather than using provider-specific retrieval services.

The current fixed retrieval configuration is:

- Supported document formats: PDF, DOCX, TXT, Markdown and native Google Docs.
- Google Drive access: service account with read-only Drive scope.
- Google Docs are exported as plain text before processing.
- PDF text is extracted with `pypdf`.
- DOCX text is extracted with `python-docx`.
- TXT/Markdown content is decoded as UTF-8 text.
- Each document is divided into fixed chunks of 180 words.
- Consecutive chunks overlap by 30 words.
- Query and chunk text are reduced to lowercase alphanumeric terms with a small set of common stop words removed.
- Relevance is calculated as the number of unique query terms that also occur in a chunk.
- Only chunks with a score greater than zero are considered relevant.
- The top four chunks are selected using the same deterministic ranking rule for both models.
- Ties are resolved by source filename and chunk number so repeated retrieval is deterministic.
- The selected passages are inserted into one common grounded prompt.
- Both models are instructed to use only the supplied document context and to state that the information is not available in the provided documentation when the context does not support an answer.
- Source filenames used for a response are recorded in the result row.

These settings must remain unchanged during formal data collection. Any later change to chunk size, overlap, stop-word handling, number of retrieved chunks or prompt wording requires a documented new experiment/version rather than being mixed with existing formal results.

## 7. Step-by-step execution procedure

For each test question:

1. Open the deployed Streamlit prototype.
2. Confirm both chatbot status indicators are operational.
3. Locate the question in `research_data/test_questions_template.csv` or its completed successor.
4. Copy the exact question text. Do not paraphrase it between models or repetitions.
5. Run the question on the first chatbot.
6. Record the complete response exactly as returned.
7. Record the measured end-to-end response time in seconds.
8. Record whether an API/provider/application error occurred.
9. Run the exact same question on the second chatbot using the same document-grounding conditions.
10. Record its response and response time.
11. Repeat until each chatbot has produced three responses for that question.
12. Move to the next question.

To reduce systematic timing bias, alternate which chatbot is tested first:

- Odd-numbered questions: A then B.
- Even-numbered questions: B then A.

Use independent prompts with no conversation history carried between questions.

## 8. Manual scoring rubric

Each individual response is scored after it has been recorded. The scorer should compare the response against the expected answer and reference passage, not against the other chatbot.

### Correctness - 0 to 2

- 0 = materially incorrect or fails to answer.
- 1 = partly correct but incomplete or contains a significant error.
- 2 = correct on the essential facts required by the reference answer.

### Relevance - 0 to 2

- 0 = off-topic or mostly irrelevant.
- 1 = partly relevant but includes substantial unnecessary or distracting material.
- 2 = directly addresses the question with appropriate technical focus.

### Faithfulness - 0 to 2

- 0 = contradicts the supplied documents or invents important unsupported facts.
- 1 = mostly supported but contains a minor unsupported claim, overstatement or ambiguity.
- 2 = all important claims are supported by the supplied document context.

### Per-response quality score

Correctness + Relevance + Faithfulness = maximum 6 points.

This total is useful for summary comparison, but the three component scores must also be retained separately so weaknesses are not hidden by a single total.

## 9. Consistency scoring

Consistency is evaluated after the three repetitions of the same question/model have been collected.

### Consistency - 0 to 2

- 0 = important factual contradictions or materially different conclusions across repetitions.
- 1 = noticeable differences in completeness/detail but the main conclusion remains broadly similar.
- 2 = substantively consistent essential facts and conclusion across all three repetitions.

The consistency score is assigned once per question/model group and may be repeated in the result rows or stored in a later summary table.

## 10. Latency

Latency is the observed end-to-end time from submitting the question in the Streamlit application to receiving the displayed answer.

Record latency in seconds to at least two decimal places where automated timing allows.

Latency must be described in the report as observed end-to-end response time. It includes network, provider routing and application overhead and therefore should not be presented as pure model inference speed.

## 11. Error recording

Do not delete failed runs.

For every failure record:

- HTTP/API error where visible.
- Provider error message.
- Timeout.
- Empty response.
- Parsing/application error.
- Whether a retry was performed.

A failed formal run remains part of the reliability evidence. If a retry is necessary, create a new result row rather than replacing the failed row.

## 12. Qualitative notes

The submitted proposal permits limited qualitative analysis of incorrect or problematic responses.

Use the notes field for observations such as:

- hallucinated technical detail;
- unsupported safety statement;
- omitted essential fact;
- over-confident wording;
- correct refusal when the document corpus does not contain the answer;
- unusually clear or useful explanation;
- contradiction between repetitions.

These notes support interpretation but do not replace the numeric scoring rubric.

## 13. Results recording

Raw test outputs will be recorded in `research_data/results_template.csv` or a generated results file with the same fields.

The minimum fields are:

- test ID;
- domain;
- exact question;
- source reference;
- chatbot/model;
- repetition number;
- timestamp;
- latency;
- full response text;
- correctness score;
- relevance score;
- faithfulness score;
- total quality score;
- consistency score;
- error status;
- notes.

Raw responses must be retained before analysis. Do not overwrite them with edited or shortened versions.

## 14. Analysis after testing

For each chatbot calculate:

- mean correctness score;
- mean relevance score;
- mean faithfulness score;
- mean total quality score;
- mean and median latency;
- number and percentage of failed/error runs;
- mean consistency score.

Also compare results by domain: PLC, SCADA, Industrial Automation and OT.

Present the results using descriptive statistics, tables and charts, as specified in the submitted proposal.

Qualitatively review the most important incorrect, unsupported or inconsistent answers to explain what the numeric results mean.

## 15. Formal test completion rule

The experiment is complete when:

- all 20 test questions have been executed three times on each frozen chatbot;
- all 120 planned responses or documented failures are present in the raw results;
- each successful response has been scored using the same rubric;
- consistency has been assessed for every question/model combination;
- summary statistics have been calculated without deleting inconvenient results.

## 16. Research integrity

The testing procedure is designed to preserve the submitted proposal's principles of controlled prompts, documented configurations and repeatable procedures. The same evidence must be retained even when it shows poor performance, errors or results contrary to expectations.