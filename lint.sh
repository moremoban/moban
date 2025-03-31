flake8 --max-line-length=88 --exclude=.moban.d,docs --ignore=W503,W504,E302,E712,F401
python setup.py checkdocs
