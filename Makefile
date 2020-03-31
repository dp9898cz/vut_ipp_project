#Test makefile for IPP project
.PHONY: test
all:
	cat test | php7.4 parse.php | python3.8 interpret.py --input=input.in
help:
	python3.8 interpret.py --help

bad:
	cat test | php7.4 parse.php | python3.8 interpret.py --input=input.in

bad_args_2:
	python3.8 interpret.py --help --help --help

input:
	python3.8 interpret.py --input=input/input/input.out

test:
	php7.4 test.php --directory=tests/both/ --recursive --jexamxml=test_library/jexamxml/jexamxml.jar --parse-only >index.html