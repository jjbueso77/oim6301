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
    # 1. The Question
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool is for a couple looking to buy a house in Middlesex County, Massachusetts. They have a budget of $700,000 and want to spend less than $8,000 a year on property taxes. The tool will help them find towns that fit both limits and compare their average home values and property tax bills, starting with the cheapest.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. My Plan Before AI
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, I would use the API to get a list of all the towns in Middlesex County.

    Then, I would check how many towns the API says there are to make sure I'm not missing any.

    After that, I would use each town's code to find its property tax information for 2026.

    Next, I would compare the average home value and yearly property tax bill with the couple's budget of $700,000 and $8,000 in taxes.

    I would keep the towns that meet both requirements and organize them from the lowest to the highest property tax bill.

    Finally, I would put everything in a table so the couple can easily compare the towns and see which ones are more affordable.

    Functions: I would need one function to get the towns in a county and another to get their tax information. The first would take the county as an input, and the second would use the town's code and the year. They would return the information needed to compare the towns.

    API addresses: I would use /ma/towns to get the towns and /ma/towns/{dor_code}/history to get their property tax information.

    Checking the data: I would compare the number of towns I collected with the total number of towns reported by the API to make sure I have all of them.

    Checking my calculations: I would take the average home value, multiply it by the residential tax rate, and divide by 1,000. Then I would compare that number with the tax bill reported by the API to see if they match.
    """)
    return


if __name__ == "__main__":
    app.run()
