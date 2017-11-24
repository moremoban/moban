all: test

update:
	moban -m mobanfile

test:
	bash test.sh
