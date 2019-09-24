pip freeze

nosetests --verbosity=3 --with-cov --with-doctest --doctest-extension=.rst --cover-package moban --cover-package tests
