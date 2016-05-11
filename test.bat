pip freeze

cd tests\moban-mako
python setup.py install
cd ..\..\
nosetests --with-coverage --with-doctest --doctest-extension=.rst --cover-package=moban --cover-package=tests
