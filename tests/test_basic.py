import pytest

import tempfile
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tasks import (
    load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, 
    filter_tasks_by_category, filter_tasks_by_completion, search_tasks, get_overdue_tasks
)
from datetime import datetime, timedelta

@pytest.fixture
def sample_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        {"id": 1, "title": "Task 1", "description": "Finish Assignment", "priority": "High", "category": "Work", "due_date": today, "completed": False},
        {"id": 2, "title": "Task 2", "description": "Cook Dinner", "priority": "Low", "category": "Personal", "due_date": today, "completed": True},
        {"id": 3, "title": "Task 3", "description": "Write Report", "priority": "Medium", "category": "Work", "due_date": today, "completed": False}
    ]

def test_generate_unique_id(sample_tasks):
    assert generate_unique_id(sample_tasks) == 4

def test_filter_tasks_by_priority(sample_tasks):
    filtered = filter_tasks_by_priority(sample_tasks, "High")
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Task 1"

def test_filter_tasks_by_category(sample_tasks):
    filtered = filter_tasks_by_category(sample_tasks, "Work")
    assert len(filtered) == 2

def test_filter_tasks_by_completion(sample_tasks):
    filtered = filter_tasks_by_completion(sample_tasks, completed=False)
    assert len(filtered) == 2

def test_search_tasks(sample_tasks):
    results = search_tasks(sample_tasks, "Write Report")
    assert len(results) == 1
    assert results[0]["title"] == "Task 3"

def test_get_overdue_tasks():
    overdue_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tasks = [
        {"id": 1, "title": "Overdue Task", "description": "", "priority": "High", "category": "Work", "due_date": overdue_date, "completed": False}
    ]
    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 1

def test_load_and_save_tasks():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name
    tmp.close()
    
    test_data = [{"id": 1, "title": "Save Test", "priority": "High", "category": "Test", "description": "", "due_date": "2025-12-31", "completed": False}]
    save_tasks(test_data, path)
    loaded = load_tasks(path)
    os.unlink(path)
    assert loaded == test_data

    result = load_tasks("bad_example.json")
    assert result == []

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp.write("Bad example")
        bad_path = tmp.name

    result = load_tasks(bad_path)
    os.remove(bad_path)
    assert result == []
