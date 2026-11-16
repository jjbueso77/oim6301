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


if __name__ == "__main__":
    app.run()
