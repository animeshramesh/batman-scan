import nexmo
import urllib

def call_phone(phone_number, text):
	params = {
	    'api_key': "91858d22",
	    'api_secret': "8dff48803f880f73",
	    'to': phone_number,
	    'from': "12674055721",
	    'text': text + " I repeat. " + text
	}

	url = 'https://api.nexmo.com/tts/json?' + urllib.urlencode(params)

	response = urllib.urlopen(url)
	print response.read()