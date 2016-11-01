#!python

import re
import cgi
import sys
import json
import methods

print "Content-type: application/json"
print ""

form = cgi.FieldStorage()
results = []
terms = ""

response = {'success': False, 'message': [], 'error': [], 'status': 404}

try:
    response['success'] = True
    response['status'] = 200
    response['message'] = methods.getStatus()
except:
    response['error'].append("Really Unexpected error:" + sys.exc_info()[0])

print json.dumps(response, ensure_ascii=False)