import requests

API_KEY = '23c3692d06d049aea56bcbd896938f4f'
url = ('https://newsapi.org/v2/top-headlines?'
       'language=en&'
       'pageSize=100&'
       f'apiKey={API_KEY}')

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    print("API Connection Successful!")
    print(f"Total Results: {data['totalResults']}")
    print("\nFirst article:")
    print(f"Title: {data['articles'][0]['title']}")
    print(f"Source: {data['articles'][0]['source']['name']}")
else:
    print(f"Error: {data['message']}") 