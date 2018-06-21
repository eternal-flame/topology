from easysnmp import *
import json
lldpObjects = "iso.0.8802.1.1.2.1"

def suggestion(ip, communityStrings):
	session = Session(hostname =ip, community =communityStrings, version =2)
	result = session.walk(lldpObjects)

	final = {}
	for x in result:
		if lldpObjects + '.3.3' in x.oid:
			final['lldpLocSysName'] = x.value.encode('ascii','ignore')
		if lldpObjects + '.3.4' in x.oid:
			final['lldpLocSysDesc'] = x.value.encode('ascii','ignore')
		if lldpObjects +'.5' and '.1.2.6.0' in x.oid:
			final['lldpXMedLocMfgName'] = x.value.encode('ascii','ignore')
		if lldpObjects + '.5' and '.1.2.7.0' in x.oid:
			final['lldpXMedLocModelName'] = x.value.encode('ascii','ignore')

	return final


def userSuggesstion(ipList):
    userSuggesstionDict = {}
    for i in ipList:
    	userSuggesstionDict[i[0]] = suggestion(i[0], i[1])

    return userSuggesstionDict



# ipList = [("192.168.1.1", "BKCS"), ('192.168.10.1', "BKCS"),('192.168.10.2', "BKCS"),('192.168.10.3', "BKCS")]
ipList = [('192.168.10.1', "BKCS")]
print json.dumps(userSuggesstion(ipList),sort_keys=True, indent=4) 