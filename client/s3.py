import os
import requests

policy = 'eyJleHBpcmF0aW9uIjogIjIwMTUtMDEtMDFUMDA6MDA6MDBaIiwKICAiY29uZGl0aW9ucyI6IFsgCiAgICB7ImJ1Y2tldCI6ICJyb290dHJlZWJ1Y2tldCJ9LCAKICAgIFsic3RhcnRzLXdpdGgiLCAiJGtleSIsICIiXSwKICAgIHsiYWNsIjogInB1YmxpYy1yZWFkIn0sCiAgXQp9'
signature = 'cppCKmmC45scE+EPLGl3idSn7/A='
AWSAccessKeyId = 'AKIAJQE2SYERMZG7CL5Q'

def upload_file(filepath=None, content=None):
	url = 'https://roottreebucket.s3.amazonaws.com/'
	payload = {
				'key': '${filename}',
				'AWSAccessKeyId': 'AKIAJQE2SYERMZG7CL5Q',
				'acl': 'public-read',
				'policy': policy,
				'signature': signature
			   }
	files = {'file': open(filepath, 'r')}
	r = requests.post(url, data=payload, files=files)
	print r.content
	return r.headers

def get_file(url):
	url = url
	payload = {'AWSAccessKeyId': AWSAccessKeyId,
				'Signature': signature
				}
	print payload
	r = requests.get(url, data=payload)
	print r.url
	return r.headers

if __name__ == "__main__":
	filepath = '/Users/sanketchauhan/Downloads/hi.txt'
	#print upload_file(filepath=filepath)
	print get_file(url='https://roottreebucket.s3.amazonaws.com/hi.txt')

#if not an image return contents
#uuid.uuid4().hex