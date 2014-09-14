import os
import requests

AWSAccessKeyId = 'AKIAISF6Q3NMVEHU2EOA'

def upload_file(policy, signature, uuid, filepath=None, content=None):
	url = 'https://roottreebucket.s3.amazonaws.com/'
	payload = {
				'key': '${filename}',
				'AWSAccessKeyId': 'AKIAISF6Q3NMVEHU2EOA',
				'acl': 'public-read',
				'policy': policy,
				'signature': signature,
			   }

	url_list = {}
	#rename the file, and open it
	if filepath is not None:
		base = os.path.basename(filepath)
		original_filename = os.path.splitext(base)[0]
		extension = os.path.splitext(base)[1]
		directory = os.path.dirname(filepath)
		new_filepath = directory + '/' + uuid + extension
		os.rename(filepath, new_filepath)
		files_temp = open(new_filepath, 'r')
		files = {'file': files_temp}
		r = requests.post(url, data=payload, files=files)
		os.rename(new_filepath, filepath)
		files_temp.close()
		url_list['file_url'] = r.headers['location']

	if content is not None:
		print content
		metafile_name = uuid + '_meta.txt'
		metafile = open(metafile_name, 'w')
		metafile.write(content)
		metafile.close()
		metafile = open(metafile_name, 'r')
		files = {'file': metafile}
		r = requests.post(url, data=payload, files=files)
		metafile.close()
		url_list['result_url'] = r.headers['location']
	
	return url_list


if __name__ == "__main__":
	filepath = '/Users/sanketchauhan/Downloads/sanke93.jpg'
	import base64
	import hmac, hashlib
	policy_document = open('policy_document.json', 'r').read()
	policy = base64.b64encode(policy_document)
	signature = base64.b64encode(hmac.new(key, policy, hashlib.sha1).digest())
	print policy
	print '####'
	print signature
	uuid = 'thisworks'
	hi = upload_file(policy=policy, signature=signature, uuid=uuid, filepath=filepath, content='this is content')
	print hi
	#print get_file(url='https://roottreebucket.s3.amazonaws.com/hi.txt')
