web:
	ve python server.py
server:
	ve gunicorn --log-level=DEBUG server:app -b 127.0.0.1:8000
install: pip bower
pip:
	ve pip install -r requirement.txt --trusted-host pypi.douban.com
bower:
	cd static && bower install
