import time
from datetime import datetime
from zoneinfo import ZoneInfo

import cohere
import pandas as pd
import streamlit as st

from google import genai

from google_drive import (
    load_research_documents,
    upload_results_csv,
)
from document_retrieval import (
    build_grounded_prompt,
    retrieve_relevant_chunks,
    source_names,
    source_references,
)
from research_results import (
    add_result,
    get_results_dataframe,
    next_run_id,
    save_edited_results,
)


st.set_page_config(
    page_title="Applied Research Project - AI Chatbot Comparison",
    layout="centered"
)


def uk_timestamp():

    return datetime.now(
        ZoneInfo("Europe/London")
    ).isoformat(timespec="seconds")


@st.cache_data(
    ttl=600,
    show_spinner=False
)
def get_research_documents():

    return load_research_documents()


FROZEN_TESTS = {
    "What is a programmable logic controller (PLC), and what is its primary role in an industrial control system?": ("PLC-01", "PLC"),
    "Describe the typical PLC scan cycle and explain what happens during the input scan, program execution and output update stages.": ("PLC-02", "PLC"),
    "What is the difference between digital and analogue input/output signals in a PLC-based control system?": ("PLC-03", "PLC"),
    "What is the purpose of interlocks and permissives in PLC control logic?": ("PLC-04", "PLC"),
    "What is the difference between a standard PLC control function and a safety-related control function?": ("PLC-05", "PLC"),
    "What is a SCADA system, and what are its main functions in an industrial automation environment?": ("SCADA-01", "SCADA"),
    "How does a SCADA system typically communicate with PLCs or remote terminal units?": ("SCADA-02", "SCADA"),
    "What is the purpose of alarm management within a SCADA system?": ("SCADA-03", "SCADA"),
    "What is an industrial process historian, and how is it used with SCADA or control systems?": ("SCADA-04", "SCADA"),
    "What is the difference between an HMI and a SCADA system?": ("SCADA-05", "SCADA"),
    "What is the purpose of closed-loop control in an industrial automation system?": ("IA-01", "Industrial Automation"),
    "Explain the difference between open-loop and closed-loop control.": ("IA-02", "Industrial Automation"),
    "What is the purpose of a variable frequency drive (VFD) in an industrial automation system?": ("IA-03", "Industrial Automation"),
    "What role do industrial communication networks play in an automated control system?": ("IA-04", "Industrial Automation"),
    "What are Factory Acceptance Testing (FAT) and Site Acceptance Testing (SAT), and why are they carried out?": ("IA-05", "Industrial Automation"),
    "What is Operational Technology (OT), and how does it differ from traditional Information Technology (IT)?": ("OT-01", "Operational Technology"),
    "Why is network segmentation important in an industrial or OT environment?": ("OT-02", "Operational Technology"),
    "What is the principle of least privilege, and why is it important for access to industrial control systems?": ("OT-03", "Operational Technology"),
    "Why can software patching and system updates be more difficult in operational technology environments than in conventional IT environments?": ("OT-04", "Operational Technology"),
    "Why are backups and recovery procedures important for industrial control and OT systems?": ("OT-05", "Operational Technology"),
}


def normalise_question_text(text):

    return " ".join(
        text.strip().split()
    )


FROZEN_TEST_LOOKUP = {
    normalise_question_text(question): metadata
    for question, metadata in FROZEN_TESTS.items()
}


def get_run_metadata(
    question,
    chatbot
):

    metadata = FROZEN_TEST_LOOKUP.get(
        normalise_question_text(question)
    )

    if metadata is None:
        return {
            "test_id": "PILOT",
            "domain": "Pilot",
            "repetition": 1,
            "test_order": "",
            "qualitative_notes": (
                "Pilot/manual run - not part of "
                "the formal research dataset."
            ),
        }

    test_id, domain = metadata
    current_results = get_results_dataframe()

    same_test = current_results[
        current_results["test_id"] == test_id
    ]

    same_model = same_test[
        same_test["chatbot"] == chatbot
    ]

    repetition = len(same_model) + 1
    test_order = len(same_test) + 1

    if repetition <= 3:
        note = "Formal benchmark run."
    else:
        note = (
            "Extra formal attempt beyond the "
            "planned three repetitions."
        )

    return {
        "test_id": test_id,
        "domain": domain,
        "repetition": repetition,
        "test_order": test_order,
        "qualitative_notes": note,
    }


