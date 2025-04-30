import pytest

import sys
import os
import json
from unittest import mock
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from tasks import (
    load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, 
    filter_tasks_by_category, filter_tasks_by_completion, search_tasks, get_overdue_tasks
)


@pytest.fixture
def sample_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        {"id": 1, "title": "Task 1", "description": "Finish Assignment", "priority": "High", "category": "Work", "due_date": today, "completed": False},
        {"id": 2, "title": "Task 2", "description": "Cook Dinner", "priority": "Low", "category": "Personal", "due_date": today, "completed": True},
        {"id": 3, "title": "Task 3", "description": "Write Report", "priority": "Medium", "category": "Work", "due_date": today, "completed": False}
    ]

@pytest.fixture
def mock_load_save():
    with mock.patch("tasks.load_tasks") as mock_load, mock.patch("tasks.save_tasks") as mock_save:
        yield mock_load, mock_save

def test_generate_unique_id_with_mock(mock_load_save, sample_tasks):
    mock_load, mock_save = mock_load_save
    mock_load.return_value = sample_tasks

    new_id = generate_unique_id(sample_tasks)
    assert new_id == 4

def test_filter_tasks_by_priority_with_mock(mock_load_save, sample_tasks):
    mock_load, mock_save = mock_load_save
    mock_load.return_value = sample_tasks

    filtered = filter_tasks_by_priority(sample_tasks, "High")
    assert len(filtered) == 1
    assert filtered[0]['title'] == "Task 1"

def test_filter_tasks_by_category_with_mock(mock_load_save, sample_tasks):
    mock_load, mock_save = mock_load_save
    mock_load.return_value = sample_tasks

    filtered = filter_tasks_by_category(sample_tasks, "Work")
    assert len(filtered) == 2

def test_filter_tasks_by_completion_with_mock(mock_load_save, sample_tasks):
    mock_load, mock_save = mock_load_save
    mock_load.return_value = sample_tasks

    filtered = filter_tasks_by_completion(sample_tasks, completed=False)
    assert len(filtered) == 2

def test_search_tasks_with_mock(mock_load_save, sample_tasks):
    mock_load, mock_save = mock_load_save
    mock_load.return_value = sample_tasks

    results = search_tasks(sample_tasks, "Write Report")
    assert len(results) == 1
    assert results[0]["title"] == "Task 3"

def test_get_overdue_tasks_with_mock(mock_load_save):
    mock_load, mock_save = mock_load_save

    overdue_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tasks = [
        {"id": 1, "title": "Overdue Task", "description": "", "priority": "High", "category": "Work", "due_date": overdue_date, "completed": False}
    ]
    mock_load.return_value = tasks

    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 1

def test_load_and_save_tasks_with_mock(mock_load_save):
    mock_load, mock_save = mock_load_save
    test_data = [{"id": 1, "title": "Save Test", "description": "", "priority": "High", "category": "Test", "due_date": "2025-05-28", "completed": False}]
    
    mock_save.return_value = None
    save_tasks(test_data)
    
    mock_load.return_value = test_data
    loaded = load_tasks("tasks.json")
    assert loaded == test_data

def test_load_tasks_incorrect_format_with_mock(mock_load_save):
    mock_load, mock_save = mock_load_save
    mock_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)
    
    result = load_tasks("incorrect_format.json")
    assert result == []

