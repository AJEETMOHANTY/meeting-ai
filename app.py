import streamlit as st
import json
import os

from modules.transcriber import transcribe_audio
from modules.ollama_processor import process_large_transcript
from modules.gemini_processor import generate_final_json
from modules.task_manager import save_tasks, load_tasks, get_pending_tasks


# app title
st.title("AI Meeting Assistant")

# upload audio file
uploaded_file = st.file_uploader(
    "Upload meeting audio",
    type=["mp3", "wav", "m4a","mp4"]
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

        # send summary to Gemini for json generation
        # result = process_text(transcript)

        # Step 1: Ollama chunk summaries
        combined_summary = process_large_transcript(transcript)

        print("Combined Summary:")
        print(combined_summary)

        # Step 2: Gemini final JSON output
        result = generate_final_json(combined_summary)

        print("Final Gemini Output:")
        print(result)

        print("Ollama Raw Output:")
        print(result)

        
        try:
            # convert JSON string → Python dictionary
            data = json.loads(result)

        except json.JSONDecodeError:
            st.error("Model did not return valid JSON")

            # show raw model response for debugging
            st.write(result)

            # stop app here so next code doesn't run
            st.stop()

        # save tasks
        # save_tasks(data["tasks"])
        tasks = data.get("tasks", [])
        save_tasks(tasks)

        print(data)
        st.write(data)

        # show summary
        st.subheader("Meeting Summary")
        st.write(data.get("summary", "No summary found"))

        # show extracted tasks
        st.subheader("Extracted Tasks")

        for task in data.get("tasks", []):
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

