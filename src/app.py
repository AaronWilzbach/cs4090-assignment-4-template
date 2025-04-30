import streamlit as st
import pandas as pd
import os
import sys
import subprocess
from datetime import datetime
from tasks import (
    load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, 
    filter_tasks_by_category, filter_tasks_by_completion, search_tasks, get_overdue_tasks
)


def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col3:
        filter_search = st.text_input("Search Tasks")
    
    show_completed = st.checkbox("Show Completed Tasks")

    show_overdue = st.checkbox("Show Overdue Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = filter_tasks_by_completion(filtered_tasks, False)
    if filter_search:
        filtered_tasks = search_tasks(filtered_tasks, filter_search)
    if show_overdue:
        filtered_tasks = get_overdue_tasks(filtered_tasks)
    
    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task['title'])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()


    #Developer Tools
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    st.header("Developer Tools")
    if st.button("Run Unit Tests"):
        result = subprocess.run(
            ["pytest", "tests/test_basic.py", "-q"], 
            capture_output=True, 
            text=True, 
            cwd=root
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("All tests passed!")
        else:
            st.error("Some tests failed")
    
    if st.button("Run Tests with Coverage"):
        result = subprocess.run(
            ["pytest", "tests/test_basic.py", "--cov=src", "-q"],
            capture_output=True,
            text=True,
            cwd=root
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("All tests passed with coverage")
        else:
            st.error("Some tests failed")
    
    if st.button("Run Parameterized Tests"):
        result = subprocess.run(
            ["pytest", "tests/test_basic.py", "-k", "test_", "-q"], 
            capture_output=True,
            text=True,
            cwd=root
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("All parameterized tests passed")
        else:
            st.error("Some tests failed")

    if st.button("Run Tests with Mocking"):
        result = subprocess.run(
            ["pytest", "tests/test_advanced.py", "-k", "mock", "-q"], 
            capture_output=True,
            text=True,
            cwd=root
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("All mocking tests passed")
        else:
            st.error("Some tests failed")

    if st.button("Generate HTML Report"):
        result = subprocess.run(
            ["pytest", "tests/test_basic.py", "--html=report.html", "-q"],
            capture_output=True,
            text=True,
            cwd=root
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("HTML report generated")
        else:
            st.error("Failed to generate HTML report")

    #BDD Test Button
    steps = os.path.abspath(os.path.join(root, 'tests', 'feature', 'steps'))
    src_path = os.path.abspath(os.path.join(root, 'src'))
    if st.button('Run BDD Tests'):
        src = os.environ.copy()
        src["PYTHONPATH"] = src_path
        result = subprocess.run(
            ['pytest', '-q'],
            capture_output=True, 
            text=True, 
            cwd=steps, 
            env=src
        )
        st.text(result.stdout)

    #Property based Test Button
    if st.button("Run Hypothesis Tests"):
        result = subprocess.run(
            ["pytest", "tests/test_property.py", "-q"],
            capture_output=True,
            text=True,
            cwd=root
        )
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("All Hypothesis tests passed!")
        else:
            st.error("Some Hypothesis tests failed")



if __name__ == "__main__":
    main()