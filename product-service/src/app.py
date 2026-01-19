from flask import Flask, jsonify, request
import psycopg2
import redis
import os
import json
import time

app = Flask(__name__)

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# PostgreSQL configuration
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "ecommerce")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "admin123")


def get_db_connection(retries=5, delay=5):
    """Connect to Postgres with retries"""
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except Exception as e:
            print(f"[DB] Connection failed, retrying ({i+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Could not connect to the database after several retries.")


@app.route("/health")
def health():
    """Health check: DB + Redis"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()

        cache.ping()
        return "OK", 200
    except Exception as e:
        return f"Not Ready: {e}", 503


@app.route("/api/products")
def all_products():
    # Check Redis cache
    cached = cache.get("products")
    if cached:
        return jsonify(json.loads(cached))

    # Fetch from Postgres
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price FROM products")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = [{"id": r[0], "name": r[1], "category": r[2], "price": float(r[3])} for r in rows]

    # Store in Redis for 60 seconds
    cache.set("products", json.dumps(data), ex=60)
    return jsonify(data)


@app.route("/api/products/<int:id>")
def single_product(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price FROM products WHERE id=%s", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Product not found"}), 404

    product = {"id": row[0], "name": row[1], "category": row[2], "price": float(row[3])}
    return jsonify(product)


@app.route("/api/products/category/<category>")
def products_by_category(category):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price FROM products WHERE category=%s", (category,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = [{"id": r[0], "name": r[1], "category": r[2], "price": float(r[3])} for r in rows]
    return jsonify(data)


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.json
    if not data or not all(k in data for k in ("name", "category", "price")):
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, category, price) VALUES (%s,%s,%s) RETURNING id",
        (data["name"], data["category"], data["price"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # Invalidate cache
    cache.delete("products")

    return jsonify({"status": "created", "id": new_id}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

