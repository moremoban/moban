pip freeze

cd tests/moban-mako
python setup.py install
cd ../../
nosetests --with-cov --with-doctest --doctest-extension=.rst --cover-package moban --cover-package tests && flake8 . --ignore=E203 --exclude=.moban.d
