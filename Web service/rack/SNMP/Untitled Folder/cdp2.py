from easysnmp import *

cdpCacheEntry = "iso.3.6.1.4.1.9.9.23.1.2.1.1"

def suggestion(ip, communityStrings):
	session = Session(hostname =ip, community =communityStrings, version =2)
	result = session.walk(cdpCacheEntry)

	final = {}
	for x in result:
		# print x.oid, x.value
		rev = x.oid.encode('ascii', 'ignore')[::-1]
		index1 = rev.find('.')
		index2 = rev.find('.', index1+1)
		if rev[:index2] not in final:
			final[rev[:index2][::-1]] = {}

	for y in final:
		temp = {}
		for x in result:
			rev = x.oid.encode('ascii', 'ignore')[::-1]
			index1 = rev.find('.')
			index2 = rev.find('.', index1+1)
			index3 = rev.find('.', index2+1)
			index4 = rev.find('.', index3+1)
			index5 = rev.find('.', index4+1)
			index6 = rev.find('.', index5+1)
			index7 = rev.find('.', index6+1)
			prefix = rev[:index7][::-1]

			if prefix and '.5.' in x.oid:
				if y in x.oid:
					temp['cdpCacheVersion'] = x.value.encode('ascii','ignore')

			if prefix and '.6.' in x.oid:
				if y in x.oid:
					temp['cdpCacheDeviceId'] = x.value.encode('ascii','ignore')
					
			if prefix and '.8.' in x.oid:
				if y in x.oid:
					temp['cdpCachePlatform'] = x.value.encode('ascii','ignore')
		final[y] = temp
		temp = {}

	return final


print suggestion('192.168.10.1', 'BKCS')