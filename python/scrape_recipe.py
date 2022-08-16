import os

import click
import requests
from recipe_scrapers import scrape_me, scrape_html

from python.RecipeModel import RecipeModel


@click.command()
@click.argument('url')
def run(url: str):
    print("Scraping {}".format(url))
    model = RecipeModel(url, "sauces")

    try:
        model.scrape()
        path = "_recipes/{}".format(model.category)
        filename = model.get_filename() + ".md"

        if not os.path.exists(path):
            os.makedirs(path)
            print("Created new directory {}".format(path))

        yaml_data = model.get_recipe_yaml()
        full_path = "{}/{}".format(path, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml_data)
            f.write("---")
            print("Wrote new document {}".format(full_path))

        r = requests.get(model.image, stream=True)
        img_path = "assets/img/{}".format(model.category)
        img_full_path = "{}/{}".format(img_path, model.get_image_name())

        if not os.path.exists(img_path):
            os.makedirs(img_path)
            print("Created new directory {}".format(img_path))

        with open(img_full_path, "wb") as f:
            f.write(r.content)
            print("Wrote image data to {}".format(img_full_path))

    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()
