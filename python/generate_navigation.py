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

def get_image_path(category: str, image_name: str) -> str:
    if image_name:
        return f'{category}/{image_name}'
    return ''


def get_recipe_navigations(root_path: str) -> dict:
    categories = []
    recipe_index = []

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
                        "url": "/recipes/{}/{}".format(subDir, filename),
                        "image": get_image_path(subDir, fm_params.get('image'))
                    })

            categories.append(cat)

    return {"recipes": categories}


if __name__ == '__main__':
    cwd = os.getcwd()
    navs = get_recipe_navigations("{}/_recipes".format(cwd))
    path = "{}/_data/navigation.yml".format(cwd)

    with open(path, "w", encoding="utf-8") as f:
        data = yaml.dump(navs, encoding="utf-8", allow_unicode=True, sort_keys=False).decode("utf-8")
        f.write(data)

        print("Wrote the following data to {}:\n".format(path))
        print(data)
