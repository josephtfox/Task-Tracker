import os
import json
import uuid
import cmd
from datetime import datetime
import enums
import tabulate

"""
Task Properties:
    id: A unique identifier for the task
    description: A short description of the task
    status: The status of the task (todo, in-progress, done)
    createdAt: The date and time when the task was created
    updatedAt: The date and time when the task was last updated
"""
class Task():
    def __init__(self, description, id=None, status="not-done", createdAt=None, updatedAt=None):
        self.description = description
        self.id = id or str(uuid.uuid4())
        self.status = status if isinstance(status, enums.Status) else enums.Status(status)
        self.createdAt = createdAt or datetime.now()
        self.updatedAt = updatedAt or datetime.now()

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(
            description=data['description'],
            id=data['id'],
            status=enums.Status(data['status']),
            createdAt=datetime.fromisoformat(data['createdAt']),
            updatedAt=datetime.fromisoformat(data['updatedAt'])
        )
    
    def to_json(self):
        return {
            'description':self.description,
            'id':self.id,
            'status':self.status.value,
            'createdAt':self.createdAt.isoformat(),
            'updatedAt':self.updatedAt.isoformat()
        }
    
class TaskTracker:
    PATH = "data"
    FILE_NAME = "tasks.json"
    FILE_PATH = os.path.join(PATH, FILE_NAME)

    def __init__(self):
        self.tasks = {}
        self.load_json()

    def load_json(self):
        # Check if directory exists, if not create it
        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)
            print(f"Created directory: {self.PATH}")

        # Check if file exists and is readable
        if os.path.isfile(self.FILE_PATH) and os.access(self.FILE_PATH, os.R_OK):
            print("File exists and is readable")
            try:
                with open(self.FILE_PATH, 'r') as db_file:
                    tasks_data = json.load(db_file)
                    self.tasks = {
                        task_id: Task.from_json(json.dumps(task_data))
                        for task_id, task_data in tasks_data.items()
                    }
            except ValueError:
                self.tasks = {}
        else:
            print("Either file is missing or is not readable, creating file...")
            try:
                with open(self.FILE_PATH, 'w') as db_file:
                    json.dump({}, db_file)
                print(f"Created file: {self.FILE_PATH}")
            except IOError as e:
                print(f"Error creating file: {e}")

    def save_to_json(self):
        with open(self.FILE_PATH, 'w') as file:
            json.dump({
                task_id: task.to_json()
                for task_id, task in self.tasks.items()
            }, file, indent=4)

    def print_tasks(self, data):
        headers = ["Id", "Description", "Status", "Created At", "Updated At"]
        table_data = [
            [
                task.id,
                task.description,
                task.status.value,
                task.createdAt.strftime("%d/%m/%Y %H:%M:%S"),
                task.updatedAt.strftime("%d/%m/%Y %H:%M:%S")
            ]
            for task in data.values()
        ]
        print(tabulate.tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    def query(self, status):
        status = status.lower().replace('-', '_')
        try:
            target_status = enums.Status[status.upper()]
            filtered_tasks = {key: task for key, task in self.tasks.items() if task.status == target_status}
            self.print_tasks(filtered_tasks)
        except KeyError:
            print(f"Invalid status: {status}. Valid options are: not-done, in-progress, done")
        # target_status = getattr(enums.Status, status, None)
        # filtered_tasks = {key: task for key, task in self.tasks.items() if task.status == target_status}

    def add_task(self, description):
        task = Task(description)
        self.tasks[task.id] = task
        self.save_to_json()

    def update_task(self, id, new_description):
        if id in self.tasks:
            self.tasks[id].description = new_description
            self.tasks[id].updatedAt = datetime.now()
            self.save_to_json()
            print(f"Task {id } description updated successfully")
        else:
            print(f"Task with ID {id} not found")

    def delete_task(self, id):
        if id in self.tasks:
            del self.tasks[id]
            self.save_to_json()
            print(f"Task with ID {id} was Deleted")
        else:
            print(f"Task with ID {id} not found")

    def change_status(self, id, status):
        if id in self.tasks:
            self.tasks[id].status = enums.Status(status)
            self.tasks[id].updatedAt = datetime.now()
            self.save_to_json()
            print(f"Task {id} status updated successfully")
        else:
            print(f"Task with ID {id} not found")


class TaskTrackerShell(cmd.Cmd):
    intro = "Welcome to TaskTracker. Type 'help' for commands."
    prompt = '(TaskTracker) '


    def __init__(self):
        super().__init__()
        self.task_tracker = TaskTracker()
    
    def do_add(self, arg):
        """
        Add a Task. Usage: add <task description>
        """
        if arg:
            self.task_tracker.add_task(arg)
            print(f"Added Task: {arg}")
        else:
            print("Error - Usage: add <task description>")
    
    def do_update(self, arg):
        """
        Update a Task description based on the id. Usage: update <id> <description>
        """
        parts = arg.split(maxsplit=1)
        if len(parts) == 2:
            id, description = parts
            self.task_tracker.update_task(id, description)
            print(f"Updated task: {id} - {description}")
        else:
            print("Error - Usage: update <id> <task description> ")

    def do_delete(self, arg):
        """
        Delete a Task. Usage: delete <id>
        """
        if arg:
            self.task_tracker.delete_task(arg)
            print(f"Deleted Task: {arg}")
        else:
            print("Error - Usage: delete <id>")

    def do_list(self, arg):
        """
        List tasks. Usage: list [status]
        """
        arg = arg.strip().lower()
        if not arg:
            # If no argument is provided, list all tasks
            self.task_tracker.print_tasks(self.task_tracker.tasks)
        else:
            try:
                # Try to convert the argument to a Status enum
                status = enums.Status(arg)
                self.task_tracker.query(status)
                print(f"Queried Tasks with {status.value} status")
            except ValueError:
                # If the argument is not a valid Status enum value
                print(f"Invalid status: {arg}")
                print("Valid statuses are: " + ", ".join([status.value for status in enums.Status]))

    def do_mark(self, arg):
        """
        Mark the task as in-progress or done. Usage: mark <status> <id> 
        """
        parts = arg.split(maxsplit=1)
        if len(parts) == 2:
            status, id = parts
            self.task_tracker.change_status(id, status)
            print(f"Marked task: {id} - {status}")
        else:
            print("Error - Usage: mark <status> <id>")

    def do_exit(self, arg):
        """
        Exit the Task Manager
        """
        print("Goodbye!")
        return True


if __name__ == "__main__":
    TaskTrackerShell().cmdloop()