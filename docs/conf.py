# -*- coding: utf-8 -*-
DESCRIPTION = (
    'Yet another jinja2 cli command for static text generation' +
    ''
)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]
intersphinx_mapping = {
}
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'moban'
copyright = u'2017-2018 Onni Software Ltd.'
version = '0.2.2'
release = '0.2.2'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'mobandoc'
latex_elements = {}
latex_documents = [
    ('index', 'moban.tex',
     'moban Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'moban',
     'moban Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'moban',
     'moban Documentation',
     'Onni Software Ltd.', 'moban',
     DESCRIPTION,
     'Miscellaneous'),
]
