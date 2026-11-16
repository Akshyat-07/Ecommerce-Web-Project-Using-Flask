<<<<<<< HEAD
# ShopLite — Full-Stack E-Commerce (Part 1)

A minimal product-listing website built to meet the Part 1 requirements of the assignment.

## Technology
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask (REST API)
- Database: SQLite (relational SQL database)

## Requirements
- Python 3.9 or newer
- pip

## Run locally

### 1. Open the project folder
```bash
cd ecommerce_part1
```

### 2. Create and activate a virtual environment

Windows PowerShell:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:
```bat
.venv\Scripts\activate.bat
```

Linux / WSL / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the application
```bash
python app.py
```

The database and sample products are created automatically on the first run.

### 5. Open in your browser
Visit: http://127.0.0.1:5000

## Features
- Product catalogue showing name, description, price and image
- Product details modal
- Search by product name or description
- Filter by category
- Data is retrieved through Flask API endpoints

## API endpoints

| Method | Endpoint | Description | Success |
|---|---|---|---|
| GET | `/api/products` | Retrieve all products | 200 |
| GET | `/api/products?search=watch` | Search products | 200 |
| GET | `/api/products?category=Electronics` | Filter by category | 200 |
| GET | `/api/products/1` | Retrieve one product | 200 |

Error responses:
- `400 Bad Request` — invalid or excessively long search/filter input
- `404 Not Found` — product or API endpoint does not exist

## Database
SQLite database file: `database/products.db`

Table: `products`

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Product name |
| description | TEXT | Product description |
| price | REAL | Product price |
| image_url | TEXT | Product image URL |
| category | TEXT | Product category |

The application inserts sample products automatically when the database is empty. The SQL table definition is also provided in `database/schema.sql`.

## Architecture
1. The browser loads the HTML, CSS and JavaScript frontend from Flask.
2. JavaScript sends HTTP GET requests to the Flask REST API.
3. Flask validates query parameters and executes SQL queries on SQLite.
4. Flask returns product data as JSON.
5. JavaScript displays the returned products and details.

```text
User / Browser
      |
      v
HTML + CSS + JavaScript
      |
      | HTTP GET / JSON
      v
Python Flask REST API
      |
      | SQL query
      v
SQLite Database
```

## Project structure
```text
ecommerce_part1/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── database/
│   └── schema.sql
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Notes
- Product images are loaded from external image URLs, so an internet connection is required for those images.
- The database file is generated locally and is excluded from Git; sample data is inserted automatically.
- Run the app with `python app.py` from the project directory.
=======
# Ecommerce-Web-Project-Using-Flask
Ecommerce Web Project Using Flask, Python, SQLite
>>>>>>> f9596ecd1ffcb8b3857878a5256006ac4eebebfc
