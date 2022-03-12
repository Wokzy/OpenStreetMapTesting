import requests, json, xmltodict

URL = 'https://nominatim.openstreetmap.org'

def openfile(way, typ):
	with open(f'{way}_{typ}.json', 'r') as f:
		s = f.read()
		f.close()
	return json.loads(s)

def format_url(request_parameters:dict, path, form='json'):
	return "{}{}{}".format(URL, path + '?', '&'.join([f"{i}={request_parameters[i]}" for i in request_parameters]) + f"&format={form}")

def make_request(rqst):
	return requests.post(rqst).text

def check(way, typ):
	tests = openfile(way, typ)

	for test in tests:
		url = format_url(test['request_parameters'], test['test_parameters']['request_path'], typ)
		text = make_request(url)

		if json.loads(text) != test['expected_result']:
			print(url)
			assert False
		