import typing
from collections.abc import Callable

import requests
import yaml
from recipe_scrapers import scrape_html


def get_or_default(func: Callable[[], typing.Any], default: typing.Any) -> typing.Any:
    try:
        return func()
    except BaseException:
        return default


class RecipeModel:
    _REPLACEMENTS = {
        'å': 'aa',
        'ä': 'ae',
        'ö': 'oe'
    }

    def __init__(self, url: str, category: str):
        self.url = url
        self.title = None
        self.description = None
        self.ingredients = []
        self.instructions = []
        self.image = None
        self.yild = None
        self.category = category.lower()
        self.source = url
        self.total_time = None

    def scrape(self):
        html = requests.get(self.url).content
        scraper = scrape_html(html=html, org_url=self.url)

        self.title = get_or_default(lambda: scraper.title(), '')
        self.description = get_or_default(lambda: scraper.description(), '')
        self.ingredients = get_or_default(lambda: scraper.ingredients(), [])
        self.instructions = get_or_default(lambda: scraper.instructions_list(), [])
        self.image = get_or_default(lambda: scraper.image(), '')
        self.yild = get_or_default(lambda: scraper.yields(), '')
        self.total_time = get_or_default(lambda: scraper.total_time(), '')

    def get_filename(self) -> str:
        filename = self.title.lower()

        for key, val in self._REPLACEMENTS.items():
            filename = filename.replace(key, val)

        filename = filename.replace(" ", "_")

        return filename

    def get_image_name(self) -> str:
        img_ext = self.image.split("/")[-1].split(".")[-1]
        return "{}.{}".format(self.get_filename(), img_ext)

    def get_recipe_yaml(self) -> str:
        map = {
            'title': self.title,
            'description': self.description,
            'ingredients': self._to_step_format(self.ingredients),
            'instructions': self._to_step_format(self.instructions),
            'image': self.get_image_name(),
            'yield': self.yild,
            'category': self.category,
            'total_time': self.total_time,
            'source': self.source,
        }

        return yaml.dump(map, encoding="utf-8", allow_unicode=True, sort_keys=False).decode("utf-8")

    def _to_step_format(self, lst: list) -> list:
        return [{
            "title": None,
            "steps": lst
        }]
