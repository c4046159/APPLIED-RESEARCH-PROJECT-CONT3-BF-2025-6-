import io

import streamlit as st

from google.oauth2 import service_account
from googleapiclient.discovery import build

from pypdf import PdfReader
from docx import Document


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
