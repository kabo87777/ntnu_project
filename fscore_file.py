import requests
url = 'https://stock.wespai.com/p/23992'
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
    }
)
response = requests.get(url, headers=headers)

print(response.text)