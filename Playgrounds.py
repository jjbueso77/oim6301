import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    charge = 10
    return (charge,)


@app.cell
def _(charge):
    print (charge)
    return


@app.cell
def _():
    return


@app.cell
def _():
    csv_text = """product_id,name,price
    1,Notebook,3.50
    2,Pen,1.20
    3,Backpack,25.00
    4,Water Bottle,8.75
    5,Desk Lamp,15.20
    6,Headphones,45.00
    7,Mouse,12.50
    8,Keyboard,22.00
    9,Monitor,150.00
    10,Charger,9.99
    """

    with open("products.csv", "w") as file:
        file.write(csv_text)
    return


@app.cell
def _():
    products = []

    with open("products.csv", "r") as file:
        lines = file.readlines()

    for line in lines[1:]:
        parts = line.strip().split(",")
        product = {"product_id": parts[0], "name": parts[1], "price": float(parts[2])}
        products.append(product)

    products
    return


if __name__ == "__main__":
    app.run()
