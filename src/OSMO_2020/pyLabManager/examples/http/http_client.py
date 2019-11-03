import httplib


c = httplib.HTTPConnection('localhost', 8080)
c.request('CUSTOM', '', '{}')
doc = c.getresponse().read()
print(doc)
print(type(doc))
