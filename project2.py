import os
import io
import sys
import psycopg2
import psycopg2.extras
from flask import Flask, request, redirect, url_for, render_template_string, flash
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change_this_secret_for_production")

DATABASE_URL = os.getenv("DATABASE_URL", None)

if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "mod16db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")
    DATABASE_URL = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_conn():
    parsed = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        dbname=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port
    )
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
        stock INTEGER NOT NULL DEFAULT 0,
        category_id INTEGER REFERENCES categories(id)
    );
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        ordered_at TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """)
    cur.execute("SELECT count(*) FROM categories;")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO categories (name) VALUES ('Dairy'), ('Beverages'), ('Snacks');")
    cur.execute("SELECT count(*) FROM products;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO products (name, description, price, stock, category_id) VALUES
            ('Whole Milk 1L', 'Pure cow milk', 1.20, 50, (SELECT id FROM categories WHERE name='Dairy' LIMIT 1)),
            ('Lassi Classic', 'Sweet lassi 300ml', 0.80, 100, (SELECT id FROM categories WHERE name='Beverages' LIMIT 1)),
            ('Masala Mix', 'Premium masala 200g', 2.50, 30, (SELECT id FROM categories WHERE name='Snacks' LIMIT 1));
        """)
    conn.commit()
    cur.close()
    conn.close()

try:
    init_db()
except Exception as e:
    print("WARNING: Could not initialize DB schema. Check DATABASE_URL and DB accessibility.")
    print(e, file=sys.stderr)

base_html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Module16 - Postgres + Flask</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
  <div class="container-fluid">
    <a class="navbar-brand" href="{{ url_for('index') }}">Module16 App</a>
    <div class="navbar-nav">
      <a class="nav-link" href="{{ url_for('index') }}">Products</a>
      <a class="nav-link" href="{{ url_for('categories') }}">Categories</a>
      <a class="nav-link" href="{{ url_for('orders') }}">Orders</a>
      <a class="nav-link" href="{{ url_for('code') }}">View Code & Timestamp</a>
      <a class="nav-link" href="{{ url_for('instructions') }}">Screenshot Instructions</a>
    </div>
  </div>
</nav>
<div class="container">
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <div class="alert alert-info">
        {% for msg in messages %}
          <div>{{ msg }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}
  {{ content }}
</div>
</body>
</html>
"""

def query_all(sql, params=None):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql, params or ())
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def query_one(sql, params=None):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql, params or ())
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

@app.route("/")
def index():
    products = query_all("""
      SELECT p.id, p.name, p.description, p.price, p.stock, c.name AS category
      FROM products p LEFT JOIN categories c ON p.category_id = c.id
      ORDER BY p.id;
    """)
    content = render_template_string("""
    <h2>Products (CRUD)</h2>
    <p><a class="btn btn-success" href="{{ url_for('add_product') }}">Add Product</a></p>
    <table class="table table-striped">
      <thead><tr><th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Actions</th></tr></thead>
      <tbody>
      {% for p in products %}
        <tr>
          <td>{{ p.id }}</td>
          <td>{{ p.name }}</td>
          <td>{{ p.category or '—' }}</td>
          <td>{{ p.price }}</td>
          <td>{{ p.stock }}</td>
          <td>
            <a class="btn btn-sm btn-primary" href="{{ url_for('edit_product', pid=p.id) }}">Edit</a>
            <a class="btn btn-sm btn-danger" href="{{ url_for('delete_product', pid=p.id) }}" onclick="return confirm('Delete product?');">Delete</a>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    """, products=products)
    return render_template_string(base_html, content=content)

@app.route("/product/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form['name']
        desc = request.form.get('description', '')
        price = request.form['price'] or 0
        stock = request.form['stock'] or 0
        category_id = request.form.get('category_id') or None
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
          INSERT INTO products (name, description, price, stock, category_id)
          VALUES (%s,%s,%s,%s,%s) RETURNING id;
        """, (name, desc, price, stock, category_id))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        flash(f"Product added (id={new_id})")
        return redirect(url_for('index'))
    categories = query_all("SELECT id, name FROM categories ORDER BY name;")
    content = render_template_string("""
    <h2>Add Product</h2>
    <form method="post">
      <div class="mb-3"><label class="form-label">Name</label><input name="name" class="form-control" required></div>
      <div class="mb-3"><label class="form-label">Description</label><input name="description" class="form-control"></div>
      <div class="mb-3"><label class="form-label">Price</label><input type="number" step="0.01" name="price" class="form-control" required></div>
      <div class="mb-3"><label class="form-label">Stock</label><input type="number" name="stock" class="form-control" required></div>
      <div class="mb-3"><label class="form-label">Category</label>
        <select name="category_id" class="form-select">
          <option value="">-- none --</option>
          {% for c in categories %}<option value="{{ c.id }}">{{ c.name }}</option>{% endfor %}
        </select>
      </div>
      <button class="btn btn-primary">Save</button>
    </form>
    """, categories=categories)
    return render_template_string(base_html, content=content)

