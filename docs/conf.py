extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'moban'
copyright = '2016, C.W.'
author = 'C.W.'
version = '0.0.6'
release = '0.0.5'
language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'alabaster'
html_static_path = ['_static']
htmlhelp_basename = 'mobandoc'
latex_elements = {
}
latex_documents = [
    (master_doc, 'moban.tex', 'moban Documentation',
     'C.W.', 'manual'),
]
man_pages = [
    (master_doc, 'moban', 'moban Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'moban', 'moban Documentation',
     author, 'moban', 'One line description of project.',
     'Miscellaneous'),
]
