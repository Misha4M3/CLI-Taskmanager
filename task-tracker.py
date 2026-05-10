#Each task is to come with a Task ID, Time stamp, Status and description
import json
import os #lets you check wether or not a task already exists
from datetime import datetime

TASKS_FILE = "tasks.json"
now = datetime.now().isoformat()

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return [] 
    with open(TASKS_FILE, "r") as f:
        return json.load(f)
# mehanizm po zagruzke, файлы хранятся на диске спомошью Json

def save_tasks(tasks):
    with open(TASKS_FILE,"w") as f:
        json.dump(tasks, f, indent=2)

if __name__ == "__main__":
    print("Task tracker is running!")
    test_tasks = [
        { 
            "id": 1,
            "description": "Finish CLI",
            "status":"todo",
            "createdAt": now,
            "updatedAt": now
        }
    ]
    save_tasks(test_tasks)
    print("Saved successfully")

    loaded = load_tasks()
    print("Loaded:", loaded)
    #CRUD Functions tba