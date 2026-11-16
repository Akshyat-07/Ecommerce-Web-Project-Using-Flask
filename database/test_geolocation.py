
from geolocation import get_ip_location

# Google's public DNS IP - test address
test_ip = "8.8.8.8"

result = get_ip_location(test_ip)

if result:
    print("Geolocation successful!")
    print("Country:", result["country"])
    print("Country Code:", result["country_code"])
    print("Region:", result["region"])
    print("City:", result["city"])
    print("Latitude:", result["latitude"])
    print("Longitude:", result["longitude"])
else:
    print("Geolocation failed. Check your internet connection or API response.")
