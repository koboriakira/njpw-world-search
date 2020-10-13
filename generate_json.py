import json
from typing import Dict, List
from njpw_world_search.firestore import get_all_movies
from datetime import datetime as DateTime


def generate_json():
    # すべてのドキュメントを取得
    actual = get_all_movies()
    movies: List[Dict] = []
    for movie_id, movie in actual.items():
        movie['id'] = movie_id
        movies.append(movie)

    # json形式で保存
    with open('movies.json', 'w') as f:
        json.dump(
            {"movies": movies},
            f,
            indent=2,
            ensure_ascii=False,
            default=support_datetime_default)


def support_datetime_default(o):
    if isinstance(o, DateTime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


if __name__ == '__main__':
    generate_json()
