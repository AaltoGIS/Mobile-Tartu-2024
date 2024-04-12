# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "OTESAMA '23"
copyright = '2023 OTESAMA Organizers & Presenters'
author = 'Henrikki Tenkanen, Rafael Pereira, Christoph Fink'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx_togglebutton',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    'myst_nb',
    "sphinx_design",
    "sphinxnotes.strike",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_book_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ["custom.css"]
#html_logo = '_static/GIScience_logo.png'
html_title = "OTESAMA <br> Workshop '23"

# Download Notebook as .ipynb, not as text file
# See https://github.com/executablebooks/sphinx-book-theme/issues/639
html_sourcelink_suffix = ""
html_source_suffix = ""

# Custom header
#templates_path = ["_templates"]

#source_suffix = {
#    ".rst": "restructuredtext",
#    ".ipynb": "myst-nb",
#    ".myst": "myst-nb",
#}

html_theme_options = {
    # "external_links": [],
    # "single_page": False,
    "toc_title": "Contents",
    "use_download_button": True,
    "show_toc_level": 0,
    "repository_url": "https://github.com/r5py/GIScience_2023",
    "repository_branch": "master",
    "path_to_docs": "source/",
    # "twitter_url": "https://twitter.com/pythongis",
    "google_analytics_id": "",
    "use_edit_page_button": False,
    "use_repository_button": False,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "thebe": False,
        "notebook_interface": "jupyterlab",
        "collapse_navigation": False,
        # Google Colab does not provide an easy way for specifying/building/activating the conda environment
        # in a similar manner as Binder. Hence, let's not keep it. The easiest way seems to be:
        # https://github.com/jaimergp/condacolab
        # But it requires actions from the user nontheless, so atm it's a no-go.
        #"colab_url": "https://colab.research.google.com"
    },

    # Add GIScience logo
    "extra_navbar": """
    <p><b>Sister workshop:</b></p>
    <a href='https://ptal-io.github.io/easm2023/'  target='_blank'> <img src='https://raw.githubusercontent.com/r5py/GIScience_2023/1c4619d401c62295d3df96b725891a9a40416c64/source/_static/EASM_logo.png'> </a>
    <p><br><b>Main conference:</b></p>
    <a href='https://giscience2023.github.io'  target='_blank'> <img src='https://github.com/r5py/GIScience_2023/blob/1c4619d401c62295d3df96b725891a9a40416c64/source/_static/GIScience_logo.png?raw=true'> </a>
    """,

    # Possible announcement for the page
    "announcement": ("📢 All presentations of the accepted papers can now be found under the 'Accepted papers - Short talks' -page. 📢"),
}

html_sidebars = {
    "**": [
        "sidebar-logo.html",
        #"search-field.html",
        #"postcard.html",
        #"recentposts.html",
        #"tagcloud.html",
        #"categories.html",
        #"archives.html",
        "sbt-sidebar-nav.html",
    ]
}

# Allow errors
nb_execution_allow_errors = True

# Do not execute cells
nb_execution_mode = "off"
