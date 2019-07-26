pip freeze
python setup.py develop
nosetests --with-cov --with-doctest --doctest-extension=.rst --cover-package moban --cover-package tests
