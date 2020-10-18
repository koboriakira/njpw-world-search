import json
from typing import Dict, List
from datetime import datetime as DateTime
from njpw_world_search.firestore import get_not_has_date_movies, get_year_movies

START_YEAR = 2020
END_YEAR = 2020

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
        movies: List[Dict] = []
        for movie_id, movie in data.items():
            movie['id'] = movie_id
            movies.append(movie)
        movies = sorted(movies, key=lambda m: m['date'])

        filepath = f'{DIR_NAME}/movies_{year}.json'

        # データ数が以前と変わらないならスキップ
        try:
            with open(filepath, 'r') as f:
                data = json.loads(f.read())
                if len(data['movies']) == len(movies):
                    print(f'{year} : skip')
                    continue
        except FileNotFoundError:
            pass

        with open(filepath, 'w') as f:
            json.dump(
                {"movies": movies},
                f,
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
                default=support_datetime_default)
            print(f'{year} : write')

    # 最後に日付のない動画をまとめて
    data = get_not_has_date_movies()
    movies: List[Dict] = []
    for movie_id, movie in data.items():
        movie['id'] = movie_id
        movies.append(movie)
    movies = sorted(movies, key=lambda m: m['title'])

    filepath = f'{DIR_NAME}/movies_others.json'

    # データ数が以前と変わらないならスキップ
    try:
        with open(filepath, 'r') as f:
            data = json.loads(f.read())
            if len(data['movies']) == len(movies):
                print('other : skip')
                return
    except FileNotFoundError:
        pass

    with open(filepath, 'w') as f:
        json.dump(
            {"movies": movies},
            f,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
            default=support_datetime_default)
        print('other : write')


def support_datetime_default(o):
    if isinstance(o, DateTime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


if __name__ == '__main__':
    generate_json()
