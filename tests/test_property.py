import pytest

import sys
import os
from hypothesis import given, strategies as st
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tasks import (
    load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, 
    filter_tasks_by_category, filter_tasks_by_completion, search_tasks, get_overdue_tasks
)
from datetime import datetime, timedelta


@given(
    st.lists(
        st.fixed_dictionaries({
            "id": st.integers(min_value=1, max_value=1000)
        })
    )
)
def test_generate_unique_id_property(tasks_list):
    ids = [task["id"] for task in tasks_list]
    if ids:
        assert generate_unique_id(tasks_list) == max(ids) + 1
    else:
        assert generate_unique_id(tasks_list) == 1

@given(
    st.lists(
        st.fixed_dictionaries({
            "priority": st.sampled_from(["Low", "Medium", "High"]),
            "id": st.integers(),
            "title": st.text(),
            "description": st.text(),
            "category": st.text(),
            "due_date": st.dates().map(lambda d: d.strftime("%Y-%m-%d")),
            "completed": st.booleans()
        })
    ),
    st.sampled_from(["Low", "Medium", "High"])
)
def test_filter_tasks_by_priority_property(tasks_list, priority):
    filtered = filter_tasks_by_priority(tasks_list, priority)
    assert all(task["priority"] == priority for task in filtered)

@given(
    st.lists(
        st.fixed_dictionaries({
            "title": st.text(),
            "description": st.text(),
            "priority": st.sampled_from(["Low", "Medium", "High"]),
            "category": st.text(),
            "due_date": st.dates().map(lambda d: d.strftime("%Y-%m-%d")),
            "completed": st.booleans()
        })
    ),
    st.text()
)
def test_search_tasks_property(tasks_list, query):
    result = search_tasks(tasks_list, query)
    for task in result:
        title = task.get("title", "").lower()
        description = task.get("description", "").lower()
        assert query.lower() in title or query.lower() in description

@given(
    st.lists(
        st.fixed_dictionaries({
            "completed": st.booleans(),
            "id": st.integers(),
            "title": st.text(),
            "description": st.text(),
            "priority": st.sampled_from(["Low", "Medium", "High"]),
            "category": st.text(),
            "due_date": st.dates().map(lambda d: d.strftime("%Y-%m-%d")),
        })
    )
)
def test_filter_tasks_by_completion_property(tasks_list):
    filtered = filter_tasks_by_completion(tasks_list, completed=True)
    assert all(task["completed"] is True for task in filtered)

@given(
    st.lists(
        st.fixed_dictionaries({
            "completed": st.booleans(),
            "due_date": st.dates().map(lambda d: d.strftime("%Y-%m-%d")),
            "id": st.integers(),
            "title": st.text(),
            "description": st.text(),
            "priority": st.sampled_from(["Low", "Medium", "High"]),
            "category": st.text(),
        })
    )
)
def test_get_overdue_tasks_property(tasks_list):
    overdue_tasks = get_overdue_tasks(tasks_list)
    today = datetime.now().strftime("%Y-%m-%d")
    for task in overdue_tasks:
        assert task["due_date"] < today
        assert task["completed"] is False
