import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

st.title("📤 Google Drive Uploader (Streamlit Version)")

# Step 1: Upload file
uploaded_file = st.file_uploader("कोई भी फ़ाइल चुनें", type=None)

if uploaded_file is not None:
    # Step 2: Save file temporarily
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Step 3: Authenticate and upload to Google Drive
    FOLDER_ID = "18Cl7QrKmELWFeHEDT00uE83GZsG96yqh"
    SERVICE_ACCOUNT_FILE = "service_account.json"

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    drive_service = build("drive", "v3", credentials=credentials)

    file_metadata = {"name": uploaded_file.name, "parents": [FOLDER_ID]}
    media = MediaFileUpload(file_path)
    drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    # Cleanup and success message
    os.remove(file_path)
    st.success("✅ आपकी फ़ाइल Google Drive में सेव हो गई!")
