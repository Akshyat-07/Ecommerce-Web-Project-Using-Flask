from flask import Flask, jsonify, render_template, request
from pathlib import Path
import sqlite3

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "products.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    DB_PATH.parent.mkdir(exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                image_url TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            sample_products = [
                ("Wireless Headphones", "Comfortable over-ear headphones with clear sound and wireless connectivity.", 2499.00, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", "Electronics"),
                ("Smart Watch", "A lightweight smartwatch for everyday activity and notifications.", 3299.00, "https://images.unsplash.com/photo-1523275335684-37898b6baf30", "Electronics"),
                ("Backpack", "A durable everyday backpack with a spacious main compartment.", 1199.00, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62", "Accessories"),
                ("Running Shoes", "Comfortable running shoes designed for daily walks and workouts.", 1899.00, "https://images.unsplash.com/photo-1542291026-7eec264c27ff", "Fashion"),
                ("Coffee Mug", "A reusable ceramic mug for your favourite hot drinks.", 399.00, "https://images.unsplash.com/photo-1514228742587-6b1558f1f1f4", "Home")
            ]
            conn.executemany(
                "INSERT INTO products (name, description, price, image_url, category) VALUES (?, ?, ?, ?, ?)",
                sample_products
            )

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/products")
def list_products():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    if len(search) > 100 or len(category) > 50:
        return jsonify({"error": "Search or category value is too long."}), 400

    sql = "SELECT * FROM products WHERE 1=1"
    params = []
    if search:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY id"

    with get_db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return jsonify([dict(row) for row in rows]), 200

@app.get("/api/products/<int:product_id>")
def product_details(product_id):
    if product_id <= 0:
        return jsonify({"error": "Product ID must be positive."}), 400
    with get_db() as conn:
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Product not found."}), 404
    return jsonify(dict(row)), 200

@app.errorhandler(404)
def not_found(_error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "API endpoint not found."}), 404
    return "Page not found", 404

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
