import sys
import json
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    try: 
        with open(TASKS_FILE, 'r') as f: 
            return json.load(f)
    except FileNotFoundError: 
        return []
    except: 
        print("Something went wrong")
        return []

def save_tasks(tasks):
    try: 
        with open(TASKS_FILE, 'w') as f: 
            json.dump(tasks, f, indent=2, ensure_ascii=False)
    except Exception as e: 
        print(f"Error when saving file {e}")

def add_task(description=""):
    tasks = load_tasks()

    if tasks:
        new_id = max(task['id'] for task in tasks) + 1
    else:
        new_id = 1

    current_time = datetime.now().isoformat()
    new_task = {
        'id': new_id,
        'description': description,
        'status': 'todo',  
        'createdAt': current_time,
        'updatedAt': current_time  
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    
    print(f"Task created (ID: {new_id}): {description}")

def update_task_description(task_id, new_description):
    tasks = load_tasks()  # загружаем все задачи

    task_found = False
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            task_found = True
            break
    
    if task_found:
        save_tasks(tasks)  
        print(f"Task ID {task_id} updated: {new_description}")
    else:
        print(f"Task with ID {task_id} not found")

def update_task_status(task_id, new_status):
    tasks = load_tasks()  # загружаем все задачи

    task_found = False
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            task['updatedAt'] = datetime.now().isoformat()
            task_found = True
            break
    
    if task_found:
        save_tasks(tasks)  
        print(f"Task ID {task_id} updated: {new_status}")
    else:
        print(f"Task with ID {task_id} not found")

def delete_task(task_id):
    tasks = load_tasks()
    
    initial_length = len(tasks)
    
    tasks = [task for task in tasks if task['id'] != task_id]
     
    if len(tasks) < initial_length:
        save_tasks(tasks)
        print(f"Task ID {task_id} deleted")
        return True
    else:
        print(f"Task with ID {task_id} not found")
        return False

def list_tasks(status_filter=None):
    tasks = load_tasks()
    
    if status_filter:
        tasks = [task for task in tasks if task['status'] == status_filter]
    
    if not tasks:
        status_text = f" with status '{status_filter}'" if status_filter else ""
        print(f"📭 No tasks{status_text}")
        return
    
    # Status emojis
    status_icons = {'todo': '📝', 'in-progress': '🔄', 'done': '✅'}
    
    print("\n" + "=" * 70)
    print(f"📋 TASK LIST{' (' + status_filter + ')' if status_filter else ''}")
    print("=" * 70)
    
    for task in tasks:
        icon = status_icons.get(task['status'], '❓')
        created = task['createdAt'][:10]  
        
        print(f"{icon} #{task['id']:03d} | {task['status']:12} | {task['description']}")
        print(f"    Created: {created} | Updated: {task['updatedAt'][:10]}")
        print("-" * 70)
    
    print(f"Total: {len(tasks)} task{'s' if len(tasks) != 1 else ''}\n")

# Основная логика CLI
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [command] [arguments]")
        print("\nCommands:")
        print("  add <description>           - Add new task")
        print("  list [status]               - List all tasks (or filter by status)")
        print("  delete <id>                 - Delete task by ID")
        print("  update <id> <description>   - Update task description")
        print("  mark-in-progress <id>       - Mark task as in progress")
        print("  mark-done <id>              - Mark task as done")
        print("  help                        - Show help")
        print("\nExamples:")
        print("  python main.py add \"Buy groceries\"")
        print("  python main.py list")
        print("  python main.py mark-in-progress 1")
        print("  python main.py mark-done 2")
        print("  python main.py update 1 \"Buy milk and bread\"")
        print("  python main.py delete 3")
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Error: Task description required")
                print("Usage: python main.py add \"Task description\"")
                sys.exit(1)
            description = sys.argv[2]
            add_task(description)

        elif command == "list":
            if len(sys.argv) > 3:
                print("Error: Too many arguments for list command")
                print("Usage: python main.py list [status]")
                sys.exit(1)
            
            status_filter = sys.argv[2] if len(sys.argv) > 2 else None
            if status_filter and status_filter not in ['todo', 'in-progress', 'done']:
                print(f"Error: Invalid status '{status_filter}'")
                print("Valid status values: todo, in-progress, done")
                sys.exit(1)
            list_tasks(status_filter)

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Task ID required")
                print("Usage: python main.py delete <id>")
                sys.exit(1)
            
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print(f"Error: ID must be a number, got '{sys.argv[2]}'")
                sys.exit(1)
            
            delete_task(task_id)

        elif command == "update":
            if len(sys.argv) < 4:
                print("Error: Task ID and new description required")
                print("Usage: python main.py update <id> \"New description\"")
                sys.exit(1)
            
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print(f"Error: ID must be a number, got '{sys.argv[2]}'")
                sys.exit(1)
            
            new_description = sys.argv[3]
            update_task_description(task_id, new_description)

        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("Error: Task ID required")
                print("Usage: python main.py mark-in-progress <id>")
                sys.exit(1)
            
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print(f"Error: ID must be a number, got '{sys.argv[2]}'")
                sys.exit(1)
            
            update_task_status(task_id, "in-progress")

        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Error: Task ID required")
                print("Usage: python main.py mark-done <id>")
                sys.exit(1)
            
            try:
                task_id = int(sys.argv[2])
            except ValueError:
                print(f"Error: ID must be a number, got '{sys.argv[2]}'")
                sys.exit(1)
            
            update_task_status(task_id, "done")

        elif command in ["help", "--help", "-h"]:
            print("Task Tracker CLI - Manage your tasks")
            print("\nCommands:")
            print("  add <description>           Add a new task")
            print("  list [status]               List tasks (filter by status)")
            print("  update <id> <description>   Update task description")
            print("  mark-in-progress <id>       Mark task as in progress")
            print("  mark-done <id>              Mark task as done")
            print("  delete <id>                 Delete a task")
            print("  help                        Show this help message")
            print("\nExamples:")
            print("  python main.py add \"Complete project\"")
            print("  python main.py mark-in-progress 1")
            print("  python main.py mark-done 2")
            print("  python main.py list in-progress")
            print("  python main.py delete 3")

        else:
            print(f"Error: Unknown command '{command}'")
            print("Type 'python main.py help' for available commands")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()