def record_result(
    run_id,
    chatbot,
    provider,
    model_id,
    question,
    latency_seconds,
    metadata,
    source_reference="",
    response_text="",
    error_status="OK",
    error_message=""
):

    add_result(
        {
            "run_id": run_id,
            "test_id": metadata["test_id"],
            "domain": metadata["domain"],
            "question": question,
            "source_reference": source_reference,
            "chatbot": chatbot,
            "provider": provider,
            "model_id": model_id,
            "repetition": metadata["repetition"],
            "test_order": metadata["test_order"],
            "timestamp_uk": uk_timestamp(),
            "latency_seconds": latency_seconds,
            "response_text": response_text,
            "correctness_0_2": "",
            "relevance_0_2": "",
            "faithfulness_0_2": "",
            "total_quality_0_6": "",
            "consistency_0_2": "",
            "error_status": error_status,
            "error_message": error_message,
            "retry_of_run_id": "",
            "qualitative_notes": (
                metadata["qualitative_notes"]
            ),
            "scored_by": "",
        }
    )


st.markdown(
    """
    <style>
        .shu-accent {
            display: flex;
            width: 100%;
            height: 8px;
            margin-bottom: 1.2rem;
            overflow: hidden;
            border-radius: 4px;
        }

        .shu-accent-maroon {
            width: 60%;
            background: #672146;
        }

        .shu-accent-crimson {
            width: 25%;
            background: #AC145A;
        }

        .shu-accent-pink {
            width: 15%;
            background: #E31C79;
        }

        .shu-kicker {
            color: #AC145A;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }

        .shu-theme-note {
            margin-top: 0.8rem;
            margin-bottom: 1rem;
            padding: 0.8rem 1rem;
            border-left: 4px solid #AC145A;
            background: #F7F5F6;
            color: #445063;
            line-height: 1.5;
        }
    </style>

    <div class="shu-accent">
        <div class="shu-accent-maroon"></div>
        <div class="shu-accent-crimson"></div>
        <div class="shu-accent-pink"></div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="shu-kicker">Academic Research</div>',
    unsafe_allow_html=True
)

st.title(
    "APPLIED RESEARCH PROJECT (CONT3 BF-2025/6) "
    "55-709708-BF-20256"
)

st.markdown(
    """
    <div class="shu-theme-note">
        The visual theme of this web application was inspired by
        Sheffield Hallam University's online websites and other
        media and materials.
    </div>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):

    st.subheader("Student Information")
    st.write("Name: Carlos Pizarro")
    st.write("Email: Carlos.Pizarro@student.shu.ac.uk")
    st.write("Student ID: 34046159")


st.subheader("Project Summary")

st.info(
    "This research prototype compares two large language model chatbot "
    "systems through the same Streamlit interface. The aim is to evaluate "
    "how the models respond to the same engineering questions under "
    "controlled conditions, providing both chatbots with the same "
    "research-safe documents and comparing measures such as response "
    "quality, groundedness, consistency and response time."
)

st.markdown(
    "How to use: Enter a relevant question in Chatbot A, for example "
    "'What is a PLC?', and submit it. Then open Chatbot B, enter the same "
    "question and submit it. The responses can then be compared under the "
    "same test conditions."
)

st.warning(
    "Disclaimer: This application is a non-commercial academic research "
    "prototype. It relies on third-party AI services, which remain subject "
    "to their own terms and conditions, availability, usage limits and "
    "policies."
)

st.divider()


tab_a, tab_b, tab_c = st.tabs(
    [
        "Chatbot A - Gemini",
        "Chatbot B - Cohere",
        "TESTS and METRICS",
    ]
)


