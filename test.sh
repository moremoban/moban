pip freeze

cd tests/moban-mako
python setup.py install
cd ../../
nosetests --rednose --with-cov --with-doctest --doctest-extension=.rst --cov moban --cov tests
