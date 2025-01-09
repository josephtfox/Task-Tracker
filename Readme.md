# Task Tracker

Task Tracker is a command-line application for managing and tracking tasks. It allows users to add, list, and update the status of tasks efficiently.

## Features

- Add new tasks
- List all tasks
- List tasks by status (not-done, in-progress, done)
- Mark tasks as in-progress or done
- Persistent storage using JSON

## Installation

1. Clone the repository:
    git clone https://github.com/yourusername/task-tracker.git
    cd task-tracker

2. Ensure you have Python 3.6 or later installed.

3. No additional dependencies are required as the project uses Python's standard libraries.

## Usage

Run the application:

    python TaskTracker.py


### Commands

- `add <description>`: Add a new task
- `list [status]`: List all tasks or tasks with a specific status
- `mark_in_progress <task_id>`: Mark a task as in-progress
- `mark_done <task_id>`: Mark a task as done
- `exit`: Exit the application

### Examples

(TaskTracker) add Complete project report
(TaskTracker) list
(TaskTracker) list not-done
(TaskTracker) mark_in_progress 5f033fea-2847-454f-ad0d-5c8cccb5d03f
(TaskTracker) mark_done 5f033fea-2847-454f-ad0d-5c8cccb5d03f

## File Structure

- `TaskTracker.py`: Main application file
- `tasks.json`: JSON file for storing tasks (created automatically)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
