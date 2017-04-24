import json
import re
import sys

def load_json(file):
	#file: path to the .json file
	with open(file) as to_be_loaded:   
	    return json.load(to_be_loaded)

def get_context_value(data, name, get):
	#returns a list of values

	if(name == "common.dataType"):
		return ["DIM"]
	elif(name == "common.authsender"):
		return [None]
	elif(name == "network.protocol"):
		for pair in get['payload']['headers']:
			if(pair['name'] == 'Received'):
				string = pair['value']
				s = string.split("with")[1]
				return [s.split()[0].lower()]
	elif(name == "email.envelope.sender"):
		return [None]
	elif(name == "email.envelope.recipient"):
		return [None]
	elif(name == "email.header.sender"):
		for pair in get['payload']['headers']:
			if(pair['name'] == 'From'):
				emails_and_extra = pair['value']
				return get_emails(emails_and_extra)
	elif(name == "email.header.recipient"):
		for pair in get['payload']['headers']:
			if(pair['name'] == 'Delivered-To'):
				return [pair['value']]

def get_emails(s):
    # modified from https://gist.github.com/dideler/5219706
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    return [email[0] for email in re.findall(regex, s) if not email[0].startswith('//')]

def context(data, get):
	data['context'] = []
	context = data['context']
	context_names = ["common.dataType", "common.authsender", "network.protocol", 
					"email.envelope.sender", "email.envelope.recipient", 
					"email.header.sender", "email.header.recipient"]

	for i in range(len(context_names)):
		context.append({})
		context[i]['name'] = context_names[i]
		context[i]['value'] = get_context_value(data, context_names[i], get)

def body(data, get):
	data["body"] = []
	body = data["body"]
	body_names = ["contentBlockId", "mimeType", "data"]

	i = 0
	body.append({})
	body[i][body_names[i]] = get["id"]
	i+=1

	body.append({})
	body[i][body_names[i]] = get["payload"]["mimeType"]
	i+=1

	body.append({})

	try:
		#for files without attachments
		body[i][body_names[i]] = get["payload"]["body"]["data"]
	except:
		#for files with attachments
		body_value = ""
		for p in get["payload"]["parts"][0]["parts"]:
			body_value += p["body"]["data"]
		body[i][body_names[i]] = body_value
	i+=1

def subject(data, get):
	data['subject'] = []
	subject = data['subject']
	subject_names = ["contentBlockId", "mimeType", "data"]

	i = 0
	subject.append({})
	subject[i][subject_names[i]] = get["threadId"]
	i+=1

	subject.append({})
	subject[i][subject_names[i]] = get["payload"]["mimeType"]
	i+=1

	subject.append({})
	for p in get['payload']['headers']:
		if(p['name'] == 'Subject'):
			subject[i][subject_names[i]] = p["value"]
			break
	i+=1

def main(json_file):

	get = load_json(json_file)
	data = {}

	context(data, get)
	body(data, get)
	subject(data, get)

	request = json.dumps(data)
	print(request)
	return request

if __name__ == '__main__':
	#cmd line: python g2s_parser.py file.json
	main(sys.argv[1])