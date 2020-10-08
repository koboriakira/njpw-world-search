import requests

complete_pages = 74

endpoint = 'http://localhost:8000/scrape/'
false_count = 0

for i in list(map(lambda i: i + complete_pages, range(534 - complete_pages))):
    print(f'{endpoint}{i}')
    res = requests.post(f'{endpoint}{i}')
    if res.status_code != 200:
        print(res.status_code)
        print(res.text)
        false_count = false_count + 1
        if false_count >= 3:
            break
