import base64
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
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

GITHUB_REPOSITORY = (
    "c4046159/"
    "APPLIED-RESEARCH-PROJECT-CONT3-BF-2025-6-"
)

GITHUB_RESULTS_BRANCH = "research-data"

GITHUB_RESULTS_PATH = (
    "research_data/results.csv"
)


def github_headers():

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if "GITHUB_RESULTS_TOKEN" in st.secrets:

        token = st.secrets[
            "GITHUB_RESULTS_TOKEN"
        ]

        if token:
            headers["Authorization"] = (
                f"Bearer {token}"
            )

    return headers


def github_results_url():

    return (
        "https://api.github.com/repos/"
        f"{GITHUB_REPOSITORY}/contents/"
        f"{GITHUB_RESULTS_PATH}"
    )


def fetch_github_results_file():

    response = requests.get(
        github_results_url(),
        headers=github_headers(),
        params={
            "ref": GITHUB_RESULTS_BRANCH
        },
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    csv_text = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    return csv_text, data["sha"]


def dataframe_from_csv_text(csv_text):

    if not csv_text.strip():
        return pd.DataFrame(
            columns=RESULT_COLUMNS
        )

    try:

        dataframe = pd.read_csv(
            StringIO(csv_text),
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


def read_repository_results():

    try:

        csv_text, _ = (
            fetch_github_results_file()
        )

        return dataframe_from_csv_text(
            csv_text
        )

    except Exception:

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


def write_repository_results(
    dataframe,
    commit_message
):

    if "GITHUB_RESULTS_TOKEN" not in st.secrets:

        return (
            False,
            "GITHUB_RESULTS_TOKEN is not configured "
            "in Streamlit Secrets."
        )

    token = st.secrets[
        "GITHUB_RESULTS_TOKEN"
    ]

    if not token:

        return (
            False,
            "GITHUB_RESULTS_TOKEN is empty."
        )

    try:

        _, current_sha = (
            fetch_github_results_file()
        )

        csv_text = dataframe[
            RESULT_COLUMNS
        ].to_csv(
            index=False
        )

        encoded_content = (
            base64.b64encode(
                csv_text.encode("utf-8")
            )
            .decode("utf-8")
        )

        response = requests.put(
            github_results_url(),
            headers=github_headers(),
            json={
                "message": commit_message,
                "content": encoded_content,
                "sha": current_sha,
                "branch": GITHUB_RESULTS_BRANCH,
            },
            timeout=20
        )

        response.raise_for_status()

        return True, ""

    except Exception as error:

        return False, str(error)


def initialise_results():

    if "research_results" not in (
        st.session_state
    ):

        dataframe = (
            read_repository_results()
        )

        st.session_state[
            "research_results"
        ] = dataframe.to_dict(
            orient="records"
        )


def refresh_results():

    dataframe = read_repository_results()

    st.session_state[
        "research_results"
    ] = dataframe.to_dict(
        orient="records"
    )

    return dataframe


def next_run_id():

    remote_results = (
        read_repository_results()
    )

    initialise_results()

    session_results = pd.DataFrame(
        st.session_state[
            "research_results"
        ],
        columns=RESULT_COLUMNS
    )

    combined_results = pd.concat(
        [
            remote_results,
            session_results
        ],
        ignore_index=True
    )

    highest_run_number = 0

    for run_id in combined_results[
        "run_id"
    ].astype(str):

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

    complete_result = {}

    for column in RESULT_COLUMNS:

        complete_result[column] = (
            result.get(column, "")
        )

    remote_results = (
        read_repository_results()
    )

    if (
        not remote_results.empty
        and complete_result["run_id"]
        in remote_results[
            "run_id"
        ].astype(str).tolist()
    ):

        return (
            False,
            "This run ID already exists "
            "in the GitHub results file."
        )

    new_row = pd.DataFrame(
        [complete_result],
        columns=RESULT_COLUMNS
    )

    updated_results = pd.concat(
        [
            remote_results,
            new_row
        ],
        ignore_index=True
    )

    saved, message = (
        write_repository_results(
            updated_results,
            (
                "Append research result "
                f"{complete_result['run_id']}"
            )
        )
    )

    st.session_state[
        "research_results"
    ] = updated_results.to_dict(
        orient="records"
    )

    return saved, message


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

        dataframe[column] = (
            pd.to_numeric(
                dataframe[column],
                errors="coerce"
            )
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

    clean_dataframe = (
        dataframe.where(
            pd.notna(dataframe),
            ""
        )
    )

    remote_results = (
        read_repository_results()
    )

    score_fields = [
        "correctness_0_2",
        "relevance_0_2",
        "faithfulness_0_2",
        "total_quality_0_6",
        "consistency_0_2",
        "qualitative_notes",
        "scored_by",
    ]

    for _, edited_row in (
        clean_dataframe.iterrows()
    ):

        run_id = str(
            edited_row["run_id"]
        )

        matching_rows = (
            remote_results[
                "run_id"
            ].astype(str)
            == run_id
        )

        if matching_rows.any():

            for field in score_fields:

                remote_results.loc[
                    matching_rows,
                    field
                ] = str(
                    edited_row[field]
                )

    saved, message = (
        write_repository_results(
            remote_results,
            "Update research result scoring"
        )
    )

    st.session_state[
        "research_results"
    ] = remote_results.to_dict(
        orient="records"
    )

    return remote_results, saved, message
