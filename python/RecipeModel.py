import requests
import yaml
from recipe_scrapers import AbstractScraper, scrape_html


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

        self.title = scraper.title()
        self.description = scraper.description()
        self.ingredients = scraper.ingredients()
        self.instructions = scraper.instructions().split("\n")
        self.image = scraper.image()
        self.yild = scraper.yields()
        self.total_time = scraper.total_time()

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

