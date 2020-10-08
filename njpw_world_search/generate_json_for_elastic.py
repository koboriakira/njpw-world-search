import json
from njpw_world_search.firestore import get_all_movies
from njpw_world_search.elastic_search import insert_from_json


def generate_json():
    # すべてのドキュメントを取得
    actual = get_all_movies()

    # json形式で保存
    with open('all_movie.json', 'w') as f:
        json.dump(actual, f, indent=2, ensure_ascii=False)

    # ローカルのelasticsearchに登録
    insert_from_json()
