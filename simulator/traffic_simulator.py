
import requests
import time
import random

# Flask backend API
API_URL = "http://127.0.0.1:5000/api/simulate"

# Public IP addresses used as simulation examples
TEST_IPS = [
    "8.8.8.8",
    "1.1.1.1",
    "208.67.222.222",
    "9.9.9.9",
    "4.2.2.2"
]

# Example website pages
PAGES = [
    "/",
    "/products",
    "/products/1",
    "/cart",
    "/checkout"
]


def simulate_traffic():

    print("Starting traffic simulation...\n")

    for i in range(10):

        # Select a sample IP
        ip = random.choice(TEST_IPS)

        # Select a website page
        page = random.choice(PAGES)

        # Prepare simulated visitor data
        visitor_data = {
            "ip": ip,
            "path": page
        }

        try:

            response = requests.post(
                API_URL,
                json=visitor_data,
                timeout=15
            )

            print(
                f"Visitor {i + 1}: "
                f"IP={ip}, "
                f"Page={page}, "
                f"Status={response.status_code}"
            )

            print("Response:", response.json())

        except requests.RequestException as error:

            print("Request failed:", error)

        # Wait before generating next visitor
        time.sleep(2)

    print("\nTraffic simulation completed!")


if __name__ == "__main__":
    simulate_traffic()
