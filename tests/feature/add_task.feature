Feature: Task Management

  Scenario: Load tasks when the file exists
    Given there are tasks in the tasks file
    When I load the tasks
    Then I should see a list of tasks

  Scenario: Add a new task with unique ID
    Given the tasks list is empty
    When I add a task with title "New Task"
    Then the task should have an ID of 1

  Scenario: Filter tasks by priority
    Given there are tasks with different priorities
    When I filter tasks by "High" priority
    Then I should see only tasks with "High" priority

  Scenario: Filter tasks by category
    Given there are tasks with different categories
    When I filter tasks by "Work" category
    Then I should see only tasks with "Work" category

  Scenario: Get overdue tasks
    Given there are tasks with overdue due dates
    When I check for overdue tasks
    Then I should see only tasks that are overdue and not completed