with tab_a:

    st.subheader("Chatbot A")
    st.write("Provider: Google")
    st.write("Model: Gemini 3.5 Flash-Lite")
    st.write("Connection: Google GenAI API")
    st.success("Status: Operational")

    with st.container(border=True):

        question_a = st.text_input(
            "Engineering related question",
            placeholder="e.g. What is a PLC?",
            key="question_a"
        )

        if st.button(
            "Ask Chatbot A",
            type="primary",
            key="button_a"
        ):

            if question_a == "":
                st.warning("Please enter a question.")

            else:

                run_id = next_run_id()
                metadata_a = get_run_metadata(
                    question_a,
                    "Chatbot A"
                )
                start_time = None

                try:

                    (
                        research_documents,
                        skipped_documents,
                    ) = get_research_documents()

                    if not research_documents:
                        raise ValueError(
                            "No readable research documents "
                            "are available from Google Drive."
                        )

                    chunks_a = (
                        retrieve_relevant_chunks(
                            question_a,
                            research_documents
                        )
                    )

                    prompt_a = build_grounded_prompt(
                        question_a,
                        chunks_a
                    )

                    sources_a = ", ".join(
                        source_names(chunks_a)
                    )

                    source_refs_a = "; ".join(
                        source_references(chunks_a)
                    )

                    gemini_key = st.secrets[
                        "GEMINI_API_KEY"
                    ]

                    client = genai.Client(
                        api_key=gemini_key
                    )

                    start_time = time.perf_counter()

                    response = (
                        client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt_a
                        )
                    )

                    if start_time is not None:
                        latency = round(
                            time.perf_counter()
                            - start_time,
                            2
                        )
                    else:
                        latency = 0.0

                    answer = response.text

                    record_result(
                        run_id=run_id,
                        chatbot="Chatbot A",
                        provider="Google",
                        model_id="gemini-3.5-flash-lite",
                        question=question_a,
                        latency_seconds=latency,
                        metadata=metadata_a,
                        source_reference=source_refs_a,
                        response_text=answer,
                    )

                    st.markdown("#### Response")

                    with st.chat_message("assistant"):
                        st.write(answer)

                    st.caption(
                        f"Observed model response time: "
                        f"{latency:.2f} seconds. "
                        f"Recorded as {run_id}."
                    )

                    if sources_a:
                        st.caption(
                            "Document source(s): "
                            + sources_a
                        )
                    else:
                        st.caption(
                            "No relevant document passage "
                            "was retrieved for this question."
                        )

                except Exception as error:

                    if start_time is not None:
                        latency = round(
                            time.perf_counter()
                            - start_time,
                            2
                        )
                    else:
                        latency = 0.0

                    record_result(
                        run_id=run_id,
                        chatbot="Chatbot A",
                        provider="Google",
                        model_id="gemini-3.5-flash-lite",
                        question=question_a,
                        latency_seconds=latency,
                        metadata=metadata_a,
                        error_status="ERROR",
                        error_message=str(error),
                    )

                    st.error(error)


