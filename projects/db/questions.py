import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # BabsonAI Labs — Part B

    ## Reading It Back: Join Prediction

    For Question 7, I predict that joining tasks with projects and assignments using LEFT JOINs will return 260 rows.

    There are 260 tasks in my database. Each task belongs to one project, and the combination of person_id and project_id is unique in assignments. This means the joins should not duplicate tasks.

    I expect 260 rows, including tasks with no assigned employee and the two tasks that break the assignment rule.
    """)
    return


@app.cell
def _(mo):
    import duckdb
    from pathlib import Path

    database = mo.notebook_dir() / "database.duckdb"
    as_of = "2026-11-08"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    print("Database connection ready!")
    return as_of, ask


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1 — Project Spending vs. Budget

    Which projects have spent the largest share of their budgets?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            project_name,
            budget,
            total_expenses,
            ROUND(percent_spent, 2) AS percent_spent
        FROM project_spending
        ORDER BY percent_spent DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Inventory AI has used the largest share of its budget at 30.68%, followed by Document Search at 18.75%. No project has gone over its budget, but Inventory AI is the one management should monitor most closely.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2 — Overdue Tasks

    Which tasks are overdue and incomplete, and who is responsible for them?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            t.task_id,
            p.project_name,
            t.description,
            t.due_date,
            pe.first_name || ' ' || pe.last_name AS assigned_employee
        FROM tasks t
        JOIN projects p
            ON t.project_id = p.project_id
        LEFT JOIN people pe
            ON t.assigned_to = pe.person_id
        WHERE t.due_date < DATE '{as_of}'
          AND t.completed_date IS NULL
        ORDER BY t.due_date
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are 95 overdue tasks that have not been completed. Six of them do not have an employee assigned. Management should prioritize these tasks and assign someone to the unassigned ones so they do not fall further behind.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3 — Employee Workload

    How many hours per week is each employee committed to active projects, and which employees are above 40 hours?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            pe.first_name || ' ' || pe.last_name AS employee,
            COALESCE(SUM(
                CASE WHEN p.status = 'active'
                    THEN a.hours_per_week
                    ELSE 0
                END
            ), 0) AS total_hours,
            CASE
                WHEN SUM(
                    CASE WHEN p.status = 'active'
                        THEN a.hours_per_week
                        ELSE 0
                    END
                ) > 40 THEN 'Over 40'
                ELSE 'Within limit'
            END AS workload_status
        FROM people pe
        LEFT JOIN assignments a
            ON pe.person_id = a.person_id
        LEFT JOIN projects p
            ON a.project_id = p.project_id
        GROUP BY pe.person_id, pe.first_name, pe.last_name
        ORDER BY total_hours DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Six employees are committed to more than 40 hours per week across active projects. Morgan Davis has the highest workload at 112 hours, followed by Taylor Brown at 109 and Jordan Johnson at 100. Management should consider redistributing some of this work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4 — Expenses by Category

    Which expense categories had total spending above the average category total during the last 90 days?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        WITH category_totals AS (
            SELECT
                category,
                ROUND(SUM(amount), 2) AS total_spent
            FROM expenses
            WHERE expense_date > DATE '{as_of}' - INTERVAL 90 DAY
              AND expense_date <= DATE '{as_of}'
            GROUP BY category
        )
        SELECT
            category,
            total_spent
        FROM category_totals
        WHERE total_spent > (
            SELECT AVG(total_spent)
            FROM category_totals
        )
        ORDER BY total_spent DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Software and GPU cloud were the only two expense categories above the average category total over the last 90 days. Software had the highest spending at $21,543.13, followed by GPU cloud at $18,811.86. Management should monitor these costs to keep spending under control.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5 — Projects Without Expenses

    Which projects have no expenses recorded?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.project_id,
            p.project_name,
            p.status
        FROM projects p
        LEFT JOIN expenses e
            ON p.project_id = e.project_id
        WHERE e.expense_id IS NULL
        ORDER BY p.project_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Internal Reporting and HR Assistant are the only two projects with no recorded expenses. HR Assistant is still active, so management should check whether costs are being recorded correctly. Internal Reporting is already completed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 6 — Project Tasks and Expenses

    How many tasks does each project have, and how much has each project spent?
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH task_counts AS (
            SELECT project_id, COUNT(*) AS total_tasks
            FROM tasks
            GROUP BY project_id
        ),
        expense_totals AS (
            SELECT project_id, SUM(amount) AS total_expenses
            FROM expenses
            GROUP BY project_id
        )
        SELECT
            p.project_name,
            COALESCE(t.total_tasks, 0) AS total_tasks,
            COALESCE(e.total_expenses, 0) AS total_expenses
        FROM projects p
        LEFT JOIN task_counts t
            ON p.project_id = t.project_id
        LEFT JOIN expense_totals e
            ON p.project_id = e.project_id
        ORDER BY p.project_id
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            (SELECT COUNT(*) FROM tasks) AS total_tasks,
            (SELECT SUM(amount) FROM expenses) AS total_expenses,
            (SELECT COUNT(*) FROM projects) AS total_projects
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.project_name,
            (SELECT COUNT(*)
             FROM tasks t
             WHERE t.project_id = p.project_id) AS checked_tasks,
            COALESCE(
                (SELECT SUM(e.amount)
                 FROM expenses e
                 WHERE e.project_id = p.project_id), 0
            ) AS checked_expenses
        FROM projects p
        ORDER BY p.project_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The database has 260 tasks across 12 projects, with $195,138.12 in total expenses. I checked each project's task count and expenses separately, and the results matched the original query. This confirms the joins did not double-count tasks or expenses.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 7 — Task Assignment Rule

    Are all tasks assigned to employees who actually work on their projects? Which tasks break this rule?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            t.task_id,
            p.project_name,
            t.assigned_to,
            a.person_id AS matching_assignment
        FROM tasks t
        LEFT JOIN projects p
            ON t.project_id = p.project_id
        LEFT JOIN assignments a
            ON t.project_id = a.project_id
            AND t.assigned_to = a.person_id
        ORDER BY t.task_id
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT COUNT(*) AS actual_rows
        FROM tasks t
        LEFT JOIN projects p
            ON t.project_id = p.project_id
        LEFT JOIN assignments a
            ON t.project_id = a.project_id
            AND t.assigned_to = a.person_id
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            t.task_id,
            p.project_name,
            t.assigned_to AS employee_id
        FROM tasks t
        JOIN projects p
            ON t.project_id = p.project_id
        LEFT JOIN assignments a
            ON t.project_id = a.project_id
            AND t.assigned_to = a.person_id
        WHERE t.assigned_to IS NOT NULL
          AND a.person_id IS NULL
        ORDER BY t.task_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The join returned 260 rows, exactly as I predicted. There were two violations: Task 10 and Task 20 were assigned to employees who were not working on their projects. Unassigned tasks were excluded because they are allowed.

    The row count matched because each task belongs to one project and can match at most one employee-project assignment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 8 — Manager Workload

    How many employees report directly to each manager, and how many weekly project hours have those employees committed?
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH employee_hours AS (
            SELECT
                person_id,
                SUM(hours_per_week) AS total_hours
            FROM assignments
            GROUP BY person_id
        )
        SELECT
            m.first_name || ' ' || m.last_name AS manager,
            COUNT(e.person_id) AS direct_reports,
            COALESCE(SUM(h.total_hours), 0) AS team_weekly_hours
        FROM people m
        JOIN people e
            ON e.manager_id = m.person_id
        LEFT JOIN employee_hours h
            ON e.person_id = h.person_id
        GROUP BY m.person_id, m.first_name, m.last_name
        ORDER BY team_weekly_hours DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Alex Smith has the highest team workload, with 7 direct reports committing a total of 626 hours per week. Casey Wilson also has 7 direct reports, but their team has 408 hours. Management should review how work is distributed between these teams.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 9 — Incomplete Tasks on Active Projects

    Which active projects have the most incomplete tasks, and where should management prioritize its attention?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.project_name,
            COUNT(t.task_id) AS total_tasks,
            COUNT(t.task_id) FILTER (
                WHERE t.completed_date IS NULL
            ) AS incomplete_tasks,
            ROUND(
                100.0 * COUNT(t.task_id) FILTER (
                    WHERE t.completed_date IS NULL
                ) / NULLIF(COUNT(t.task_id), 0), 2
            ) AS incomplete_percentage
        FROM projects p
        LEFT JOIN tasks t
            ON p.project_id = t.project_id
        WHERE p.status = 'active'
        GROUP BY p.project_id, p.project_name
        ORDER BY incomplete_tasks DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Recommendation Tool has the most incomplete tasks, with 11 out of 22 still unfinished (50%). Financial Forecasting and Sales Dashboard each have 10 incomplete tasks. Management should prioritize Recommendation Tool and review the progress of these other two projects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 10 — Staffing on Active Projects

    Which active projects have the fewest employees assigned, and how many weekly hours are committed to them?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.project_name,
            COUNT(a.person_id) AS employees_assigned,
            COALESCE(SUM(a.hours_per_week), 0) AS weekly_hours
        FROM projects p
        LEFT JOIN assignments a
            ON p.project_id = a.project_id
        WHERE p.status = 'active'
        GROUP BY p.project_id, p.project_name
        ORDER BY employees_assigned ASC, weekly_hours ASC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    HR Assistant and Recommendation Tool have the fewest employees assigned, with 5 each. HR Assistant has 92 weekly hours committed, while Recommendation Tool has 99. Since Recommendation Tool also has the most incomplete tasks among active projects, management should review whether it needs additional staffing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    I checked Question 6 by counting tasks and adding expenses separately for each project. I also checked Question 7 by comparing the number of rows from the joins with the original tasks table.
    """)
    return


