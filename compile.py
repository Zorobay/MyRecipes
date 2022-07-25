import os
import shutil

import dominate.document
import markdown
from dominate import tags

BASE_MARKDOWN_SRC_DIR = "recipes/"
BASE_HTML_OUT_DIR = "out/html/"


def clean_out():
    for root, dirs, files in os.walk(BASE_HTML_OUT_DIR):
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))


def generate_toc() -> str:
    ol = tags.ol(_class="toc")
    for root, dirs, files in os.walk(BASE_MARKDOWN_SRC_DIR):
        for dir in dirs:
            ol.add(tags.li(dir))

    return str(ol)

def generate_index() -> str:
    doc = dominate.document(title="My Recipes")
    doc += generate_toc()
    return str(doc)


if __name__ == "__main__":

    # Remove all old generated files
    clean_out()

    index = generate_index()

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index)

    for root, dirs, files in os.walk(BASE_MARKDOWN_SRC_DIR):
        for file in files:
            path = os.path.join(root, file)
            print("Compiling: {}".format(path))

            with open(path, "r", encoding="utf-8") as f:
                md_text = f.read()
                html = markdown.markdown(md_text)
                a = 2