with tab_b:

    st.subheader("Chatbot B")
    st.write("Provider: Cohere")
    st.write("Model: Command A+")
    st.write(
        "Model ID: command-a-plus-05-2026"
    )
    st.write("Connection: Cohere Chat API")
    st.success("Status: Operational")

    with st.container(border=True):

        question_b = st.text_input(
            "Engineering related question",
            placeholder="e.g. What is a PLC?",
            key="question_b"
        )

        if st.button(
            "Ask Chatbot B",
            type="primary",
            key="button_b"
        ):

            if question_b == "":
                st.warning("Please enter a question.")

            else:

                run_id = next_run_id()
                metadata_b = get_run_metadata(
                    question_b,
                    "Chatbot B"
                )
                start_time = None

                try:

                    (
                        research_documents,
                        skipped_documents,
                    ) = get_research_documents()

                    if not research_documents:
                        raise ValueError(
                            "No readable research documents "
                            "are available from Google Drive."
                        )

                    chunks_b = (
                        retrieve_relevant_chunks(
                            question_b,
                            research_documents
                        )
                    )

                    prompt_b = build_grounded_prompt(
                        question_b,
                        chunks_b
                    )

                    sources_b = ", ".join(
                        source_names(chunks_b)
                    )

                    source_refs_b = "; ".join(
                        source_references(chunks_b)
                    )

                    cohere_key = st.secrets[
                        "COHERE_API_KEY"
                    ]

                    client = cohere.ClientV2(
                        api_key=cohere_key
                    )

                    start_time = time.perf_counter()

                    response = client.chat(
                        model="command-a-plus-05-2026",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt_b
                            }
                        ]
                    )

                    answer = ""

                    for content in (
                        response.message.content
                    ):

                        if content.type == "text":
                            answer = content.text

                    if start_time is not None:
                        latency = round(
                            time.perf_counter()
                            - start_time,
                            2
                        )
                    else:
                        latency = 0.0

                    if answer == "":

                        record_result(
                            run_id=run_id,
                            chatbot="Chatbot B",
                            provider="Cohere",
                            model_id=(
                                "command-a-plus-05-2026"
                            ),
                            question=question_b,
                            latency_seconds=latency,
                            metadata=metadata_b,
                            error_status="ERROR",
                            error_message=(
                                "No text response "
                                "was returned."
                            ),
                        )

                        st.error(
                            "No text response was returned."
                        )

                    else:

                        record_result(
                            run_id=run_id,
                            chatbot="Chatbot B",
                            provider="Cohere",
                            model_id=(
                                "command-a-plus-05-2026"
                            ),
                            question=question_b,
                            latency_seconds=latency,
                            metadata=metadata_b,
                            source_reference=source_refs_b,
                            response_text=answer,
                        )

                        st.markdown("#### Response")

                        with st.chat_message(
                            "assistant"
                        ):
                            st.write(answer)

                        st.caption(
                            f"Observed model response time: "
                            f"{latency:.2f} seconds. "
                            f"Recorded as {run_id}."
                        )

                        if sources_b:
                            st.caption(
                                "Document source(s): "
                                + sources_b
                            )
                        else:
                            st.caption(
                                "No relevant document passage "
                                "was retrieved for this question."
                            )

                except Exception as error:

                    if start_time is not None:
                        latency = round(
                            time.perf_counter()
                            - start_time,
                            2
                        )
                    else:
                        latency = 0.0

                    record_result(
                        run_id=run_id,
                        chatbot="Chatbot B",
                        provider="Cohere",
                        model_id=(
                            "command-a-plus-05-2026"
                        ),
                        question=question_b,
                        latency_seconds=latency,
                        metadata=metadata_b,
                        error_status="ERROR",
                        error_message=str(error),
                    )

                    st.error(error)


