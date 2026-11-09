
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

DATA = Path(__file__).resolve().parent / "data"
DATA.mkdir(exist_ok=True)
AS_OF = date(2026, 11, 8)


def save_csv(filename, columns, rows):
    with open(DATA / filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)
    print(f"{filename}: {len(rows)} rows")


def random_date(start, end):
    days = (end - start).days
    return start + timedelta(days=random.randint(0, max(0, days)))


# 1. Employees
first_names = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey",
    "Jamie", "Avery", "Riley", "Cameron", "Drew",
    "Sam", "Charlie", "Robin", "Parker", "Quinn",
    "Blake", "Reese", "Logan", "Skyler", "Hayden",
    "Emerson", "Rowan", "Finley", "Dakota", "Elliot"
]

last_names = [
    "Smith", "Johnson", "Brown", "Davis", "Wilson",
    "Miller", "Anderson", "Thomas", "Moore", "Martin",
    "Lee", "White", "Clark", "Lewis", "Walker",
    "Hall", "Young", "Allen", "King", "Wright",
    "Scott", "Green", "Baker", "Adams", "Nelson"
]

people = []
for i in range(1, 26):
    title = "Founder" if i <= 2 else random.choice(
        ["Data Analyst", "Engineer", "Designer", "Project Manager"]
    )
    manager = "" if i <= 2 else random.randint(1, min(i - 1, 5))
    start = date(2023, 1, 1) + timedelta(days=i * 25)
    people.append([
        i, first_names[i - 1], last_names[i - 1],
        f"{first_names[i - 1].lower()}.{last_names[i - 1].lower()}@babsonai.com",
        title, start.isoformat(), manager
    ])

save_csv(
    "people.csv",
    ["person_id", "first_name", "last_name", "email",
     "title", "start_date", "manager_id"],
    people
)


# 2. Projects
project_names = [
    "Customer Chatbot", "Sales Dashboard", "Inventory AI",
    "Marketing Assistant", "Document Search", "Data Pipeline",
    "Customer Analytics", "Recommendation Tool", "Support Bot",
    "Financial Forecasting", "Internal Reporting", "HR Assistant"
]

projects = []
project_dates = {}

for i, name in enumerate(project_names, 1):
    start = date(2025, 11, 8) + timedelta(days=(i - 1) * 24)
    project_dates[i] = start

    projects.append([
        i, name,
        "" if i in (11, 12) else f"Client {i}",
        random.choice(["LLM app", "data pipeline", "internal tool"]),
        random.randint(50000, 200000),
        start.isoformat(),
        random.choice(["planned", "active", "paused", "done"])
    ])

save_csv(
    "projects.csv",
    ["project_id", "project_name", "client_name",
     "category", "budget", "start_date", "status"],
    projects
)


# 3. Employee assignments
assignments = []
team_members = {}
joined_dates = {}

for project_id in range(1, 13):
    team = random.sample(range(1, 26), random.randint(5, 8))
    team_members[project_id] = team

    for person_id in team:
        joined = project_dates[project_id] + timedelta(
            days=random.randint(0, 10)
        )
        joined_dates[(person_id, project_id)] = joined

        assignments.append([
            person_id,
            project_id,
            random.choice(["Developer", "Analyst", "Lead", "Designer"]),
            random.randint(5, 40),
            joined.isoformat()
        ])

save_csv(
    "assignments.csv",
    ["person_id", "project_id", "role",
     "hours_per_week", "joined_date"],
    assignments
)


# 4. Tasks
tasks = []
bad_assignments = []

for task_id in range(1, 261):
    project_id = ((task_id - 1) % 12) + 1
    team = team_members[project_id]

    # Two intentional rule violations for Part B
    if task_id in (10, 20):
        outsiders = [p for p in range(1, 26) if p not in team]
        assigned_to = random.choice(outsiders)
        bad_assignments.append((task_id, project_id, assigned_to))
        earliest = project_dates[project_id]
    elif task_id % 17 == 0:
        assigned_to = ""
        earliest = project_dates[project_id]
    else:
        assigned_to = random.choice(team)
        earliest = joined_dates[(assigned_to, project_id)]

    created = random_date(earliest, AS_OF)
    due = created + timedelta(days=random.randint(7, 30))

    completed = ""
    if random.random() < 0.55:
        latest = min(due, AS_OF)
        completed = random_date(created, latest).isoformat()

    tasks.append([
        task_id, project_id, f"Complete project task {task_id}",
        created.isoformat(), assigned_to,
        due.isoformat(), completed
    ])

save_csv(
    "tasks.csv",
    ["task_id", "project_id", "description",
     "created_date", "assigned_to", "due_date", "completed_date"],
    tasks
)


# 5. Expenses
expenses = []

for expense_id in range(1, 161):
    # Projects 11 and 12 intentionally have no expenses
    project_id = ((expense_id - 1) % 10) + 1

    expense_date = random_date(project_dates[project_id], AS_OF)

    expenses.append([
        expense_id,
        project_id,
        expense_date.isoformat(),
        round(random.uniform(100, 2500), 2),
        random.choice([
            "GPU cloud", "data labeling", "software", "travel"
        ]),
        f"Project expense {expense_id}"
    ])

save_csv(
    "expenses.csv",
    ["expense_id", "project_id", "expense_date",
     "amount", "category", "note"],
    expenses
)


print("\nIntentional rule violations:")
for task_id, project_id, person_id in bad_assignments:
    print(
        f"Task {task_id}: Person {person_id} "
        f"is not assigned to Project {project_id}"
    )

print("\nData generation complete!")
