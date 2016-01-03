sever:
	ve python server.py
install: pip bower
pip:
	ve pip install -r requirement.txt
bower:
	bower install
