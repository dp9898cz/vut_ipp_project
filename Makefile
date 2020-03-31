#Test makefile for IPP project
.PHONY: test
all:
	cat test | php7.4 parse.php | python3.8 interpret.py --input=input.in
help:
	python3.8 interpret.py --help
parse_only:
	php7.4 test.php --directory=tests/parse_only --recursive --jexamxml=test_library/jexamxml/jexamxml.jar --parse-only >index.html
int_only:
	php7.4 test.php --directory=tests/int_only --recursive --jexamxml=test_library/jexamxml/jexamxml.jar --int-only >index.html
test:
	php7.4 test.php --directory=tests/both --recursive --jexamxml=test_library/jexamxml/jexamxml.jar >index.html
