from modules.llm_processor import process_text  # import the function we created
from modules.task_manager import save_tasks, get_pending_tasks # import the functions we created
import json  # used to work with JSON files

text = """
Team discussed the project deadline.
Ajeet will build backend APIs.
Chunnu will design UI.
"""
# this is your sample meeting text

# Step 1 → Send text to AI and get result
result = process_text(text) 

print("AI Output:")
print(result)  # print output on screen

# Step 2 → Convert JSON string into Python dictionary.This is needed because AI returns a JSON string, but we need to work with a Python dictionary
data = json.loads(result)

# Step 3 → Save extracted tasks
save_tasks(data["tasks"])

print("\nTasks saved successfully!")

# Step 4 → Get only pending tasks
pending_tasks = get_pending_tasks()

print("\nPending Tasks:")

# Step 5 → Print pending tasks cleanly
for task in pending_tasks:
    print(
        f"- {task['task']} | Owner: {task['owner']}"
    )