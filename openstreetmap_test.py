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

		if typ == 'json':
			
			if json.loads(text) != test['expected_result']:
				print(url)
				assert False
			
		else:
			if typ == 'xml':
				txt1 = text.split('timestamp')[0]
				txt2 = text.split('timestamp')[1].split('attribution')[1]
				text = txt1 + 'attribution' + txt2

			with open(test['expected_result'], 'r') as f:
				res = f.read()
				f.close()
			
			if text != res:
				print(url)
				assert False


def test_rjson():
	check('reverse', 'json')

def test_djson():
	check('direct', 'json')

def test_dxml():
	check('direct', 'xml')

def test_rxml():
	check('reverse', 'xml')

def test_rhtml():
	check('reverse', 'html')

def test_dhtml():
	check('direct', 'html')
