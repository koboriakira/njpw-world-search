import json
import requests
import re
from datetime import datetime as DateTime
from typing import Dict, Any, List, Optional
from njpw_world_search.model.tag import Tag, Tags
from njpw_world_search.model.movie import Movie, Movies

HEADERS = {
    'Content-Type': 'application/json'}

# ENDPOINT = 'https://elasticsearch-test-4kl4rebkoq-an.a.run.app/'
ENDPOINT = 'http://localhost:9200/'


def insert(movie_id: str, movie: Dict[str, Any]) -> Dict[str, Any]:
    url = f'{ENDPOINT}movies/_doc/{movie_id}?pretty&pretty'
    res = requests.put(url=url, data=json.dumps(movie), headers=HEADERS)
    return res.text


def insert_from_json():
    with open('all_movie.json', 'r') as f:
        data = json.loads(f.read())
        for movie_id, movie in data.items():
            insert(movie_id=movie_id, movie=movie)


def search(options: Dict) -> Optional[Movies]:
    query = _create_query(options=options)
    print(query)

    url = f'{ENDPOINT}movies/_search?pretty'
    res = requests.post(url=url, data=json.dumps(query), headers=HEADERS)
    if res.status_code not in [200, 201]:
        print(res.text)
        return None
    datas = json.loads(res.text)
    movie_list: List[Movie] = list(
        map(lambda data: _generate_movie_model(data), datas['hits']['hits']))
    return Movies(movies=movie_list)


def _create_query(options: Dict):
    text_conds = re.sub(r'\s+', ' ', options['text']).split(' ')
    must_one: str = text_conds[0]
    should_list: Optional[List[str]] = text_conds[1:] if len(
        text_conds) > 1 else None

    # begin creating query
    bool_query = {}

    # must
    must_query = {
        "match": {
            "title": must_one
        }
    }
    bool_query['must'] = must_query

    # should
    if should_list is not None:
        should_query = list(
            map(lambda text: {"match": {"title": text}}, should_list))
        bool_query['should'] = should_query

    return {
        "query": {
            "bool": bool_query
        }
    }


def _generate_movie_model(data: Dict) -> Movie:
    id = data['_id']
    title = data['_source']['title']
    like_count = data['_source']['like_count'] if 'like_count' in data['_source'] else 0
    date: DateTime = data['_source']['date']
    tag_dict_list = data['_source']['tags']
    tag_list: List[Tag] = list(
        map(lambda tag_dict: Tag(**tag_dict), tag_dict_list))
    tags = Tags(tags=tag_list)
    movie = Movie(
        id=id,
        title=title,
        tags=tags,
        like_count=like_count,
        date=date)
    return movie


def get_indices():
    url = f'{ENDPOINT}_cat/indices?v'
    print(url)
    res = requests.get(url)
    print(res)


if __name__ == '__main__':
    get_indices()
    # insert_from_json()
    # options = {
    #     'text': "内藤 8月 神宮"
    # }
    # print(search(options))
