import streamlit as st

from google.oauth2 import service_account
from googleapiclient.discovery import build


DRIVE_SCOPE = [
    "https://www.googleapis.com/auth/drive.readonly"
]


def get_drive_service():

    service_account_info = dict(
        st.secrets["gcp_service_account"]
    )

    credentials = (
        service_account.Credentials
        .from_service_account_info(
            service_account_info,
            scopes=DRIVE_SCOPE
        )
    )

    drive_service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    return drive_service


def list_folder_files():

    drive_service = get_drive_service()

    folder_id = st.secrets[
        "GOOGLE_DRIVE_FOLDER_ID"
    ]

    result = drive_service.files().list(
        q=(
            f"'{folder_id}' in parents "
            "and trashed = false "
            "and mimeType != 'application/vnd.google-apps.folder'"
        ),
        fields="files(id, name, mimeType)",
        orderBy="name",
        pageSize=100
    ).execute()

    return result.get("files", [])
