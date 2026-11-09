import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    from pathlib import Path

    database = mo.notebook_dir() / "database.duckdb"
    data_dir = mo.notebook_dir() / "data"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()



    return ask, data_dir, database, duckdb, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # BabsonAI Labs Database

    ## 1. The Tables
    """)
    return


@app.cell
def _(data_dir, database, duckdb):

    import csv

    # Remove the old database so we can rebuild it from scratch
    if database.exists():
        database.unlink()

    with duckdb.connect(database) as _con:

        # PEOPLE
        _con.execute("""
            CREATE TABLE people (
                person_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                email VARCHAR NOT NULL UNIQUE,
                title VARCHAR NOT NULL,
                start_date DATE NOT NULL,
                manager_id INTEGER REFERENCES people(person_id)
            )
        """)

        # PROJECTS
        _con.execute("""
            CREATE TABLE projects (
                project_id INTEGER PRIMARY KEY,
                project_name VARCHAR NOT NULL,
                client_name VARCHAR,
                category VARCHAR NOT NULL CHECK (
                    category IN ('LLM app', 'data pipeline', 'internal tool')
                ),
                budget DECIMAL(12,2) NOT NULL CHECK (budget > 0),
                start_date DATE NOT NULL,
                status VARCHAR NOT NULL CHECK (
                    status IN ('planned', 'active', 'paused', 'done')
                )
            )
        """)

        # ASSIGNMENTS
        _con.execute("""
            CREATE TABLE assignments (
                person_id INTEGER REFERENCES people(person_id),
                project_id INTEGER REFERENCES projects(project_id),
                role VARCHAR NOT NULL,
                hours_per_week INTEGER NOT NULL
                    CHECK (hours_per_week BETWEEN 1 AND 40),
                joined_date DATE NOT NULL,
                PRIMARY KEY (person_id, project_id)
            )
        """)

        # TASKS
        _con.execute("""
            CREATE TABLE tasks (
                task_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(project_id),
                description VARCHAR NOT NULL,
                created_date DATE NOT NULL,
                assigned_to INTEGER REFERENCES people(person_id),
                due_date DATE NOT NULL,
                completed_date DATE,
                CHECK (
                    completed_date IS NULL
                    OR completed_date >= created_date
                )
            )
        """)

        # EXPENSES
        _con.execute("""
            CREATE TABLE expenses (
                expense_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL REFERENCES projects(project_id),
                expense_date DATE NOT NULL,
                amount DECIMAL(12,2) NOT NULL CHECK (amount > 0),
                category VARCHAR NOT NULL CHECK (
                    category IN (
                        'GPU cloud', 'data labeling', 'software', 'travel'
                    )
                ),
                note VARCHAR
            )
        """)

        # Load people one by one because managers reference other people
        with open(data_dir / "people.csv", newline="") as file:
            for row in csv.DictReader(file):
                _con.execute("""
                    INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)
                """, [
                    int(row["person_id"]),
                    row["first_name"],
                    row["last_name"],
                    row["email"],
                    row["title"],
                    row["start_date"],
                    int(row["manager_id"]) if row["manager_id"] else None
                ])

        # Load the remaining CSV files
        for table in ["projects", "assignments", "tasks", "expenses"]:
            file_path = str(data_dir / f"{table}.csv")
            _con.execute(
                f"INSERT INTO {table} "
                f"SELECT * FROM read_csv_auto(?)",
                [file_path]
            )

        # A reusable view for checking project spending
        _con.execute("""
            CREATE VIEW project_spending AS
            SELECT
                p.project_id,
                p.project_name,
                p.budget,
                COALESCE(SUM(e.amount), 0) AS total_expenses,
                COALESCE(SUM(e.amount), 0) / p.budget * 100 AS percent_spent
            FROM projects p
            LEFT JOIN expenses e
                ON p.project_id = e.project_id
            GROUP BY p.project_id, p.project_name, p.budget
        """)

    print("Database created successfully!")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data

    The database uses CSV files generated with Python. It includes employees, projects, assignments, tasks, and expenses.

    Two tasks intentionally break the project assignment rule:
    - Task 10: Person 16 is not assigned to Project 10.
    - Task 20: Person 1 is not assigned to Project 8.

    ## 3. A Look at the Data

    ## 4. Row Counts
    """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT 'people' AS table_name, COUNT(*) AS row_count FROM people
        UNION ALL
        SELECT 'projects', COUNT(*) FROM projects
        UNION ALL
        SELECT 'assignments', COUNT(*) FROM assignments
        UNION ALL
        SELECT 'tasks', COUNT(*) FROM tasks
        UNION ALL
        SELECT 'expenses', COUNT(*) FROM expenses
    """)

    return


@app.cell
def _(data_dir, mo, pl):

    # Read expenses directly from the CSV file
    expense_data = pl.read_csv(data_dir / "expenses.csv")

    # Count expenses by category
    expense_chart = (
        expense_data
        .group_by("category")
        .len()
        .sort("len", descending=True)
    )

    mo.vstack([
        mo.md("### Expenses by Category"),
        mo.ui.altair_chart(
            expense_chart.plot.bar(
                x="category",
                y="len"
            )
        )
    ])

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The chart shows how expenses are divided into four categories. Software has the most expenses, while travel has the fewest. The amounts are pretty close because the data was randomly generated. In a real AI company, I would expect cloud and software expenses to make up a bigger share.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb, mo):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO projects
                VALUES (
                    999, 'Invalid Project', NULL,
                    'LLM app', -5000, '2026-01-01', 'active'
                )
            """)
        refusal = "The database accepted the invalid row."
    except duckdb.ConstraintException as error:
        refusal = str(error).splitlines()[0]

    mo.md(f"**Database response:** {refusal}")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew

    Before running the queries, I expected:

    - 25 employees because I generated 25 people.
    - 12 projects because I created 12 projects.
    - 2 projects with no expenses because I left projects 11 and 12 out of the expense data.
    """)
    return


@app.cell
def _(ask, mo):

    mo.vstack([
        mo.md("**1. Number of employees**"),
        ask("SELECT COUNT(*) AS employees FROM people"),

        mo.md("**2. Number of projects**"),
        ask("SELECT COUNT(*) AS projects FROM projects"),

        mo.md("**3. Projects with no expenses**"),
        ask("""
            SELECT p.project_id, p.project_name
            FROM projects p
            LEFT JOIN expenses e
                ON p.project_id = e.project_id
            WHERE e.expense_id IS NULL
            ORDER BY p.project_id
        """)
    ])

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View

    I created a view called `project_spending` to see how much money each project has spent compared to its budget. This could be useful for the company to check every week.
    """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT *
        FROM project_spending
        ORDER BY percent_spent DESC
    """)

    return


if __name__ == "__main__":
    app.run()
