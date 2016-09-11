import nexmo
import urllib
import urllib2

def call_phone(phone_number, text, sendSMS):
	params = {
	    'api_key': "91858d22",
	    'api_secret': "8dff48803f880f73",
	    'to': phone_number,
	    'from': "12674055721",
	    'text': text + " I repeat. " + text
	}

	call_url = 'https://api.nexmo.com/tts/json?' + urllib.urlencode(params)
	call_response = urllib.urlopen(call_url)
	print call_response.read()

	params['text'] = text
	sms_url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(params)
	request = urllib2.Request(sms_url)
	request.add_header('Accept', 'application/json')
	response = urllib2.urlopen(request)
	print response

	