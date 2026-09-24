import io

import streamlit as st

from docx import Document
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pypdf import PdfReader


DRIVE_SCOPE = [
    "https://www.googleapis.com/auth/drive.readonly"
]


GOOGLE_DOC_MIME = (
    "application/vnd.google-apps.document"
)

PDF_MIME = "application/pdf"

DOCX_MIME = (
    "application/vnd.openxmlformats-officedocument."
    "wordprocessingml.document"
)

TEXT_MIME_TYPES = {
    "text/plain",
    "text/markdown",
}


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
            "and mimeType != 'application/vnd.google-apps.folder'"
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


def export_google_doc_text(file_id):

    drive_service = get_drive_service()

    request = drive_service.files().export_media(
        fileId=file_id,
        mimeType="text/plain"
    )

    file_buffer = io.BytesIO()

    downloader = MediaIoBaseDownload(
        file_buffer,
        request
    )

    done = False

    while not done:
        _, done = downloader.next_chunk()

    return file_buffer.getvalue().decode(
        "utf-8",
        errors="ignore"
    )


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


def extract_docx_text(file_bytes):

    document = Document(
        io.BytesIO(file_bytes)
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_plain_text(file_bytes):

    return file_bytes.decode(
        "utf-8",
        errors="ignore"
    )


def read_drive_file(file_info):

    file_id = file_info["id"]
    file_name = file_info["name"]
    mime_type = file_info["mimeType"]

    if mime_type == GOOGLE_DOC_MIME:

        text = export_google_doc_text(
            file_id
        )

    elif mime_type == PDF_MIME:

        file_bytes = download_file_bytes(
            file_id
        )

        text = extract_pdf_text(
            file_bytes
        )

    elif mime_type == DOCX_MIME:

        file_bytes = download_file_bytes(
            file_id
        )

        text = extract_docx_text(
            file_bytes
        )

    elif (
        mime_type in TEXT_MIME_TYPES
        or file_name.lower().endswith(
            (".txt", ".md")
        )
    ):

        file_bytes = download_file_bytes(
            file_id
        )

        text = extract_plain_text(
            file_bytes
        )

    else:

        return None

    text = text.strip()

    if not text:
        return None

    return {
        "name": file_name,
        "mime_type": mime_type,
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
