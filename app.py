
import ipaddress

from flask import Flask, jsonify, request, render_template

from database.db import get_db_connection, init_db
from database.geolocation import get_ip_location


app = Flask(__name__)

# Initialize the database
init_db()


# ----------------------------------------
# HOME PAGE
# ----------------------------------------

@app.route("/")
def home():
    return "E-Commerce Website Backend"


# ----------------------------------------
# TEST API
# ----------------------------------------

@app.route("/api/test", methods=["GET"])
def test_api():
    return jsonify({
        "message": "API is working successfully",
        "status": "success"
    })


# ----------------------------------------
# REAL VISITOR TRACKING
# ----------------------------------------

@app.after_request
def log_visitor(response):

    # Ignore static files and API requests
    if request.path.startswith((
        "/static/",
        "/api/simulate",
        "/api/admin"
    )):
        return response

    ip_address = request.remote_addr or "unknown"

    # Avoid geolocation for invalid/private IP addresses
    try:
        ip = ipaddress.ip_address(ip_address)
    except ValueError:
        return response

    if not ip.is_global:
        return response

    # Check whether location is already stored for this IP
    with get_db_connection() as conn:
        existing = conn.execute(
            """
            SELECT country, country_code, region, city,
                   latitude, longitude
            FROM visitors
            WHERE ip_address = ?
            AND is_simulated = 0
            AND country IS NOT NULL
            LIMIT 1
            """,
            (str(ip),)
        ).fetchone()

        if existing:
            location = dict(existing)
        else:
            location = get_ip_location(str(ip)) or {}

        conn.execute(
            """
            INSERT INTO visitors (
                ip_address,
                country,
                country_code,
                region,
                city,
                latitude,
                longitude,
                requested_url,
                is_simulated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (
                str(ip),
                location.get("country"),
                location.get("country_code"),
                location.get("region"),
                location.get("city"),
                location.get("latitude"),
                location.get("longitude"),
                request.path
            )
        )

    return response


@app.route("/api/simulate", methods=["POST"])
def simulate_visitor():

    # Allow simulator requests only from localhost
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return jsonify({"error": "Local access only"}), 403

    data = request.get_json(silent=True) or {}

    ip_address = data.get("ip")
    requested_url = data.get("path", "/")

    # Validate IP address
    try:
        ip = ipaddress.ip_address(ip_address)

        if not ip.is_global:
            return jsonify({
                "error": "A public IP address is required"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "error": "Invalid IP address"
        }), 400

    # Validate requested page
    if (
        not isinstance(requested_url, str)
        or not requested_url.startswith("/")
        or requested_url.startswith("//")
    ):
        return jsonify({
            "error": "Invalid page path"
        }), 400

    # Get approximate visitor location
    location = get_ip_location(str(ip)) or {}

    # Save simulated visitor
    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO visitors (
                ip_address,
                country,
                country_code,
                region,
                city,
                latitude,
                longitude,
                requested_url,
                is_simulated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (
                str(ip),
                location.get("country"),
                location.get("country_code"),
                location.get("region"),
                location.get("city"),
                location.get("latitude"),
                location.get("longitude"),
                requested_url
            )
        )

    return jsonify({
        "status": "success",
        "message": "Simulated visitor recorded",
        "ip": str(ip),
        "location": location
    }), 201


# ----------------------------------------
# ADMIN API 1: VISITOR STATISTICS
# ----------------------------------------

@app.route("/api/admin/stats", methods=["GET"])
def admin_stats():

    with get_db_connection() as conn:
        stats = conn.execute("""
            SELECT
                COUNT(*) AS total_visitors,
                COUNT(DISTINCT ip_address) AS unique_visitors,
                COALESCE(SUM(
                    CASE WHEN is_simulated = 0 THEN 1 ELSE 0 END
                ), 0) AS real_visitors,
                COALESCE(SUM(
                    CASE WHEN is_simulated = 1 THEN 1 ELSE 0 END
                ), 0) AS simulated_visitors
            FROM visitors
        """).fetchone()

    return jsonify(dict(stats))


# ----------------------------------------
# ADMIN API 2: COUNTRY STATISTICS
# ----------------------------------------

@app.route("/api/admin/countries", methods=["GET"])
def admin_countries():

    with get_db_connection() as conn:
        countries = conn.execute("""
            SELECT
                COALESCE(country, 'Unknown') AS country,
                COALESCE(country_code, '') AS country_code,
                COUNT(*) AS visitors
            FROM visitors
            GROUP BY country, country_code
            ORDER BY visitors DESC
        """).fetchall()

    return jsonify([dict(row) for row in countries])


# ----------------------------------------
# ADMIN API 3: RECENT VISITORS
# ----------------------------------------

@app.route("/api/admin/recent", methods=["GET"])
def admin_recent():

    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "Limit must be a number"}), 400

    # Limit the number of returned records
    limit = max(1, min(limit, 100))

    with get_db_connection() as conn:
        visitors = conn.execute("""
            SELECT
                ip_address,
                country,
                country_code,
                region,
                city,
                requested_url,
                timestamp,
                latitude,
                longitude,
                is_simulated
            FROM visitors
            ORDER BY timestamp DESC, id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return jsonify([dict(row) for row in visitors])

@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
