import requests

sites = {
    "Site A": "http://localhost:5001/count",
    "Site B": "http://localhost:5002/count",
    "Site C": "http://localhost:5003/count"
}

print("=" * 50)
print("DISTRIBUTED DATABASE MONITOR")
print("=" * 50)

total_records = 0

for site_name, url in sites.items():

    try:
        response = requests.get(url, timeout=3)

        if response.status_code == 200:

            data = response.json()

            print(
                f"{site_name}: ONLINE | Records = {data['records']}"
            )

            total_records += data["records"]

        else:
            print(f"{site_name}: ERROR")

    except requests.exceptions.RequestException:

        print(f"{site_name}: OFFLINE")

print("-" * 50)
print(f"Total Accessible Records: {total_records}")