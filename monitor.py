import requests

url = 'http://localhost:6800/listjobs.json'

params = {'project': 'urls'}

response = requests.get(url, params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(response.json())
