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
	isort -y $(find moban -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
	git diff
	black -l 79 moban
	git diff
	black -l 79 tests
	git diff

uml:
	plantuml -tsvg -o ./images/ docs/*.uml

