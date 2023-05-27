# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "django-backend-starter"
copyright = "2023, kimsoungryoul@gmail.com"
author = "kimsoungryoul@gmail.com"
release = "v1.0.0"
# html_short_title = "[docs] django backend starter"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []

language = "ko"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_material"
html_static_path = ["_static"]
# Set link name generated in the top bar.
html_title = "Django Backend Starter"

# Material theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "Django Backend Starter",
    # Set you GA account ID to enable tracking
    "google_analytics_account": "UA-XXXXX",
    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    "base_url": "https://kimsoungryoul.github.io/django-backend-starter/",
    # Set the color and the accent color
    "color_primary": "green",
    "color_accent": "light-green",
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/KimSoungRyoul/django-backend-starter/",
    "repo_name": "django-backend-starter",
    # Visible levels of the global TOC; -1 means unlimited
    "globaltoc_depth": 3,
    # If False, expand all TOC entries
    "globaltoc_collapse": False,
    # If True, show hidden TOC entries
    "globaltoc_includehidden": False,
}
