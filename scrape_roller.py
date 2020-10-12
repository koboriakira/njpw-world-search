from typing import List
import requests
import json

complete_pages = 363

endpoint = 'http://localhost:8000/movies/unregisted/'
endpoint_movie = 'http://localhost:8000/scrape/movie/'
false_count = 0

for page in list(map(lambda i: i + complete_pages + 1,
                     range(538 - complete_pages))):
    url = f'{endpoint}?begin_page={page}&end_page={page}'
    res = requests.get(url)
    if res.status_code != 200:
        print(res.status_code)
        print(res.text)
        false_count = false_count + 1
        if false_count >= 3:
            break
    else:
        print(page, end=' ')
        movie_id_list: List[str] = json.loads(res.content)['result']
        print(movie_id_list)
        for movie_id in movie_id_list:
            url = f'{endpoint_movie}{movie_id}'
            res = requests.post(url)
            print(movie_id, json.loads(res.content)['result']['title'])
