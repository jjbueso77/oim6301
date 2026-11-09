
# BabsonAI Labs Database

## 1. The Scenario

I chose Scenario A, BabsonAI Labs. The company builds AI tools for small businesses and needs a database to keep track of employees, projects, assignments, tasks, and expenses.

The goal is to organize the data so the company can see who is working on each project, how many hours people are committing, and how much money each project is spending.

## 2. The ERD

```mermaid
erDiagram
    PEOPLE ||--o{ ASSIGNMENTS : works_on
    PROJECTS ||--o{ ASSIGNMENTS : has
    PROJECTS ||--o{ TASKS : contains
    PEOPLE o|--o{ TASKS : assigned_to
    PROJECTS ||--o{ EXPENSES : has
    PEOPLE o|--o{ PEOPLE : manages

    PEOPLE {
        int person_id PK
        string first_name
        string last_name
        string email
        string title
        date start_date
        int manager_id FK
    }

    PROJECTS {
        int project_id PK
        string project_name
        string client_name
        string category
        float budget
        date start_date
        string status
    }

    ASSIGNMENTS {
        int person_id PK,FK
        int project_id PK,FK
        string role
        int hours_per_week
        date joined_date
    }

    TASKS {
        int task_id PK
        int project_id FK
        string description
        date created_date
        int assigned_to FK
        date due_date
        date completed_date
    }

    EXPENSES {
        int expense_id PK
        int project_id FK
        date expense_date
        float amount
        string category
        string note
    }
```

## 3. What One Row Means

- PEOPLE: One row is one employee at BabsonAI Labs.
- PROJECTS: One row is one project the company is working on.
- ASSIGNMENTS: One row shows one employee working on one project, including their role and hours.
- TASKS: One row is one task that belongs to a project.
- EXPENSES: One row is one expense charged to a project.

## 4. Design Choices
