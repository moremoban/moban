pip freeze

cd tests\moban-mako
python setup.py install
cd ..\..\
nosetests --with-cov --with-doctest --doctest-extension=.rst --cov moban --cov tests
