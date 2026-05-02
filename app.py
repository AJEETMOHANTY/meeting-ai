import streamlit as st
import json
import os

from modules.transcriber import transcribe_audio
from modules.llm_processor import process_text
from modules.task_manager import save_tasks, get_pending_tasks


# app title
st.title("AI Meeting Assistant")

# upload audio file
uploaded_file = st.file_uploader(
    "Upload meeting audio",
    type=["mp3", "wav", "m4a"]
)

# process button
if st.button("Generate Summary & Tasks"):

    if uploaded_file is None:
        st.warning("Please upload an audio file")

    else:
        # create temp folder if not exists
        os.makedirs("temp", exist_ok=True)

        # save uploaded file temporarily
        file_path = f"temp/{uploaded_file.name}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("Transcribing audio...")

        # convert audio → text
        transcript = transcribe_audio(file_path)

        st.subheader("Transcript")
        st.write(transcript)

        # send transcript to Gemini
        result = process_text(transcript)

        # convert JSON string → Python dictionary
        data = json.loads(result)

        # save tasks
        save_tasks(data["tasks"])

        # show summary
        st.subheader("Meeting Summary")
        st.write(data["summary"])

        # show extracted tasks
        st.subheader("Extracted Tasks")

        for task in data["tasks"]:
            st.write(
                f"Task: {task['task']} | Owner: {task['owner']} | Status: {task['status']}"
            )

        # show pending tasks
        st.subheader("Pending Tasks")

        pending_tasks = get_pending_tasks()

        for task in pending_tasks:
            st.write(
                f"{task['task']} | Owner: {task['owner']}"
            )