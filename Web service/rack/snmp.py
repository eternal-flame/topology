from flask import Blueprint,request

from db import connect
import SNMP.main as snmpAPI

cursor = connect.cursor()

snmp = Blueprint('snmp',__name__)

#Discover all SNMP info with IP and Community string given by user
@snmp.route('/discover/',methods=['POST'])
def discover():
	try:
		deviceList = request.get_json()
		ipList = []

		for ip, comString in deviceList.iteritems():
			ipList.append((ip,comString))

		snmpAPI.getInfo(ipList)
	except:
		return {'status':'error'}

	return {'status':'success'}
	

