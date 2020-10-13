from typing import List
import re


SPLIT_KEYWORD = re.compile(r'(\s|　|・)')


class SearchCondition:
    def __init__(self, text: str = None) -> None:
        self.text = text if text is not None else ''
        self.keywords = _generate_keywords(text=text)


def _generate_keywords(text: str) -> List[str]:
    return list(
        filter(
            lambda w: not SPLIT_KEYWORD.fullmatch(w),
            SPLIT_KEYWORD.split(text)))
