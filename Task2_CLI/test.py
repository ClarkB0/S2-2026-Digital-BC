import requests, json

data = requests.get('https://world.openfoodfacts.net/api/v2/product/3017624010701').json()

with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)