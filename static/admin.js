
// ----------------------------------------
// LOAD VISITOR STATISTICS
// ----------------------------------------

async function loadStats() {
    try {
        const response = await fetch("/api/admin/stats");

        if (!response.ok) {
            throw new Error("Failed to fetch statistics");
        }

        const data = await response.json();

        document.getElementById("totalVisitors").textContent =
            data.total_visitors;

        document.getElementById("uniqueVisitors").textContent =
            data.unique_visitors;

        document.getElementById("realVisitors").textContent =
            data.real_visitors;

        document.getElementById("simulatedVisitors").textContent =
            data.simulated_visitors;

    } catch (error) {
        console.error("Statistics error:", error);
    }
}


// ----------------------------------------
// LOAD COUNTRY STATISTICS
// ----------------------------------------

async function loadCountries() {
    try {
        const response = await fetch("/api/admin/countries");

        if (!response.ok) {
            throw new Error("Failed to fetch country data");
        }

        const countries = await response.json();

        const table = document.getElementById("countryTable");

        table.innerHTML = "";

        if (countries.length === 0) {
            table.innerHTML = `
                <tr>
                    <td colspan="3">No country data available</td>
                </tr>
            `;
            return;
        }

        countries.forEach(country => {
            const row = document.createElement("tr");

            const values = [
                country.country,
                country.country_code || "-",
                country.visitors
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Country data error:", error);
    }
}


// ----------------------------------------
// LOAD RECENT VISITORS
// ----------------------------------------

async function loadRecentVisitors() {
    try {
        const response = await fetch("/api/admin/recent?limit=10");

        if (!response.ok) {
            throw new Error("Failed to fetch recent visitors");
        }

        const visitors = await response.json();

        const table = document.getElementById("recentTable");

        table.innerHTML = "";

        if (visitors.length === 0) {
            table.innerHTML = `
                <tr>
                    <td colspan="6">No visitor records found</td>
                </tr>
            `;
            return;
        }

        visitors.forEach(visitor => {
            const row = document.createElement("tr");

            const values = [
                visitor.ip_address,
                visitor.country || "Unknown",
                visitor.city || "Unknown",
                visitor.requested_url,
                visitor.timestamp || "-"
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            // Visitor type label
            const typeCell = document.createElement("td");
            const badge = document.createElement("span");

            if (Number(visitor.is_simulated) === 1) {
                badge.textContent = "Simulated";
                badge.className = "visitor-type simulated";
            } else {
                badge.textContent = "Real";
                badge.className = "visitor-type real";
            }

            typeCell.appendChild(badge);

            // Insert type before timestamp
            row.insertBefore(typeCell, row.lastChild);

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Recent visitors error:", error);
    }
}


// ----------------------------------------
// REFRESH ALL DASHBOARD DATA
// ----------------------------------------

async function refreshDashboard() {
    await Promise.all([
        loadStats(),
        loadCountries(),
        loadRecentVisitors()
    ]);
}


// Initial dashboard loading
refreshDashboard();


// Automatically refresh every 10 seconds
setInterval(refreshDashboard, 10000);
