all:
	ve python sever.py
install:
	ve pip install -r requirement.txt --upgrade
play:
	ve python2 play.py