with tab_c:

    st.subheader(
        "Research Results and Metrics"
    )

    st.info(
        "This area records and visualises the results generated by "
        "the two chatbots using the same fields defined in "
        "research_data/results_template.csv. The chatbots now use "
        "the same Google Drive document corpus and the same retrieval "
        "method. The 20-question benchmark is now frozen. Exact "
        "matches to those questions are automatically recorded with "
        "their formal test ID, domain, repetition and run order; "
        "other questions remain marked PILOT."
    )

    st.caption(
        "Results are recorded in the current Streamlit session. "
        "Each chatbot run adds a new timestamped row. "
        "Save the session CSV to Google Drive and keep a local "
        "download as backup."
    )

    results = get_results_dataframe()


    if results.empty:

        st.info(
            "No chatbot results have been recorded "
            "in this session yet."
        )

    else:

        successful_results = results[
            results["error_status"] != "ERROR"
        ].copy()

        latency_values = pd.to_numeric(
            successful_results[
                "latency_seconds"
            ],
            errors="coerce"
        )

        total_runs = len(results)

        chatbot_a_runs = len(
            results[
                results["chatbot"]
                == "Chatbot A"
            ]
        )

        chatbot_b_runs = len(
            results[
                results["chatbot"]
                == "Chatbot B"
            ]
        )

        error_runs = len(
            results[
                results["error_status"]
                == "ERROR"
            ]
        )

        metric_1, metric_2, metric_3, metric_4 = (
            st.columns(4)
        )

        metric_1.metric(
            "Total runs",
            total_runs
        )

        metric_2.metric(
            "Chatbot A",
            chatbot_a_runs
        )

        metric_3.metric(
            "Chatbot B",
            chatbot_b_runs
        )

        metric_4.metric(
            "Errors",
            error_runs
        )

        st.markdown(
            "#### Observed Response Time"
        )

        latency_dataframe = (
            successful_results[
                ["chatbot", "latency_seconds"]
            ]
            .copy()
        )

        latency_dataframe[
            "latency_seconds"
        ] = pd.to_numeric(
            latency_dataframe[
                "latency_seconds"
            ],
            errors="coerce"
        )

        latency_summary = (
            latency_dataframe
            .dropna()
            .groupby("chatbot")[
                "latency_seconds"
            ]
            .mean()
            .rename("Mean latency (seconds)")
        )

        if not latency_summary.empty:

            st.bar_chart(
                latency_summary
            )

        if not latency_values.dropna().empty:

            st.caption(
                "Latency is the observed model/API "
                "response time measured after shared "
                "document retrieval has completed."
            )

        st.markdown(
            "#### Score a Recorded Response"
        )

        selected_run_id = st.selectbox(
            "Select result",
            results["run_id"].tolist(),
            key="score_run_id"
        )

        selected_index = (
            results.index[
                results["run_id"]
                == selected_run_id
            ][0]
        )

        selected_result = (
            results.loc[selected_index]
        )

        st.write(
            f"**Chatbot:** "
            f"{selected_result['chatbot']}"
        )

        st.write(
            f"**Question:** "
            f"{selected_result['question']}"
        )

        st.write(
            f"**Observed latency:** "
            f"{selected_result['latency_seconds']} "
            "seconds"
        )

        st.markdown("**Recorded response:**")

        with st.container(border=True):
            st.write(
                selected_result[
                    "response_text"
                ]
                if selected_result[
                    "response_text"
                ]
                else "No response text recorded."
            )

        score_options = [
            "Not scored",
            0,
            1,
            2,
        ]

        def score_index(value):

            try:
                number = int(float(value))
                return score_options.index(
                    number
                )
            except Exception:
                return 0

        score_col_1, score_col_2 = (
            st.columns(2)
        )

        with score_col_1:

            correctness = st.selectbox(
                "Correctness (0-2)",
                score_options,
                index=score_index(
                    selected_result[
                        "correctness_0_2"
                    ]
                ),
                key=(
                    "score_correctness_"
                    + selected_run_id
                )
            )

            relevance = st.selectbox(
                "Relevance (0-2)",
                score_options,
                index=score_index(
                    selected_result[
                        "relevance_0_2"
                    ]
                ),
                key=(
                    "score_relevance_"
                    + selected_run_id
                )
            )

        with score_col_2:

            faithfulness = st.selectbox(
                "Faithfulness (0-2)",
                score_options,
                index=score_index(
                    selected_result[
                        "faithfulness_0_2"
                    ]
                ),
                key=(
                    "score_faithfulness_"
                    + selected_run_id
                )
            )

            consistency = st.selectbox(
                "Consistency (0-2)",
                score_options,
                index=score_index(
                    selected_result[
                        "consistency_0_2"
                    ]
                ),
                key=(
                    "score_consistency_"
                    + selected_run_id
                )
            )

        qualitative_notes = st.text_area(
            "Qualitative notes",
            value=str(
                selected_result[
                    "qualitative_notes"
                ]
            ),
            key=(
                "score_notes_"
                + selected_run_id
            )
        )

        scored_by = st.text_input(
            "Scored by",
            value=str(
                selected_result[
                    "scored_by"
                ]
            ),
            key=(
                "score_name_"
                + selected_run_id
            )
        )

        if st.button(
            "Save scoring",
            key="save_scoring_button"
        ):

            results.at[
                selected_index,
                "correctness_0_2"
            ] = (
                ""
                if correctness
                == "Not scored"
                else correctness
            )

            results.at[
                selected_index,
                "relevance_0_2"
            ] = (
                ""
                if relevance
                == "Not scored"
                else relevance
            )

            results.at[
                selected_index,
                "faithfulness_0_2"
            ] = (
                ""
                if faithfulness
                == "Not scored"
                else faithfulness
            )

            results.at[
                selected_index,
                "consistency_0_2"
            ] = (
                ""
                if consistency
                == "Not scored"
                else consistency
            )

            results.at[
                selected_index,
                "qualitative_notes"
            ] = qualitative_notes

            results.at[
                selected_index,
                "scored_by"
            ] = scored_by

            save_edited_results(
                results
            )

            st.success(
                f"Scoring saved for "
                f"{selected_run_id}."
            )

            st.rerun()

        scored_results = (
            get_results_dataframe()
        )

        for score_column in [
            "correctness_0_2",
            "relevance_0_2",
            "faithfulness_0_2",
            "total_quality_0_6",
            "consistency_0_2",
        ]:

            scored_results[
                score_column
            ] = pd.to_numeric(
                scored_results[
                    score_column
                ],
                errors="coerce"
            )

        score_summary = (
            scored_results
            .groupby("chatbot")[
                [
                    "correctness_0_2",
                    "relevance_0_2",
                    "faithfulness_0_2",
                ]
            ]
            .mean()
            .dropna(how="all")
        )

        if not score_summary.empty:

            st.markdown(
                "#### Mean Quality Scores"
            )

            score_summary.columns = [
                "Correctness",
                "Relevance",
                "Faithfulness",
            ]

            st.bar_chart(
                score_summary
            )

        st.markdown(
            "#### Recorded Results"
        )

        st.dataframe(
            scored_results,
            use_container_width=True
        )

        csv_data = (
            scored_results
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            "Download research results CSV",
            data=csv_data,
            file_name=(
                "chatbot_research_results.csv"
            ),
            mime="text/csv",
            key="download_results"
        )

        if st.button(
            "Save session to Google Drive",
            key="save_session_drive"
        ):

            try:

                session_timestamp = (
                    datetime.now(
                        ZoneInfo("Europe/London")
                    )
                    .strftime("%Y%m%d_%H%M%S")
                )

                session_file_name = (
                    "research_results_"
                    + session_timestamp
                    + ".csv"
                )

                uploaded_file = (
                    upload_results_csv(
                        csv_data,
                        session_file_name
                    )
                )

                st.success(
                    "Session saved to Google Drive as "
                    + uploaded_file["name"]
                    + "."
                )

                st.caption(
                    "Google Drive file ID: "
                    + uploaded_file["id"]
                )

            except Exception as error:

                st.error(
                    "The session could not be saved "
                    "to Google Drive: "
                    + str(error)
                )

        st.info(
            "Results remain in the current Streamlit "
            "session while the app is open. Save a "
            "timestamped session CSV to Google Drive "
            "for persistent research evidence, and "
            "use the download button for a local backup."
        )

    with st.expander(
        "Google Drive document connection status"
    ):

        st.caption(
            "Drive files are loaded only when needed "
            "so they do not delay the main interface."
        )

        if st.button(
            "Check Google Drive documents",
            key="check_drive_documents"
        ):

            try:

                (
                    research_documents,
                    skipped_documents,
                ) = get_research_documents()

                st.success(
                    f"{len(research_documents)} readable "
                    "document(s) loaded."
                )

                for document in research_documents:
                    st.write(
                        f"- {document['name']}"
                    )

                if skipped_documents:
                    st.caption(
                        "Skipped unsupported or unreadable "
                        "files: "
                        + ", ".join(
                            skipped_documents
                        )
                    )

            except Exception as error:

                st.error(
                    "Google Drive connection could not "
                    "be completed: "
                    + str(error)
                )
