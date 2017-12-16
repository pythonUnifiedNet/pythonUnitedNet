#! /usr/bin/env python3
import urllib.parse
import urllib.request

region = '420000'
code = '083823482'

url = 'http://59.208.245.184:9970/gateway/api/1/hb/code/accept'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

values = {'region': region, 'code': code}

headers = {'User-Agent': user_agent, 'AppKey': '385092005169987584'}

data = urllib.parse.urlencode(values).encode(encoding='UTF8')

req = urllib.request.Request(url, data, headers)

response = urllib.request.urlopen(req)

the_page = response.read()

print(the_page.decode("utf8"))
