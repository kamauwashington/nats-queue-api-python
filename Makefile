api :
	sanic api:app
subscriber :
	python3 subscriber.py
load-test :
	artillery quick --count 20 -n 20 http://127.0.0.1:8000/ --output report.json
	artillery report report.json

