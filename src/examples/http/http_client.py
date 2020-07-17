import httplib

c = httplib.HTTPConnection('localhost', 8080)
c.request('OSMO2020COMMAND', '', 'TESTSAMPLEid')

response = c.getresponse()
print(str(response.getheaders()))
# Doing PUT
#body_content = 'BODY CONTENT GOES HERE'
#c.request('PUT', '', body_content)

#print(type(doc))
