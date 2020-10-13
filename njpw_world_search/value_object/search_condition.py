from typing import Dict, List, Optional
from datetime import date as Date
from datetime import datetime as DateTime
from datetime import time, timedelta, timezone
import re


SPLIT_KEYWORD = re.compile(r'(\s|　|・)')


class SearchCondition:
    def __init__(
        self,
        text: str = None,
        begin_date: Date = None,
        end_date: Date = None,
    ) -> None:
        self.text: str = text if text is not None else ''
        if begin_date is not None:
            self.begin_date: Optional[DateTime] = _convert_to_datetime(
                date=begin_date, mode='begin')
        else:
            self.begin_date = None
        if end_date is not None:
            self.end_date: Optional[DateTime] = _convert_to_datetime(
                date=end_date, mode='end')
        else:
            self.end_date = None
        self.keywords = _generate_keywords(text=text)

    def validate(self) -> None:
        if self.text == '' and self.begin_date is None and self.end_date is None:
            raise SearchConditionException('検索条件が未指定です')
        if self.begin_date is None or self.end_date is None:
            return
        if self.begin_date >= self.end_date:
            raise SearchConditionException('期間の指定が誤っています')

    def has_begin_date(self) -> bool:
        return self.begin_date is not None

    def has_end_date(self) -> bool:
        return self.end_date is not None

    def __str__(self) -> str:
        data: Dict = {
            "text": self.text,
            "begin_date": self.begin_date,
            "end_date": self.end_date
        }
        return str(data)


def _generate_keywords(text: Optional[str]) -> List[str]:
    if text is None:
        return []
    return list(
        filter(
            lambda w: not SPLIT_KEYWORD.fullmatch(w),
            SPLIT_KEYWORD.split(text)))


def _convert_to_datetime(
        date: Optional[Date],
        mode: str) -> Optional[DateTime]:
    if date is None:
        return None
    if mode == 'begin':
        return DateTime.combine(
            date=date, time=time(0, 0, 0), tzinfo=timezone.utc)
    if mode == 'end':
        return DateTime.combine(
            date=date, time=time(23, 59, 59), tzinfo=timezone.utc)


class SearchConditionException(Exception):
    pass
