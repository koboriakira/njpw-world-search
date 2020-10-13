from njpw_world_search.value_object.search_condition import SearchCondition
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date as Date
from typing import Dict, List, Optional
from njpw_world_search.controller import scrape_page, search_movies, batch_execute, grant_seq_batch_execute, search_unregisted_movies
from njpw_world_search import controller
from pydantic import BaseModel
import os

ALLOW_ORIGIN = "https://njpw-world-search-front.vercel.app/"
ao_value: Optional[str] = os.getenv('ALLOW_ORIGINS')
allow_origins: List[str] = ao_value.split(',') if ao_value is not None else []
allow_origins.append(ALLOW_ORIGIN)
print(allow_origins)


app = FastAPI()
# CORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    # allow_credentials=True,   # 追記により追加
    allow_methods=["GET"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


class SearchMoviesOptions(BaseModel):
    text: str


@app.get("/")
def hello():
    return {
        "API": "is running"
    }


@app.post("/scrape/{page}")
def scrape(page: int):
    result: List[str] = scrape_page(page=page, stop_if_exists=False)
    return {"count": len(result), "result": result}


@app.post("/scrape/movie/{movie_id}")
def scrape_movie(movie_id: str):
    result: Dict = controller.scrape_movie(movie_id=movie_id)
    return {"status_code": 200, "result": result}


@ app.get("/movies/unregisted/")
def unregisted_movies(begin_page: Optional[int], end_page: Optional[int]):
    return {
        "status_code": 200,
        "result": search_unregisted_movies(
            begin_page=begin_page,
            end_page=end_page)}


@app.get("/movies")
def get_movies(
        text: Optional[str] = None,
        begin_date: Optional[str] = None,
        end_date: Optional[str] = None):
    try:
        cond = SearchCondition(
            text=text,
            begin_date=Date.fromisoformat(begin_date) if begin_date is not None and begin_date != '' else None,
            end_date=Date.fromisoformat(end_date) if end_date is not None and begin_date != '' else None)
        movies = search_movies(cond=cond)
        return {"movies": movies}
    except Exception:
        raise RuntimeError("エラーが発生しました。詳細はサーバのログを確認してください")


@app.put("/to-elastic/")
def to_elastic():
    pass


@app.post("/batch/")
def batch():
    is_success = batch_execute()
    return {"is_success": is_success}


@app.post("/grant-seq-batch/")
def grant_seq_batch():
    is_success = grant_seq_batch_execute()
    return {"is_success": is_success}


@app.post("/only-in-japan")
def only_in_japan():
    result = controller._only_in_japan()
    return {"result": result}
