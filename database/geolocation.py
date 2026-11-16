
import ipaddress
import requests


def get_ip_location(ip_address):
   
    try:
        ip = ipaddress.ip_address(ip_address)

        # Local/private IPs cannot be geolocated accurately
        if not ip.is_global:
            return None

        url = f"https://ipwho.is/{ip_address}"

        response = requests.get(url, timeout=8)
        response.raise_for_status()

        data = response.json()

        if not data.get("success"):
            return None

        return {
            "country": data.get("country"),
            "country_code": data.get("country_code"),
            "region": data.get("region"),
            "city": data.get("city"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }

    except (ValueError, requests.RequestException):
        return None
