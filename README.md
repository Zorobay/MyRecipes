# MyRecipes

## Setup
You need to have python installed first.

1. Install Jekyll: https://jekyllrb.com/docs/installation/windows/
2. Install Poetry: https://python-poetry.org/docs/
3. Run `poetry install` from the project root.
4. Run `bundle install` from the project root.

## Running

### Webserver

Run from the root:
```
bundle exec jekyll serve --livereload
```

_You might need to run_ `bundle install` _first, but you should get a warning if that is the case._

## Python scripts

### Generating navigation

To automatically generate the left navigation (recipe index) from the folder structure under `_recipes/` run:
```
poetry run python .\python\generate_navigation.py
```

## Adding recipes

### Adding new category

Create a new folder under `_recipes/`. Then run the python script for generating navigation.

### Adding new recipe

Create a new `.md` file under your chosen category in `_recipes/` and fill out the recipe using the following template:

```yaml
---
title: <title>
description:
  <description>
ingredients:
- title: <optional ingredients subtitle>
  steps:
  - <amount> <ingredient 1>
  - <amount> <ingredient 2>
- title: <optional ingredients subtitle>
  steps:
  - <amount> <ingredient 3>
  - <amount> <ingredient 4>
instructions:
- title: <optional instruction subtitle>
  steps:
  - <step 1>
  - <step 2>
- title: <optional instruction subtitle>
  steps:
  - <step 3>
  - <step 4>
image: <path to cover image>
yield: <description of yield>
category: <name of category>
total_time: <total time>
source: <link to original source>
note: <notes>
---
```

The content can include html elements as well, like links:

```yaml
description:
  Amazing wontons best served with a <a href="./chinese_cucumber_salad">to-die-for cucumber salad</a>! These are also easy and fun to make!
```

Icons are also supported: https://aksakalli.github.io/jekyll-doc-theme/docs/font-awesome/