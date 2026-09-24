from pathlib import Path

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


RESULTS_FILE = Path(
    "research_data/results.csv"
)


def read_repository_results():

    if not RESULTS_FILE.exists():
        return pd.DataFrame(
            columns=RESULT_COLUMNS
        )

    try:
        dataframe = pd.read_csv(
            RESULTS_FILE,
            dtype=str,
            keep_default_na=False
        )
    except pd.errors.EmptyDataError:
        return pd.DataFrame(
            columns=RESULT_COLUMNS
        )

    missing_columns = [
        column
        for column in RESULT_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        return pd.DataFrame(
            columns=RESULT_COLUMNS
        )

    return dataframe[
        RESULT_COLUMNS
    ].copy()


def initialise_results():

    if "research_results" not in st.session_state:

        dataframe = read_repository_results()

        st.session_state[
            "research_results"
        ] = dataframe.to_dict(
            orient="records"
        )


def next_run_id():

    initialise_results()

    highest_run_number = 0

    for result in st.session_state[
        "research_results"
    ]:

        run_id = str(
            result.get("run_id", "")
        )

        if run_id.startswith("RUN-"):

            try:
                run_number = int(
                    run_id.replace(
                        "RUN-",
                        ""
                    )
                )

                highest_run_number = max(
                    highest_run_number,
                    run_number
                )

            except ValueError:
                pass

    return (
        f"RUN-{highest_run_number + 1:04d}"
    )


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
