import pandas as pd
import streamlit as st


RESULT_COLUMNS = [
    "run_id",
    "test_id",
    "domain",
    "question",
    "source_reference",
    "chatbot",
    "provider",
    "model_id",
    "repetition",
    "test_order",
    "timestamp_uk",
    "latency_seconds",
    "response_text",
    "correctness_0_2",
    "relevance_0_2",
    "faithfulness_0_2",
    "total_quality_0_6",
    "consistency_0_2",
    "error_status",
    "error_message",
    "retry_of_run_id",
    "qualitative_notes",
    "scored_by",
]


def initialise_results():

    if "research_results" not in st.session_state:
        st.session_state["research_results"] = []


def next_run_id():

    initialise_results()

    run_number = (
        len(st.session_state["research_results"])
        + 1
    )

    return f"RUN-{run_number:04d}"


def add_result(result):

    initialise_results()

    complete_result = {}

    for column in RESULT_COLUMNS:
        complete_result[column] = (
            result.get(column, "")
        )

    st.session_state[
        "research_results"
    ].append(
        complete_result
    )


def get_results_dataframe():

    initialise_results()

    return pd.DataFrame(
        st.session_state[
            "research_results"
        ],
        columns=RESULT_COLUMNS
    )


def save_edited_results(dataframe):

    dataframe = dataframe.copy()

    score_columns = [
        "correctness_0_2",
        "relevance_0_2",
        "faithfulness_0_2",
    ]

    for column in score_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    dataframe[
        "total_quality_0_6"
    ] = (
        dataframe[
            score_columns
        ]
        .sum(
            axis=1,
            min_count=3
        )
    )

    clean_dataframe = dataframe.where(
        pd.notna(dataframe),
        ""
    )

    st.session_state[
        "research_results"
    ] = (
        clean_dataframe
        .to_dict(
            orient="records"
        )
    )

    return clean_dataframe
