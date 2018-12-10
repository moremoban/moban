pip freeze

cd tests\moban-mako
python setup.py install
cd ..\..\
nosetests --with-coverage --cover-package=moban --cover-package=tests
flake8 . --exclude=docs --exclude=.moban.d --ignore=E203,E121,E123,E126,E226,E24,E704,W503,W504
