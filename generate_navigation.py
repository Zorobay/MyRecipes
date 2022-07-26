import os



def _do_build_navtree(root_path: str, navs: list):
    for entry in os.scandir(root_path):
        if entry.is_dir():
            category = dict()
            category["title"] = entry.name


def build_navtree(root_path: str) -> list:
    navs = list()
    _do_build_navtree(root_path, navs)



if __name__ == '__main__':
    tree = build_navtree("_recipes/")




