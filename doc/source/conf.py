import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'Piggy_game'
author = 'Dechen Dolkar, Rebecca Blixt and Hmon Wutt'
release = '1.0'

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
