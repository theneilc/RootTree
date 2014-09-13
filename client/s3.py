import os
import requests

policy = 'eyJleHBpcmF0aW9uIjogIjIwMTUtMDEtMDFUMDA6MDA6MDBaIiwKICAiY29uZGl0aW9ucyI6IFsgCiAgICB7ImJ1Y2tldCI6ICJyb290dHJlZWJ1Y2tldCJ9LCAKICAgIFsic3RhcnRzLXdpdGgiLCAiJGtleSIsICIiXSwKICAgIHsiYWNsIjogImF1dGhlbnRpY2F0ZWQtcmVhZCJ9LAogIF0KfQ=='
signature = 'PWrxSaAOYfnLe7q/6tCVXwfaQw8='

def upload_file(filepath):
	url = 'https://roottreebucket.s3.amazonaws.com/'
	payload = {
				'key': '${filename}',
				'AWSAccessKeyId': 'AKIAJQE2SYERMZG7CL5Q',
				'acl': 'authenticated-read',
				'policy': policy,
				'signature': signature
			   }
	files = {'file': open(filepath, 'r')}
	r = requests.post(url, data=payload, files=files)
	return r.headers

if __name__ == "__main__":
	filepath = '/Users/sanketchauhan/Downloads/hi.txt'
	print upload_file(filepath=filepath)