# PROJECT- PRODUCT INVENTORY & SALES MANAGEMENT SYSTEM


from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)


# ================= DATABASE =================

def create_database():

    conn = sqlite3.connect("tanayara.db")

    # Products table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Purchase price column
    columns = conn.execute(
        "PRAGMA table_info(products)"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "purchase_price" not in column_names:

        conn.execute("""
            ALTER TABLE products
            ADD COLUMN purchase_price REAL DEFAULT 0
        """)


    # Sales table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL
        )
    """)

    # Profit column
    sales_columns = conn.execute(
        "PRAGMA table_info(sales)"
    ).fetchall()

    sales_column_names = [column[1] for column in sales_columns]

    if "profit" not in sales_column_names:

        conn.execute("""
            ALTER TABLE sales
            ADD COLUMN profit REAL DEFAULT 0
        """)

    conn.commit()
    conn.close()


# ================= HOME =================

@app.route("/")
def home():

    conn = sqlite3.connect("tanayara.db")


    # Products
    products = conn.execute("""
        SELECT
            id,
            name,
            size,
            price,
            stock,
            purchase_price
        FROM products
        ORDER BY id DESC
    """).fetchall()


    # Sales 
   # Sales
    sales = conn.execute("""
    SELECT
      sales.id,
    sales.customer,
    products.name,
     products.size,
    sales.quantity,
    sales.total,
    sales.profit
  FROM sales
    JOIN products
    ON sales.product_id = products.id
    ORDER BY sales.id DESC
""").fetchall()


    # ================= DASHBOARD =================

    total_products = conn.execute("""
        SELECT COUNT(*)
        FROM products
    """).fetchone()[0]


    total_stock = conn.execute("""
        SELECT COALESCE(SUM(stock), 0)
        FROM products
    """).fetchone()[0]


    total_sales = conn.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM sales
    """).fetchone()[0]


    total_orders = conn.execute("""
        SELECT COUNT(*)
        FROM sales
    """).fetchone()[0]


    total_profit = conn.execute("""
        SELECT COALESCE(SUM(profit), 0)
        FROM sales
    """).fetchone()[0]


    low_stock = conn.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE stock <= 10
    """).fetchone()[0]


    conn.close()


    # ================= PRODUCT LIST =================

    product_list = ""

    for product in products:

        product_id = product[0]
        name = product[1]
        size = product[2]
        selling_price = product[3]
        stock = product[4]
        purchase_price = product[5] or 0


        if stock <= 10:

            stock_html = f"""
            <span style="color:red;font-weight:bold;">
                {stock}
            </span>
            """

        else:

            stock_html = str(stock)


        product_list += f"""
        <tr>

            <td>{name}</td>

            <td>{size}</td>

            <td>₹{purchase_price}</td>

            <td>₹{selling_price}</td>

            <td>{stock_html}</td>

        </tr>
        """


   # ================= SALES LIST =================

    sales_list = ""

    for sale in sales:

        sales_list += f"""
        <tr>

            <td>{sale[1]}</td>

            <td>{sale[2]}</td>

            <td>{sale[3]}</td>

            <td>{sale[4]}</td>

            <td>₹{sale[5]}</td>

            <td style="color:green;font-weight:bold;">
                ₹{sale[6]}
            </td>

            <td>
                <form action="/delete-sale/{sale[0]}" method="POST"
                onsubmit="return confirm('Delete this sale?');">

                    <button type="submit" style="background:red;">
                        Delete
                    </button>

                </form>
            </td>

        </tr>
        """

    # ================= HTML =================

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>PRODUCT INVENTORY & SALES MANAGEMENT SYSTEM</title>

        <style>

            body {{
                margin: 0;
                font-family: Arial;
                background: #f4f6f8;
            }}

            .header {{
                background: #222;
                color: white;
                padding: 20px;
                text-align: center;
            }}

            .container {{
                padding: 25px;
            }}

            .dashboard {{
                display: grid;
                grid-template-columns: repeat(6, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }}

            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }}

            .stat-card h3 {{
                margin: 0;
                color: #555;
                font-size: 14px;
            }}

            .stat-card h2 {{
                margin-top: 10px;
            }}

            .profit {{
                color: green;
            }}

            .low-stock {{
                color: red;
            }}

            .card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }}

            input, select {{
                padding: 10px;
                margin: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}

            button {{
                padding: 10px 18px;
                background: #222;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}

            button:hover {{
                background: #444;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}

            th {{
                background: #eee;
            }}

        </style>

    </head>


    <body>


        <div class="header">

            <h1>Product Inventory & sales Management system</h1>

            <p>Business Management System</p>

        </div>


        <div class="container">


            <!-- ================= DASHBOARD ================= -->

            <div class="dashboard">


                <div class="stat-card">

                    <h3>Total Products</h3>

                    <h2>
                        {total_products}
                    </h2>

                </div>


                <div class="stat-card">

                    <h3>Total Stock</h3>

                    <h2>
                        {total_stock}
                    </h2>

                </div>


                <div class="stat-card">

                    <h3>Total Sales</h3>

                    <h2>
                        ₹{total_sales:.2f}
                    </h2>

                </div>


                <div class="stat-card">

                    <h3>Total Orders</h3>

                    <h2>
                        {total_orders}
                    </h2>

                </div>


                <div class="stat-card">

                    <h3>Total Profit</h3>

                    <h2 class="profit">
                        ₹{total_profit:.2f}
                    </h2>

                </div>


                <div class="stat-card">

                    <h3>Low Stock</h3>

                    <h2 class="low-stock">
                        {low_stock}
                    </h2>

                </div>


            </div>


            <!-- ================= ADD PRODUCT ================= -->

            <div class="card">

                <h2>Add Product</h2>

                <form action="/add-product" method="POST">

                    <input
                        type="text"
                        name="name"
                        placeholder="Product Name"
                        required
                    >

                    <input
                        type="text"
                        name="size"
                        placeholder="Size (1L / 500ml)"
                        required
                    >

                    <input
                        type="number"
                        step="0.01"
                        name="purchase_price"
                        placeholder="Purchase Price"
                        required
                    >

                    <input
                        type="number"
                        step="0.01"
                        name="price"
                        placeholder="Selling Price"
                        required
                    >

                    <input
                        type="number"
                        name="stock"
                        placeholder="Stock Quantity"
                        min="1"
                        required
                    >

                    <button type="submit">
                        Add Product
                    </button>

                </form>

            </div>


            <!-- ================= MAKE SALE ================= -->

            <div class="card">

                <h2>Make Sale</h2>

                <form action="/make-sale" method="POST">

                    <input
                        type="text"
                        name="customer"
                        placeholder="Customer Name"
                        required
                    >


                    <select name="product_id" required>

                        <option value="">
                            Select Product
                        </option>

                        {"".join(
                            f'<option value="{p[0]}">{p[1]} - {p[2]} - ₹{p[3]} (Stock: {p[4]})</option>'
                            for p in products
                        )}

                    </select>


                    <input
                        type="number"
                        name="quantity"
                        placeholder="Quantity"
                        min="1"
                        required
                    >


                    <button type="submit">
                        Complete Sale
                    </button>

                </form>

            </div>


            <!-- ================= PRODUCTS ================= -->

            <div class="card">

                <h2>Products</h2>

                <table>

                    <tr>

                        <th>Product Name</th>
                        <th>Size</th>
                        <th>Purchase Price</th>
                        <th>Selling Price</th>
                        <th>Stock</th>

                    </tr>

                    {product_list}

                </table>

            </div>


            <!-- ================= SALES HISTORY ================= -->

            <div class="card">

                <h2>Sales History</h2>

                <table>

                    <tr>

                        <th>Customer</th>
                        <th>Product</th>
                        <th>Size</th>
                        <th>Quantity</th>
                        <th>Total Sale</th>
                        <th>Profit</th>
                        <th>Delete</th>

                    </tr>

                    {sales_list}

                </table>

            </div>


        </div>

    </body>

    </html>
    """