@app.route("/product/<int:pid>/edit", methods=["GET", "POST"])
def edit_product(pid):
    if request.method == "POST":
        name = request.form['name']
        desc = request.form.get('description', '')
        price = request.form['price'] or 0
        stock = request.form['stock'] or 0
        category_id = request.form.get('category_id') or None
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
          UPDATE products SET name=%s, description=%s, price=%s, stock=%s, category_id=%s WHERE id=%s;
        """, (name, desc, price, stock, category_id, pid))
        conn.commit()
        cur.close()
        conn.close()
        flash("Product updated")
        return redirect(url_for('index'))
    p = query_one("SELECT * FROM products WHERE id=%s;", (pid,))
    if not p:
        flash("Product not found")
        return redirect(url_for('index'))
    categories = query_all("SELECT id, name FROM categories ORDER BY name;")
    content = render_template_string("""
    <h2>Edit Product</h2>
    <form method="post">
      <div class="mb-3"><label class="form-label">Name</label><input name="name" class="form-control" value="{{ p.name }}" required></div>
      <div class="mb-3"><label class="form-label">Description</label><input name="description" class="form-control" value="{{ p.description }}"></div>
      <div class="mb-3"><label class="form-label">Price</label><input type="number" step="0.01" name="price" class="form-control" value="{{ p.price }}" required></div>
      <div class="mb-3"><label class="form-label">Stock</label><input type="number" name="stock" class="form-control" value="{{ p.stock }}" required></div>
      <div class="mb-3"><label class="form-label">Category</label>
        <select name="category_id" class="form-select">
          <option value="">-- none --</option>
          {% for c in categories %}
            <option value="{{ c.id }}" {% if p.category_id==c.id %}selected{% endif %}>{{ c.name }}</option>
          {% endfor %}
        </select>
      </div>
      <button class="btn btn-primary">Save</button>
    </form>
    """, p=p, categories=categories)
    return render_template_string(base_html, content=content)

@app.route("/product/<int:pid>/delete")
def delete_product(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s;", (pid,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Product deleted (if existed)")
    return redirect(url_for('index'))

@app.route("/categories")
def categories():
    cats = query_all("SELECT id,name FROM categories ORDER BY id;")
    content = render_template_string("""
      <h2>Categories</h2>
      <form class="row g-2" method="post" action="{{ url_for('add_category') }}">
        <div class="col-auto"><input name="name" class="form-control" placeholder="New category" required></div>
        <div class="col-auto"><button class="btn btn-success">Add</button></div>
      </form>
      <hr/>
      <ul class="list-group mt-3">
        {% for c in cats %}
          <li class="list-group-item d-flex justify-content-between align-items-center">
            {{ c.id }} — {{ c.name }}
            <a class="btn btn-sm btn-danger" href="{{ url_for('delete_category', cid=c.id) }}" onclick="return confirm('Delete category?');">Delete</a>
          </li>
        {% endfor %}
      </ul>
    """, cats=cats)
    return render_template_string(base_html, content=content)

@app.route("/category/add", methods=["POST"])
def add_category():
    name = request.form['name']
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id;", (name,))
        new_id = cur.fetchone()[0]
        conn.commit()
        flash(f"Category added (id={new_id})")
    except Exception as ex:
        conn.rollback()
        flash(f"Could not add category: {ex}")
    finally:
        cur.close(); conn.close()
    return redirect(url_for('categories'))

@app.route("/category/<int:cid>/delete")
def delete_category(cid):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM categories WHERE id=%s;", (cid,))
        conn.commit()
        flash("Category deleted (if existed)")
    except Exception as ex:
        conn.rollback()
        flash(f"Could not delete category: {ex}")
    finally:
        cur.close(); conn.close()
    return redirect(url_for('categories'))

@app.route("/orders")
def orders():
    orders = query_all("""
      SELECT o.id, o.quantity, o.ordered_at, p.name AS product_name, p.price
      FROM orders o JOIN products p ON o.product_id = p.id
      ORDER BY o.ordered_at DESC;
    """)
    products = query_all("SELECT id, name, stock FROM products ORDER BY name;")
    content = render_template_string("""
      <h2>Orders (join and transaction example)</h2>
      <form method="post" action="{{ url_for('place_order') }}" class="row g-2">
        <div class="col-auto">
          <select name="product_id" class="form-select" required>
            <option value="">-- select product --</option>
            {% for p in products %}<option value="{{ p.id }}">{{ p.name }} (stock: {{ p.stock }})</option>{% endfor %}
          </select>
        </div>
        <div class="col-auto"><input name="quantity" type="number" class="form-control" min="1" placeholder="quantity" required></div>
        <div class="col-auto"><button class="btn btn-primary">Place Order (transaction)</button></div>
      </form>
      <hr/>
      <table class="table">
        <thead><tr><th>ID</th><th>Product</th><th>Qty</th><th>Price per</th><th>Ordered at</th></tr></thead>
        <tbody>
          {% for o in orders %}
            <tr><td>{{ o.id }}</td><td>{{ o.product_name }}</td><td>{{ o.quantity }}</td><td>{{ o.price }}</td><td>{{ o.ordered_at }}</td></tr>
          {% endfor %}
        </tbody>
      </table>
      <p><small>This page demonstrates a SELECT JOIN and a transaction safely reducing product stock when an order is placed.</small></p>
    """, orders=orders, products=products)
    return render_template_string(base_html, content=content)

@app.route("/orders/place", methods=["POST"])
def place_order():
    product_id = int(request.form['product_id'])
    qty = int(request.form['quantity'])
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT stock FROM products WHERE id=%s FOR UPDATE;", (product_id,))
        row = cur.fetchone()
        if not row:
            raise Exception("Product not found")
        stock = row[0]
        if stock < qty:
            raise Exception(f"Not enough stock (available {stock})")
        cur.execute("INSERT INTO orders (product_id, quantity) VALUES (%s,%s) RETURNING id;", (product_id, qty))
        new_order_id = cur.fetchone()[0]
        cur.execute("UPDATE products SET stock = stock - %s WHERE id=%s;", (qty, product_id))
        conn.commit()
        flash(f"Order placed (id={new_order_id}) and stock updated")
    except Exception as ex:
        conn.rollback()
        flash(f"Order failed: {ex}")
    finally:
        cur.close(); conn.close()
    return redirect(url_for('orders'))

@app.route("/search")
def search():
    q = request.args.get('q', '')
    rows = []
    if q:
        rows = query_all("""
          SELECT id, name, description FROM products
          WHERE name ILIKE %s OR description ILIKE %s
          ORDER BY id;
        """, (f"%{q}%", f"%{q}%"))
    content = render_template_string("""
      <h2>Search Products (parameterized)</h2>
      <form><div class="input-group mb-3"><input value="{{ q }}" name="q" class="form-control" placeholder="Search..."><button class="btn btn-outline-secondary">Search</button></div></form>
      <ul class="list-group">
        {% for r in rows %}
          <li class="list-group-item">{{ r.id }} — <strong>{{ r.name }}</strong><div><small>{{ r.description }}</small></div></li>
        {% endfor %}
      </ul>
    """, rows=rows, q=q)
    return render_template_string(base_html, content=content)

@app.route("/code")
def code():
    src = ""
    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        src = f"Error reading source: {e}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")
    content = render_template_string("""
      <h2>Application Source Code (for screenshot)</h2>
      <p><strong>System timestamp:</strong> {{ timestamp }}</p>
      <p><small>Take a full, unedited screenshot showing both the code below and the system timestamp to meet the assignment requirements.</small></p>
      <pre style="max-height:70vh; overflow:auto; background:#f8f9fa; padding:10px; border-radius:6px;">{{ src }}</pre>
    """, src=src, timestamp=timestamp)
    return render_template_string(base_html, content=content)

@app.route("/instructions")
def instructions():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")
    content = render_template_string("""
    <h2>Screenshot & Submission Instructions</h2>
    <ol>
      <li>Run the app and your terminal/IDE in full-screen. Make sure the system timestamp is visible in your OS taskbar or terminal prompt.</li>
      <li>Open the code page: <a href="{{ url_for('code') }}" target="_blank">{{ url_for('code', _external=True) }}</a>. It displays the entire app source and a timestamp above. Take a full (uncropped) screenshot showing the entire browser window including the timestamp visible on your system clock.</li>
      <li>For each practical (create table, insert, select, update, delete, join, transaction), open the route that demonstrates it and take full screenshots:
        <ul>
          <li>Products list: <a href="{{ url_for('index') }}" target="_blank">{{ url_for('index', _external=True) }}</a></li>
          <li>Add product form: <a href="{{ url_for('add_product') }}" target="_blank">{{ url_for('add_product', _external=True) }}</a></li>
          <li>Orders and transaction: <a href="{{ url_for('orders') }}" target="_blank">{{ url_for('orders', _external=True) }}</a></li>
          <li>Search example: <a href="{{ url_for('search') }}" target="_blank">{{ url_for('search', _external=True) }}?q=milk</a></li>
        </ul>
      </li>
      <li>Also take a screenshot of your terminal where you started Flask (it shows the command and server start time). Make sure the timestamp is visible in the terminal prompt or system clock.</li>
      <li>Put all screenshots (full, unedited) in a folder, name them in the order of the lecture/practical (e.g. 01_create_table.png, 02_insert.png ...). Then either:
        <ul>
          <li>Zip the folder, or</li>
          <li>Create a PDF in the correct order (one screenshot per page) — do not crop.</li>
        </ul>
      </li>
      <li>Upload the zip or PDF to Google Drive and enable sharing. Submit the shareable link.</li>
    </ol>
    <p><small>Server timestamp: {{ now }}</small></p>
    """, now=now)
    return render_template_string(base_html, content=content)

@app.route("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("Starting Flask app on port", port)
    app.run(host="0.0.0.0", port=port, debug=True)