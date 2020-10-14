from typing import Any, Dict, Iterator, List
import time
import os
import json
from datetime import datetime as DateTime
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD, DATETIME
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, OperatorsPlugin
from njpw_world_search.mecab import generate_keywords

JSON_FILE_NAME = 'movies.json'

WHOOSH_INDEX_NAME = 'whoosh_index'
if not os.path.exists(WHOOSH_INDEX_NAME):
    os.mkdir(WHOOSH_INDEX_NAME)


# OperatorsPluginはAnd,orなどに好きな記号を割り当てることが出来る
operators_plugin = OperatorsPlugin(And="&", Or="\\|", Not="~")


def prepare() -> None:
    try:
        # Schemaの定義
        writer = _prepare_writer()
        with open(JSON_FILE_NAME, 'r') as f:
            data = json.loads(f.read())
            documents = list(_to_documents(movies=data['movies']))
            count = len(documents)
            print(f'{count}件のデータを挿入')
            for document in documents:
                writer.add_document(**document)
                count = count - 1
                if count % 100 == 0:
                    print(f'残り{count}件')
        writer.commit()
    except BaseException as e:
        print(e)
        import traceback
        traceback.print_exc()


def search_whoosh(keywords: List[str] = []):
    start = time.time()
    result_list = []
    error = False
    ix = open_dir(WHOOSH_INDEX_NAME)  # 作成したインデックスファイルのディレクトリを指定
    try:
        with ix.searcher() as searcher:
            if len(keywords) == 0:
                results = searcher.documents()
                result_list = [result for result in results]
            else:
                # QueryParserに"content"内を検索することを指定
                words = "&".join(keywords)
                parser = QueryParser("content", ix.schema)
                parser.replace_plugin(operators_plugin)  # opをセット
                query = parser.parse(words)  # parserに検索語を入れる
                results = searcher.search(query, limit=None)  # 検索語で全文検索
                for result in results:
                    data = {}
                    data['title'] = result['title']
                    data['path'] = result['path']
                    if 'datetime' in result:
                        data['datetime'] = result['datetime']
                    result_list.append(data)
    except Exception as e:
        error = str(e)
        print(f'Got an error: {error}')
        pass
    finally:
        measurement_time = str((time.time() - start) * 10000 // 10) + "ms"
        return {"time": measurement_time,
                "result": result_list,
                "error": error}


def _prepare_writer():
    schema = Schema(
        title=TEXT(stored=True),
        path=ID(stored=True),
        content=KEYWORD,
        datetime=DATETIME(stored=True))
    ix = create_in(WHOOSH_INDEX_NAME, schema)
    return ix.writer()


def _to_documents(movies: List[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    for movie in movies:
        result = {}
        result['title'] = movie['title']
        result['path'] = movie['id']
        result['content'] = generate_keywords(title=movie['title'])
        if movie['date'] is not None:
            result['datetime'] = DateTime.fromisoformat(str(movie['date']))
        yield result
