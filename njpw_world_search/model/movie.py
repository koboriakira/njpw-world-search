from __future__ import annotations
from dataclasses import dataclass, field
from njpw_world_search.model.tag import Tags
from typing import List, Dict


@dataclass
class Movie:
    id: str
    title: str
    tags: Tags
    like_count: int = field(default=0)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags.to_dict(),
            "like_count": self.like_count
        }


@dataclass
class Movies:
    movies: List[Movie]

    def length(self) -> int:
        return len(self.movies)

    def to_dict(self) -> Dict:
        return {
            "movies": list(map(lambda m: m.to_dict(), self.movies))
        }