# ================= ADD PRODUCT =================

@app.route("/add-product", methods=["POST"])
def add_product():

    name = request.form["name"]

    size = request.form["size"]

    purchase_price = float(
        request.form["purchase_price"]
    )

    selling_price = float(
        request.form["price"]
    )

    stock = int(
        request.form["stock"]
    )


    conn = sqlite3.connect("tanayara.db")


    conn.execute("""
        INSERT INTO products
        (name, size, price, stock, purchase_price)

        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        size,
        selling_price,
        stock,
        purchase_price
    ))


    conn.commit()

    conn.close()

    return redirect("/")


# ================= MAKE SALE =================

@app.route("/make-sale", methods=["POST"])
def make_sale():

    customer = request.form["customer"]

    product_id = int(
        request.form["product_id"]
    )

    quantity = int(
        request.form["quantity"]
    )


    conn = sqlite3.connect("tanayara.db")


    product = conn.execute("""
        SELECT
            id,
            name,
            size,
            price,
            stock,
            purchase_price
        FROM products
        WHERE id = ?
    """, (
        product_id,
    )).fetchone()


    if product is None:

        conn.close()

        return "Product not found"


    selling_price = product[3]

    stock = product[4]

    purchase_price = product[5] or 0


    # Stock check

    if quantity > stock:

        conn.close()

        return """
        <script>

            alert("Not enough stock available!");

            window.location.href="/";

        </script>
        """


    # ================= CALCULATE =================

    total = selling_price * quantity

    cost = purchase_price * quantity

    profit = total - cost


    # New stock

    new_stock = stock - quantity


    # Update stock

    conn.execute("""
        UPDATE products

        SET stock = ?

        WHERE id = ?
    """, (
        new_stock,
        product_id
    ))


    # Save sale + profit

    conn.execute("""
        INSERT INTO sales
        (customer, product_id, quantity, total, profit)

        VALUES (?, ?, ?, ?, ?)
    """, (
        customer,
        product_id,
        quantity,
        total,
        profit
    ))


    conn.commit()

    conn.close()


    return redirect("/")

# ================= DELETE SALE =================

@app.route("/delete-sale/<int:sale_id>", methods=["POST"])
def delete_sale(sale_id):

    conn = sqlite3.connect("tanayara.db")

    conn.execute("""
        DELETE FROM sales
        WHERE id = ?
    """, (sale_id,))

    conn.commit()

    conn.close()

    return redirect("/")




# ================= START =================

create_database()


if __name__ == "__main__":

    app.run(debug=True)