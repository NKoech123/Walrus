import requests
import json

url = 'https://storage.googleapis.com/dc-recruiting-longform-4d1c78ff/heroes-1460ca6a.json'

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=4))  # Pretty-print the result
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
