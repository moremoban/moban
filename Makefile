all: test

install:
	pip install .

install_test:
	pip install -r tests/requirements.txt

update:
	moban -m mobanfile

git-diff-check:
	git diff --exit-code

test:
	bash test.sh

lint:
	bash lint.sh
	yamllint -d "{extends: default, rules: {line-length: {max: 120}}}" .moban.cd/changelog.yml
	yamllint -d "{extends: default, ignore: .moban.cd/changelog.yml}" .

format:
	bash format.sh

uml:
	plantuml -tsvg -o ./images/ docs/*.uml


doc: uml
	sphinx-build -b html docs build
