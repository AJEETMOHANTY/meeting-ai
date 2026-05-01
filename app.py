import streamlit as st              # used to build web UI
import json                         # converts AI output string → Python dict

from modules.llm_processor import process_text
# process_text → sends transcript to Gemini

from modules.task_manager import save_tasks, get_pending_tasks
# save_tasks → stores extracted tasks
# get_pending_tasks → loads pending tasks


# Page title shown in browser
st.title("AI Meeting Assistant")

# Text box where user pastes meeting transcript
meeting_text = st.text_area(
    "Paste your meeting transcript here:"
)

# Button to process transcript
if st.button("Generate Summary & Tasks"):

    # Prevent empty input
    if meeting_text.strip() == "":
        st.warning("Please enter meeting transcript")
    
    else:
        # Send transcript to Gemini
        result = process_text(meeting_text)

        # Convert JSON string → Python dictionary
        data = json.loads(result)

        # Save extracted tasks
        save_tasks(data["tasks"])

        # Show summary
        st.subheader("Meeting Summary")
        st.write(data["summary"])

        # Show extracted tasks
        st.subheader("Extracted Tasks")

        for task in data["tasks"]:
            st.write(
                f"Task: {task['task']} | Owner: {task['owner']} | Status: {task['status']}"
            )

        # Show pending tasks
        st.subheader("Pending Tasks")

        pending_tasks = get_pending_tasks()

        for task in pending_tasks:
            st.write(
                f"{task['task']} | Owner: {task['owner']}"
            )