@app.cell
def _(ask):
    check = ask("""
        WITH task_counts AS (
            SELECT project_id, COUNT(*) AS n
            FROM tasks GROUP BY project_id
        ),
        expense_totals AS (
            SELECT project_id, SUM(amount) AS total
            FROM expenses GROUP BY project_id
        )
        SELECT
            COUNT(*) AS projects_checked,
            COUNT(*) FILTER (
                WHERE COALESCE(t.n, 0) !=
                    (SELECT COUNT(*) FROM tasks x
                     WHERE x.project_id = p.project_id)
                OR COALESCE(e.total, 0) !=
                    COALESCE((SELECT SUM(amount) FROM expenses x
                     WHERE x.project_id = p.project_id), 0)
            ) AS mismatches
        FROM projects p
        LEFT JOIN task_counts t ON p.project_id = t.project_id
        LEFT JOIN expense_totals e ON p.project_id = e.project_id
    """)

    print(check)
    assert check["mismatches"][0] == 0, "Verification failed!"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The automated check compared each project's task count and total expenses using two different methods. All 12 projects matched, with zero discrepancies.
    """)
    return


@app.cell
def _(as_of, ask):
    original_count = ask(f"""
        SELECT COUNT(*) AS total
        FROM tasks t
        JOIN projects p ON t.project_id = p.project_id
        LEFT JOIN people pe ON t.assigned_to = pe.person_id
        WHERE t.due_date < DATE '{as_of}'
          AND t.completed_date IS NULL
    """)["total"][0]

    independent_count = ask(f"""
        SELECT COUNT(*) AS total
        FROM tasks
        WHERE completed_date IS NULL
          AND due_date < DATE '{as_of}'
    """)["total"][0]

    print("Question 2 result:", original_count)
    print("Independent check:", independent_count)

    assert original_count == independent_count, "Counts do not match!"
    print("Verification passed!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I also checked Question 2 by counting overdue and incomplete tasks directly from the tasks table. Both methods returned 95 tasks, confirming that the joins did not change the count.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    For Question 3, the first AI-generated query could have included hours from projects that were not active. I used a CASE WHEN condition to count hours only when the project's status was active.

    I checked the corrected query by reviewing the SQL and its results. It returned all 25 employees and identified six employees with more than 40 weekly hours on active projects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    Before running Question 7, I predicted that joining tasks with projects and assignments using LEFT JOINs would return 260 rows.

    The query returned exactly 260 rows, so my prediction was correct.

    This happened because each task belongs to one project, and the combination of person_id and project_id is unique in assignments. The LEFT JOINs also kept tasks with no matching assignment, so no tasks were lost or duplicated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Going Further

    I created a chart to make it easier to see which employees have the highest workloads across active projects. This helps management quickly identify employees who may have too much work assigned.
    """)
    return


@app.cell
def _(ask, mo):
    workload_chart_data = ask("""
        SELECT
            pe.first_name || ' ' || pe.last_name AS employee,
            SUM(a.hours_per_week) AS weekly_hours
        FROM people pe
        JOIN assignments a ON pe.person_id = a.person_id
        JOIN projects p ON a.project_id = p.project_id
        WHERE p.status = 'active'
        GROUP BY pe.person_id, pe.first_name, pe.last_name
        ORDER BY weekly_hours DESC
        LIMIT 10
    """)

    workload_chart = workload_chart_data.plot.bar(
        x="employee",
        y="weekly_hours"
    ).properties(
        title="Top 10 Employees by Weekly Workload"
    )

    mo.ui.altair_chart(workload_chart)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The chart shows that Morgan Davis, Taylor Brown, and Jordan Johnson have the highest weekly workloads. All three are committed to more than 100 hours per week across active projects. This makes it easier for management to see where workloads may need to be redistributed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Time Spent

    I spent approximately 6.5 hours outside of class working on Parts A and B combined.
    """)
    return


if __name__ == "__main__":
    app.run()
