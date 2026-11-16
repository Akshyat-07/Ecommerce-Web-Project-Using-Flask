
-- Product information
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    image_url TEXT,
    category TEXT
);

-- Website visitor information
CREATE TABLE IF NOT EXISTS visitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    country TEXT,
    country_code TEXT,
    city TEXT,
    requested_url TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_simulated INTEGER DEFAULT 0
);

-- Indexes for faster dashboard queries
CREATE INDEX IF NOT EXISTS idx_visitors_ip
ON visitors(ip_address);

CREATE INDEX IF NOT EXISTS idx_visitors_country
ON visitors(country);

CREATE INDEX IF NOT EXISTS idx_visitors_timestamp
ON visitors(timestamp);
