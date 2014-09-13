AWS_SECRET_ACCESS_KEY = 'CVdcUQd3jQXmHK5aaq5yrfYR+tdfYrRMF7M4UVFV'

import base64
import hmac, hashlib
policy_document = open('policy_document.json', 'r').read()
policy = base64.b64encode(policy_document)
signature = base64.b64encode(hmac.new(AWS_SECRET_ACCESS_KEY, policy, hashlib.sha1).digest())
print "policy:", policy
print "sign:", signature