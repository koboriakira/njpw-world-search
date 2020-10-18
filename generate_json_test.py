import json
from typing import Dict, List
from datetime import datetime as DateTime
from njpw_world_search.firestore import get_year_movies

START_YEAR = 1973
END_YEAR = 1974

DIR_NAME = 'json'


def generate_json():
    # すべてのドキュメントを取得
    # actual = get_all_movies()
    # movies: List[Dict] = []
    # for movie_id, movie in actual.items():
    #     movie['id'] = movie_id
    #     movies.append(movie)

    # データを年ごとに分ける

    for year in range(START_YEAR, END_YEAR + 1):
        data = get_year_movies(year=year)
        print(year)
        movies: List[Dict] = []
        for movie_id, movie in data.items():
            movie['id'] = movie_id
            movies.append(movie)
        movies = sorted(movies, key=lambda m: m['date'])

        # json形式で保存
        filename = f'movies_{year}.json'
        with open(f'{DIR_NAME}/{filename}', 'w') as f:
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
