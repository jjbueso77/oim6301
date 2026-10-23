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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. Inputs
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026

    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. The Work
    """)
    return


@app.cell
def _():
    import requests
    import csv
    import os


    return csv, os, requests


@app.cell
def _(county, requests):
    # Get the towns in Middlesex County
    def get_towns(county):
        reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "per_page": 100},
            timeout=10
        )

        data = reply.json()
        return data["items"]

    towns = get_towns(county)

    print("Towns collected:", len(towns))


    return get_towns, towns


@app.cell
def _(fiscal_year, requests, towns):
    # Get the property tax information for a town
    def get_tax_history(town_code, year):
        reply = requests.get(
            f"https://oim.zhili.dev/ma/towns/{town_code}/history",
            params={"from_year": year, "to_year": year},
            timeout=10
        )

        data = reply.json()
        return data["years"]

    tax_records = []

    for _town in towns:
        _history = get_tax_history(_town["dor_code"], fiscal_year)

        if len(_history) > 0:
            _year = _history[0]

            tax_records.append({
                "town": _town["name"],
                "average_home_value": _year["average_single_family_value_dollars"],
                "tax_rate": _year["residential_rate_per_thousand"],
                "average_tax_bill": _year["average_single_family_bill_dollars"]
            })

    print("Tax records collected:", len(tax_records))



    return (tax_records,)


@app.cell
def _(budget_dollars, tax_limit_dollars, tax_records):
    # Filter and sort the affordable towns
    affordable_towns = []

    for _record in tax_records:
        if _record["average_home_value"] <= budget_dollars:
            if _record["average_tax_bill"] <= tax_limit_dollars:
                affordable_towns.append(_record)

    sorted_towns = []
    remaining = affordable_towns[:]

    while len(remaining) > 0:
        cheapest = remaining[0]
        for _record in remaining:
            if _record["average_tax_bill"] < cheapest["average_tax_bill"]:
                cheapest = _record
        sorted_towns.append(cheapest)
        remaining.remove(cheapest)

    print("Towns that meet both limits:", len(sorted_towns))

    for _record in sorted_towns:
        print(_record["town"], "-", "$" + format(_record["average_tax_bill"], ",.2f"))

    return (sorted_towns,)


@app.cell
def _(csv, os, tax_records):
    # Save the tax records to a CSV file
    os.makedirs("projects/mp2/data", exist_ok=True)

    file_path = "projects/mp2/data/town_taxes.csv"

    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["town", "average_home_value", "tax_rate", "average_tax_bill"]
        )

        writer.writeheader()
        writer.writerows(tax_records)

    print("Saved", len(tax_records), "tax records to CSV")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. The Answer
    """)
    return


@app.cell
def _(county, sorted_towns):
    print(f"{'Town':<18} {'Home Value':>15} {'Tax Bill':>12}")
    print("-" * 48)

    for _record in sorted_towns:
        print(
            f"{_record['town']:<18} "
            f"${_record['average_home_value']:>14,.0f} "
            f"${_record['average_tax_bill']:>11,.0f}"
        )

    print()
    print(f"{len(sorted_towns)} towns in {county} County meet both limits.")

    if len(sorted_towns) > 0:
        print(f"{sorted_towns[0]['town']} has the lowest average tax bill at ${sorted_towns[0]['average_tax_bill']:,.0f}.")
    else:
        print("No towns meet both limits.")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 6. How I Know These Numbers Are Right
    """)
    return


@app.cell
def _(sorted_towns):
    # Check Malden's tax bill using the tax rate
    check_town = sorted_towns[0]

    calculated_tax = (
        check_town["average_home_value"]
        * check_town["tax_rate"] / 1000
    )

    reported_tax = check_town["average_tax_bill"]

    print(f"Calculated tax bill: ${calculated_tax:,.2f}")
    print(f"API tax bill: ${reported_tax:,.2f}")

    difference = abs(calculated_tax - reported_tax)

    print(f"Difference: ${difference:,.2f}")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked Malden's property tax bill by multiplying its average home value by the residential tax rate and dividing by 1,000. I got $4,952.39, while the API reported $4,952. The difference is only 39 cents, which makes sense because the API reports the tax bill in whole dollars. This gives me more confidence that the numbers are correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 7. Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When I was working on Section 4, I asked the Marimo AI agent to simplify my code because I wanted to use things we had already learned in class.

    It gave me a version using basic loops, lists, and if statements, which was easier for me to understand. However, I realized it had removed the functions that were required for the project.

    I went back and added the get_towns and get_tax_history functions while keeping the simpler filtering and sorting code. I then ran everything again and checked that I still got 54 towns, 54 tax records, and 12 towns that met both budget limits.

    The changes are in the first two Python cells under Section 4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 8. Understanding and Testing My Functions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The get_towns function takes the name of a county and gets all the towns in it from the API. It gives me back a list of towns that I can use later in the project.

    The get_tax_history function takes a town's code and a year. It uses those to get the property tax information for that town and returns the data I need.

    Prediction: I think that if I lower the property tax limit from $8,000 to $6,000, fewer towns will qualify since they have to meet a lower limit. Right now 12 towns qualify, but I think that number will drop to 5.
    """)
    return


@app.cell
def _(budget_dollars, sorted_towns, tax_records):
    # Test my prediction with a lower tax limit
    test_limit = 6000
    test_towns = []

    for _town_test in tax_records:
        if _town_test["average_home_value"] <= budget_dollars:
            if _town_test["average_tax_bill"] <= test_limit:
                test_towns.append(_town_test)

    print("Original qualifying towns:", len(sorted_towns))
    print("Qualifying towns with $6,000 limit:", len(test_towns))
    print("My prediction was 5 towns.")
    print("Prediction correct:", len(test_towns) == 5)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After lowering the property tax limit from $8,000 to $6,000, the number of towns that qualified dropped from 12 to 5, just like I predicted. This shows that the filtering works because changing the tax limit changes which towns meet the requirements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 9. Going Further
    """)
    return


@app.cell
def _(get_towns):
    #Try another county
    new_county = "Norfolk"

    new_towns = get_towns(new_county)

    print("County:", new_county)
    print("Towns collected:", len(new_towns))

    for _new_town in new_towns[:5]:
        print(_new_town["name"])

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For Going Further, I wanted to see if I could use the same function with another county instead of Middlesex. I tried Norfolk County, and the function gave me 28 towns. I didn't have to change the function itself, just the county name. This shows that I can reuse the same code for different counties in Massachusetts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 10. Time Spent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I spent approximately 3 hours working on Mini Project 2 outside of class. Most of my time went into writing and testing the code, fixing errors, and checking that the results were correct.
    """)
    return


if __name__ == "__main__":
    app.run()
