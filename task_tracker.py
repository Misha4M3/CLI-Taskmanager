#Each task is to come with a Task ID, Time stamp, Status and description
import json
import os #lets you check wether or not a task already exists
import sys
from datetime import datetime


VALID_STATUSES = ["todo", "in-progress", "done"]
TASKS_FILE = "tasks.json"
now = datetime.now().isoformat()

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return [] 
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: task.json is corrupted. Starting with empty task list.")
        return []
# mehanizm po zagruzke, файлы хранятся на диске спомошью Json

def save_tasks(tasks):
    with open(TASKS_FILE,"w") as f:
        json.dump(tasks, f, indent=2)

def add_task(description):
    if not description.strip():
        print("Description cannot be empty")
        return
    
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) +1
    now = datetime.now().isoformat()
    tasks.append({
        "id" : new_id,
        "description" : description.strip(),
        "status" : "todo",
        "createdAt" : now,
        "updatedAt" : now
    })
    save_tasks(tasks)
    print(f"Tasks added (ID: {new_id})")

def delete_task(task_id):
    tasks = load_tasks()
    original_count = len(tasks)

    tasks = [t for t in tasks if t["id"] != task_id]
    #keep everything except the one i want to delete

    if len(tasks) == original_count:
        print(f"No task found with ID {task_id}")
        return
    save_tasks(tasks)
    print(f"Task {task_id} deleted")

def update_task(task_id, new_description):
    if not new_description.strip():
        print("Description cannot be empty")
        return

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description.strip()
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated")
            return
    print(f"No task found with ID {task_id}")

def mark_task(task_id, status):
    if status not in VALID_STATUSES:
        print(f"Invalid status. Choose from: {','.join(VALID_STATUSES)}")
        #na sluchi proyobov
        return
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return
    print(f"No task found with ID {task_id}")

def list_tasks(filter_status=None):
    tasks = load_tasks()

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("No tasks found")
        return
    label = f"({filter_status})" if filter_status else "(all)"
    print(f"\n-- Tasks {label}: {len(tasks)} total --\n")

    for task in tasks:
        print(f"[{task['id']}] ({task['status']}) {task['description']}")
        print(f"Status: {task['status']}")
        print(f"Created: {task['createdAt']}")
        print(f"Updated: {task['updatedAt']}")
        print()

def parse_id(value):
    try:
        return int(value)
    except ValueError:
        print(f"Invalid ID '{value}' - must be a whole number")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 task_tracker.py <command> [arguments]")
        print("Commands: add, delete, update, mark, list")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: python3 task_tracker.py add <description>")
        else:
            add_task(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python3 task_tracker.py delete <id>")
        else:
            delete_task(parse_id(sys.argv[2]))
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: python3 task_tracker.py update <id> <description>")
        else:
            update_task(parse_id(sys.argv[2]), sys.argv[3])
    elif command == "mark":
        if len(sys.argv) < 4:
            print("Usage: python3 task_tracker.py mark <id> <status>")
        else:
            mark_task(parse_id(sys.argv[2]), sys.argv[3])
    elif command == "list":
        if len(sys.argv) == 3:
            list_tasks(sys.argv[2])
        else:
            list_tasks()
    else:
        print(f"Unknown commnad: {command}")
        print("Commands: add, delete, update, mark, list.")