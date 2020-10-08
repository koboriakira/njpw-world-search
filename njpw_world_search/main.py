from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from njpw_world_search.controller import sample, scrape_page, search_movies
from pydantic import BaseModel

app = FastAPI()
# CORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
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


@app.post("/sample/")
def test_sample():
    sample()
    return {
        "sample": "is executed."
    }


@app.post("/movies/")
def get_movies(data: SearchMoviesOptions):
    options = {"text": data.text}
    return search_movies(options=options)


@app.put("/to-elastic/")
def to_elastic():
    pass
