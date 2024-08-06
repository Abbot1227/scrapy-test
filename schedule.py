import requests

url = 'http://localhost:6800/schedule.json'

data = {'project': 'urls', 'spider': 'general'}

response = requests.post(url, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(response.json())
