import os
import re
import yaml

REG_FRONT_MATTER = re.compile(r"---(.+)---", re.DOTALL)


def get_params_from_front_matter(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
        match = REG_FRONT_MATTER.search(data)
        front_matter = match.group(1)
        return yaml.safe_load(front_matter)

def get_filename_without_extension(filename: str) -> str:
    return filename.rsplit(".", maxsplit=1)[0]


def get_recipe_navigations(root_path: str) -> dict:
    categories = []

    for rootDir, subDirs, files in os.walk(root_path, topdown=True):
        for subDir in subDirs:
            cat = {
                "title": subDir.capitalize(),
                "children": []
            }

            subDirPath = os.path.join(rootDir, subDir)
            for subRootDir, subsubDirs, subFiles in os.walk(subDirPath):
                for subFile in subFiles:
                    filepath = os.path.join(subDirPath, subFile)
                    fm_params = get_params_from_front_matter(filepath)
                    filename = get_filename_without_extension(subFile)

                    cat["children"].append({
                        "title": fm_params["title"],
                        "url": "/recipes/{}/{}".format(subDir, filename)
                    })

            categories.append(cat)

    return {"recipes": categories}


if __name__ == '__main__':
    navs = get_recipe_navigations("_recipes")

    with open("_data/navigation.yml", "w", encoding="utf-8") as f:
        yaml.dump(navs, f)
