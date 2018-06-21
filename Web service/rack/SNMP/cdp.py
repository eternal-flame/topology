from easysnmp import *
import json

cdpCacheEntry = "iso.3.6.1.4.1.9.9.23.1.2.1.1"

def suggestion(ip, communityStrings):
	session = Session(hostname =ip, community =communityStrings, version =2)
	result = session.walk(cdpCacheEntry)

	final = {}
	for x in result:
		if cdpCacheEntry + '.5.' in x.oid:
			final[x.oid.replace(cdpCacheEntry + '.5.', '').encode('ascii','ignore')] = {}

	for y in final:
		temp = {}
		for x in result:
			if cdpCacheEntry + '.5.' + y in x.oid:
				temp['cdpCacheVersion'] = x.value.encode('ascii','ignore')

			if cdpCacheEntry + '.6.' + y in x.oid:
				temp['cdpCacheDeviceId'] = x.value.encode('ascii','ignore')
			
			if cdpCacheEntry + '.8.' + y in x.oid:
				temp['cdpCachePlatform'] = x.value.encode('ascii','ignore')
		final[y] = temp
		temp = {}

	return final
