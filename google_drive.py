import io

import streamlit as st

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pypdf import PdfReader


DRIVE_SCOPE = [
    "https://www.googleapis.com/auth/drive.readonly"
]

PDF_MIME = "application/pdf"


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

    return build(
        "drive",
        "v3",
        credentials=credentials
    )


def list_folder_files():

    drive_service = get_drive_service()

    folder_id = st.secrets[
        "GOOGLE_DRIVE_FOLDER_ID"
    ]

    result = drive_service.files().list(
        q=(
            f"'{folder_id}' in parents "
            "and trashed = false "
            f"and mimeType = '{PDF_MIME}'"
        ),
        fields="files(id, name, mimeType)",
        orderBy="name",
        pageSize=100
    ).execute()

    return result.get("files", [])


def download_file_bytes(file_id):

    drive_service = get_drive_service()

    request = drive_service.files().get_media(
        fileId=file_id
    )

    file_buffer = io.BytesIO()

    downloader = MediaIoBaseDownload(
        file_buffer,
        request
    )

    done = False

    while not done:
        _, done = downloader.next_chunk()

    return file_buffer.getvalue()


def extract_pdf_text(file_bytes):

    reader = PdfReader(
        io.BytesIO(file_bytes)
    )

    pages = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    return "\n".join(pages)


def read_drive_file(file_info):

    if file_info["mimeType"] != PDF_MIME:
        return None

    file_bytes = download_file_bytes(
        file_info["id"]
    )

    text = extract_pdf_text(
        file_bytes
    ).strip()

    if not text:
        return None

    return {
        "name": file_info["name"],
        "mime_type": file_info["mimeType"],
        "text": text,
    }


def load_research_documents():

    documents = []
    skipped_files = []

    for file_info in list_folder_files():

        try:

            document = read_drive_file(
                file_info
            )

            if document:
                documents.append(document)
            else:
                skipped_files.append(
                    file_info["name"]
                )

        except Exception:

            skipped_files.append(
                file_info["name"]
            )

    return documents, skipped_files
