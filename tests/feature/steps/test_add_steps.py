import pytest

import sys
import os
from pytest_bdd import scenarios, given, when, then
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src')))
from tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, get_overdue_tasks

tasks_file = 'tasks.json'

scenarios('../add_task.feature')

#Step Definitions

@given('there are tasks in the tasks file')
def tasks_in_file():
    tasks = [
        {
            "id": 1,
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "Medium",
            "category": "Work",
            "due_date": "2025-05-01",
            "completed": False
        }
    ]
    save_tasks(tasks, 'tasks.json')
    return tasks

@when('I load the tasks')
def load_the_tasks():
    return load_tasks('tasks.json')

@then('I should see a list of tasks')
def check_loaded_tasks():
    tasks = load_tasks('tasks.json')
    assert isinstance(tasks, list)
    assert len(tasks) > 0

@given('the tasks list is empty')
def empty_task_list():
    save_tasks([], 'tasks.json')

@when('I add a task with title "New Task"')
def add_task():
    tasks = load_tasks('tasks.json')
    new_task = {
        "id": generate_unique_id(tasks),
        "title": "New Task",
        "priority": "Medium",
        "category": "Work",
        "due_date": "2025-05-01",
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks, 'tasks.json')

@then('the task should have an ID of 1')
def check_task_id():
    tasks = load_tasks('tasks.json')
    assert len(tasks) == 1

@given('there are tasks with different priorities')
def tasks_with_priorities():
    tasks = [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-05-01", "completed": False},
        {"id": 2, "title": "Task 2", "priority": "Medium", "category": "Home", "due_date": "2025-05-02", "completed": False}
    ]
    save_tasks(tasks, 'tasks.json')

@when('I filter tasks by "High" priority')
def filter_by_priority():
    tasks = load_tasks('tasks.json')
    save_tasks([], 'tasks.json')
    priority_tasks = filter_tasks_by_priority(tasks, "High")
    save_tasks(priority_tasks, 'tasks.json')

@then('I should see only tasks with "High" priority')
def check_filtered_by_priority():
    priority_tasks = load_tasks('tasks.json')
    assert all(task["priority"] == "High" for task in priority_tasks)

@given('there are tasks with different categories')
def tasks_with_categories():
    tasks = [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-05-01", "completed": False},
        {"id": 2, "title": "Task 2", "priority": "Medium", "category": "Home", "due_date": "2025-05-02", "completed": False}
    ]
    save_tasks(tasks, 'tasks.json')

@when('I filter tasks by "Work" category')
def filter_by_category():
    tasks = load_tasks('tasks.json')
    save_tasks([], 'tasks.json')
    category_tasks = filter_tasks_by_category(tasks, "Work")
    save_tasks(category_tasks, 'tasks.json')

@then('I should see only tasks with "Work" category')
def check_filtered_by_category():
    category_tasks = load_tasks('tasks.json')
    assert all(task["category"] == "Work" for task in category_tasks)

@given('there are tasks with overdue due dates')
def overdue_tasks():
    tasks = [
        {"id": 1, "title": "Overdue Task", "priority": "High", "category": "Work", "due_date": "2025-01-01", "completed": False}
    ]
    save_tasks(tasks, 'tasks.json')

@when('I check for overdue tasks')
def check_overdue():
    tasks = load_tasks('tasks.json')
    save_tasks([], 'tasks.json')
    overdue_tasks = get_overdue_tasks(tasks)
    save_tasks(overdue_tasks, 'tasks.json')

@then('I should see only tasks that are overdue and not completed')
def check_overdue_tasks():
    overdue_tasks = load_tasks('tasks.json')
    assert all(task["due_date"] < datetime.now().strftime("%Y-%m-%d") and not task["completed"] for task in overdue_tasks)