from dataclasses import dataclass
from bs4 import BeautifulSoup
from typing import List, Dict, Any


@dataclass
class Scraper:
    html: str

    def __post_init__(self) -> None:
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_movie_id_list(self) -> List[str]:
        movie_id_list: List[str] = []
        for tag in self.soup.select('.movieArea dl dd a'):
            movie_id = tag.attrs['href'].replace('/p/', '')
            movie_id_list.append(movie_id)
        return movie_id_list

    def get_movie_detail(self) -> Dict[str, Any]:
        soup_section = self.soup.select_one('section.article-item')
        # タイトル
        title = soup_section.select_one('.article-title').text

        # タグ（タグの種類とタグ名がある）
        tags_soup = soup_section.select('.tag-list a')
        tags = list(map(lambda t: _scrape_tag(t), tags_soup))
        return {
            "title": title,
            "tags": tags
        }


def _scrape_tag(tag_el) -> Dict[str, str]:
    tag = {}
    tag['div'] = tag_el.attrs['class'][0]
    tag['id'] = tag_el.attrs['href'].replace('/search/tag/', '')
    tag['name'] = tag_el.text
    return tag
