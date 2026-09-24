import time
from datetime import datetime
from zoneinfo import ZoneInfo

import cohere
import pandas as pd
import streamlit as st

from google import genai

from google_drive import list_folder_files
from research_results import (
    add_result,
    get_results_dataframe,
    next_run_id,
    refresh_results,
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


def record_pilot_result(
    run_id,
    chatbot,
    provider,
    model_id,
    question,
    latency_seconds,
    response_text="",
    error_status="OK",
    error_message=""
):

    add_result(
        {
            "run_id": run_id,
            "test_id": "PILOT",
            "domain": "Pilot",
            "question": question,
            "source_reference": "",
            "chatbot": chatbot,
            "provider": provider,
            "model_id": model_id,
            "repetition": 1,
            "test_order": "",
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
                "Pilot/manual run - not part of the formal research dataset."
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
    <div class="Sheffield Hallam University theme disclaimer:">
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
                start_time = time.perf_counter()

                try:

                    gemini_key = st.secrets[
                        "GEMINI_API_KEY"
                    ]

                    client = genai.Client(
                        api_key=gemini_key
                    )

                    response = (
                        client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=question_a
                        )
                    )

                    latency = round(
                        time.perf_counter()
                        - start_time,
                        2
                    )

                    answer = response.text

                    record_pilot_result(
                        run_id=run_id,
                        chatbot="Chatbot A",
                        provider="Google",
                        model_id="gemini-3.5-flash-lite",
                        question=question_a,
                        latency_seconds=latency,
                        response_text=answer,
                    )

                    st.markdown("#### Response")

                    with st.chat_message("assistant"):
                        st.write(answer)

                    st.caption(
                        f"Observed response time: "
                        f"{latency:.2f} seconds. "
                        f"Recorded as {run_id}."
                    )

                except Exception as error:

                    latency = round(
                        time.perf_counter()
                        - start_time,
                        2
                    )

                    record_pilot_result(
                        run_id=run_id,
                        chatbot="Chatbot A",
                        provider="Google",
                        model_id="gemini-3.5-flash-lite",
                        question=question_a,
                        latency_seconds=latency,
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
                start_time = time.perf_counter()

                try:

                    cohere_key = st.secrets[
                        "COHERE_API_KEY"
                    ]

                    client = cohere.ClientV2(
                        api_key=cohere_key
                    )

                    response = client.chat(
                        model="command-a-plus-05-2026",
                        messages=[
                            {
                                "role": "user",
                                "content": question_b
                            }
                        ]
                    )

                    answer = ""

                    for content in (
                        response.message.content
                    ):

                        if content.type == "text":
                            answer = content.text

                    latency = round(
                        time.perf_counter()
                        - start_time,
                        2
                    )

                    if answer == "":

                        record_pilot_result(
                            run_id=run_id,
                            chatbot="Chatbot B",
                            provider="Cohere",
                            model_id=(
                                "command-a-plus-05-2026"
                            ),
                            question=question_b,
                            latency_seconds=latency,
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

                        record_pilot_result(
                            run_id=run_id,
                            chatbot="Chatbot B",
                            provider="Cohere",
                            model_id=(
                                "command-a-plus-05-2026"
                            ),
                            question=question_b,
                            latency_seconds=latency,
                            response_text=answer,
                        )

                        st.markdown("#### Response")

                        with st.chat_message(
                            "assistant"
                        ):
                            st.write(answer)

                        st.caption(
                            f"Observed response time: "
                            f"{latency:.2f} seconds. "
                            f"Recorded as {run_id}."
                        )

                except Exception as error:

                    latency = round(
                        time.perf_counter()
                        - start_time,
                        2
                    )

                    record_pilot_result(
                        run_id=run_id,
                        chatbot="Chatbot B",
                        provider="Cohere",
                        model_id=(
                            "command-a-plus-05-2026"
                        ),
                        question=question_b,
                        latency_seconds=latency,
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
        "research_data/results_template.csv. Current manual chatbot "
        "runs are marked PILOT because the shared document-grounding "
        "stage is not yet complete. PILOT rows must not be included "
        "in the final formal analysis."
    )

    st.caption(
        "Canonical dataset: research_data/results.csv "
        "on the GitHub research-data branch. "
        "The dashboard reads it automatically."
    )

    if (
        "GITHUB_RESULTS_TOKEN"
        in st.secrets
        and st.secrets[
            "GITHUB_RESULTS_TOKEN"
        ]
    ):
        st.success(
            "GitHub results persistence is configured."
        )
    else:
        st.warning(
            "GITHUB_RESULTS_TOKEN is not configured. "
            "Results can be viewed in this session but "
            "cannot yet be appended to the GitHub CSV."
        )

    if st.button(
        "Refresh results from GitHub",
        key="refresh_results_button"
    ):
        refresh_results()
        st.rerun()

    results = refresh_results()


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
                "Latency is the observed end-to-end "
                "response time measured by the "
                "Streamlit application."
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

            (
                _,
                scoring_saved,
                scoring_message,
            ) = save_edited_results(
                results
            )

            if scoring_saved:
                st.success(
                    f"Scoring saved to GitHub for "
                    f"{selected_run_id}."
                )
            else:
                st.warning(
                    "Scoring was updated in the current "
                    "session but could not be written to "
                    "GitHub: "
                    + scoring_message
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

        st.info(
            "The primary research record is the cumulative "
            "research_data/results.csv file on the GitHub "
            "research-data branch. Each chatbot run appends "
            "a new timestamped row. The download button is "
            "kept only for local backup/export."
        )

    with st.expander(
        "Google Drive document connection status"
    ):

        try:

            files = list_folder_files()

            st.success(
                f"Connected to Google Drive. "
                f"{len(files)} file(s) available."
            )

            for file in files:
                st.write(
                    f"- {file['name']}"
                )

        except Exception:

            st.error(
                "Google Drive connection could not "
                "be completed. Check the Streamlit "
                "Secrets, Drive API status and folder "
                "sharing permissions."
            )
