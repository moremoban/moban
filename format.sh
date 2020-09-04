isort $(find moban -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
black -l 79 moban
black -l 79 tests
