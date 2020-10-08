from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class Tag:
    div: TagClass
    id: str
    name: str

    def __init__(self, div: str, id: str, name: str) -> None:
        self.div = TagClass.to_enum(div)
        self.id = id
        self.name = name

    def to_dict(self) -> Dict:
        return {
            "div": self.div.value[0],
            "id": self.id,
            "name": self.name
        }


@dataclass
class Tags:
    tags: List[Tag]

    def length(self) -> int:
        return len(self.tags)

    def to_dict(self) -> List:
        return list(map(lambda t: t.to_dict(), self.tags))


class TagClass(Enum):
    MAN = 'tag-man', '選手名'
    YEAR = 'tag-year', '年代'
    BOX = 'tag-box', '会場名'
    MIC = 'tag-mic', '実況解説者'
    CHANP = 'tag-champ', 'タイトルマッチ'
    OTHER = 'tag-other', 'その他'

    @classmethod
    def to_enum(cls, value: str) -> TagClass:
        for tag_class in TagClass:
            if tag_class.value[0] == value:
                return tag_class
        raise ValueError(f'存在しないタグの種類です tag_class:{value}')
