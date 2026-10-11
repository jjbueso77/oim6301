# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A financial advisor could use this tool to help a client rebalance their stock portfolio. It calculates how many shares should be bought or sold to get closer to the target allocation while making sure there is enough cash available.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, I would calculate how much each stock is worth by multiplying the number of shares by its price.

    Then, I would add everything together, including the cash, to find the total value of the portfolio.

    Next, I would use the target percentages to figure out how much money should be invested in each stock.

    After that, I would calculate how many whole shares I should have and compare that to what I currently own.

    I would then figure out which stocks I need to buy or sell and how much cash I have left.

    Finally, I would check how close the new portfolio is to the target percentages.

    1. What does my loop carry from one step to the next?

    The loop would go through each stock one at a time and keep adding its value to a running total. Later, I would use a loop to calculate the shares needed for each stock.

    2. Which check will I use in Section 6?

    I would compare the total portfolio value before and after rebalancing. Since there are no trading fees, both numbers should be the same. This would help me check that my calculations are correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    cash = 5000.00
    target_weights = {"AAPL": 0.20, "MSFT": 0.20, "GOOG": 0.15,
                      "AMZN": 0.15, "NVDA": 0.15, "TSLA": 0.15}# Your inputs.
    return cash, holdings, target_weights


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(cash, holdings):
    # Total Portfolio Value

    total_value = cash
    for ticker, shares, price in holdings:
        total_value = total_value + shares * price

    total_value
    return (total_value,)


@app.cell
def _(holdings, target_weights, total_value):

    results = []
    invested_value = 0

    for stock_ticker, stock_shares, stock_price in holdings:
        weight = target_weights[stock_ticker]
        target_dollars = total_value * weight
        target_shares = int(target_dollars // stock_price)
        trade = target_shares - stock_shares
        value_after = target_shares * stock_price
        invested_value = invested_value + value_after
        weight_after = value_after / total_value

        row = {
            "ticker": stock_ticker,
            "shares_now": stock_shares,
            "shares_target": target_shares,
            "trade": trade,
            "value_after": value_after,
            "weight_after": weight_after
        }

        results.append(row)

    cash_left = total_value - invested_value
    cash_weight = cash_left / total_value

    results.append({
        "ticker": "CASH",
        "shares_now": None,
        "shares_target": None,
        "trade": None,
        "value_after": cash_left,
        "weight_after": cash_weight
    })

    print(f"Cash remaining: ${cash_left:,.2f}")

    return cash_left, results


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(cash_left, results):

    print(f"{'Ticker':<8} {'Now':>8} {'Target':>8} {'Trade':>8} {'Value After':>16} {'Weight':>9}")
    print("-" * 65)

    for answer_row in results:
        if answer_row["shares_now"] is None:
            print(f"{'CASH':<8} {'-':>8} {'-':>8} {'-':>8} ${answer_row['value_after']:>14,.2f} {answer_row['weight_after']*100:>8.1f}%")
        else:
            print(f"{answer_row['ticker']:<8} {answer_row['shares_now']:>8} {answer_row['shares_target']:>8} {answer_row['trade']:>+8} ${answer_row['value_after']:>14,.2f} {answer_row['weight_after']*100:>8.1f}%")

    print()
    print(f"Cash remaining: ${cash_left:,.2f}")


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(cash_left, results, total_value):
    value_after_total = cash_left
    for check_row in results:
        if check_row["shares_now"] is not None:
            value_after_total = value_after_total + check_row["value_after"]

    print(f"Total before: ${total_value:,.2f}")
    print(f"Total after:  ${value_after_total:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When I was working on Section 4, the AI gave me code that reused variables like `ticker`, `shares`, and `price` from another cell. Marimo wouldn't run it because those variables were already defined. I changed their names to `stock_ticker`, `stock_shares`, and `stock_price`, and that fixed the issue.

    I also had a problem in Section 5 because the AI included explanations and Markdown inside a Python code cell. I removed that extra text and kept only the Python code.

    I knew what needed to be changed because Marimo showed error messages, and I used those messages to identify the problems. After making the changes, I checked that the code ran and produced the portfolio results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(holdings, target_weights, total_value):
    trade_fee = 5.00
    min_trade_value = 500

    results_fees = []
    invested_value_fees = 0
    total_fees = 0

    for fee_ticker, fee_shares, fee_price in holdings:
        fee_weight = target_weights[fee_ticker]
        fee_target_dollars = total_value * fee_weight
        fee_target_shares = int(fee_target_dollars // fee_price)
        fee_trade = fee_target_shares - fee_shares
        trade_value = abs(fee_trade) * fee_price

        if trade_value < min_trade_value:
            final_shares = fee_shares
            executed_trade = 0
        else:
            final_shares = fee_target_shares
            executed_trade = fee_trade
            total_fees = total_fees + trade_fee

        value_after_fee = final_shares * fee_price
        invested_value_fees = invested_value_fees + value_after_fee

        row_fee = {
            "ticker": fee_ticker,
            "shares_now": fee_shares,
            "shares_target": fee_target_shares,
            "trade": executed_trade,
            "value_after": value_after_fee,
        }
        results_fees.append(row_fee)

    cash_left_fees = total_value - invested_value_fees - total_fees
    total_value_after_fees = invested_value_fees + cash_left_fees



    return cash_left_fees, results_fees, total_fees, total_value_after_fees


@app.cell
def _(
    cash_left_fees,
    results_fees,
    target_weights,
    total_fees,
    total_value_after_fees,
):
    print(f"{'Ticker':<8} {'Trade':>8} {'Value After':>16} {'Weight':>9} {'Target':>8} {'Gap (pts)':>10}")
    print("-" * 70)

    for fee_row in results_fees:
        weight_after_fee = fee_row["value_after"] / total_value_after_fees
        target = target_weights[fee_row["ticker"]]
        gap = abs(weight_after_fee - target) * 100
        print(f"{fee_row['ticker']:<8} {fee_row['trade']:>+8} ${fee_row['value_after']:>14,.2f} "
              f"{weight_after_fee*100:>8.1f}% {target*100:>7.1f}% {gap:>9.2f}")

    print()
    print(f"Total fees paid: ${total_fees:,.2f}")
    print(f"Cash remaining: ${cash_left_fees:,.2f}")
    return


if __name__ == "__main__":
    app.run()
