import json   # used to work with JSON files
import os     # used to check file existence
import time   # used to add delay between retries

FILE_PATH = "data/tasks.json"   # where we store tasks


def load_tasks():
    """
    Load tasks from JSON file safely
    """

    # Case 1: File doesn't exist → return empty list
    if not os.path.exists(FILE_PATH):
        return []

    # Open file
    with open(FILE_PATH, "r") as file:

        # Read file content
        content = file.read().strip()

        # Case 2: File exists but empty → return empty list
        if not content:
            return []

        # Convert JSON string → Python list
        return json.loads(content)


def save_tasks(new_tasks):
    """
    Save new tasks into file
    """

    os.makedirs("data", exist_ok=True)

    tasks = load_tasks()

    # Create a set of existing task names (lowercase for matching)
    existing_tasks = set(
        (task["task"].lower(), task["owner"].lower())
        for task in tasks
    )

    # Add only new unique tasks
    for new_task in new_tasks:
        key = (new_task["task"].lower(), new_task["owner"].lower())

        if key not in existing_tasks:
            tasks.append(new_task)

    # Save updated list
    with open(FILE_PATH, "w") as file:
        json.dump(tasks, file, indent=4)

def get_pending_tasks():
    """
    This function returns only pending tasks
    Why needed?
    → Later UI should show only unfinished work
    """

    tasks = load_tasks()   # load all tasks from tasks.json

    # create new list that only keeps pending tasks
    pending_tasks = [
        task for task in tasks
        if task["status"] == "pending"
    ]

    return pending_tasks   # send filtered tasks back