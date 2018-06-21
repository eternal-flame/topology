from flask import *

from db import connect
import SNMP.main as snmpAPI

synchronize = Blueprint('synchronize',__name__)

cursor = connect.cursor()

#Discover all SNMP info with IP and Community string given by user
@synchronize.route('/device/',methods=['GET'])
def device():
	result = []
	try:
		cursor.execute("""SELECT IP, sysDescr, sysUpTime, sysContact, sysName, \
			type, sysLocation, sysServices, note, community, fixed FROM device;""")

		rows = cursor.fetchall()
		for row in rows:
			temp                = {}
			temp['IP']          = row[0]
			temp['sysDescr']    = row[1]
			temp['sysUpTime']   = row[2]
			temp['sysContact']  = row[3]
			temp['sysName']     = row[4]
			temp['type']        = row[5]
			temp['sysLocation'] = row[6]
			temp['sysServices'] = row[7]
			temp['note']        = row[8]
			temp['community']   = row[9]
			temp['fixed']       = row[10]

			result.append(temp)
	except:
		print 'not execute'

	return result

@synchronize.route('/ifTable/',methods=['GET'])
def ifTable():
	result = []
	try:
		cursor.execute("SELECT ifIndex, ifDescr, ifType, ifMtu, ifSpeed, ifPhysAddress, \
			ifAdminStatus, ifOperStatus, ifLastChange, note, address, portId FROM ifTable;")
		
		rows = cursor.fetchall()
		for row in rows:
			temp                  = {}
			temp['ifIndex']       = row[0]
			temp['ifDescr']       = row[1]
			temp['ifType']        = row[2]
			temp['ifMtu']         = row[3]
			temp['ifSpeed']       = row[4]
			temp['ifPhysAddress'] = row[5]
			temp['ifAdminStatus'] = row[6]
			temp['ifOperStatus']  = row[7]
			temp['ifLastChange']  = row[8]
			temp['note']          = row[9]
			temp['address']       = row[10]
			temp['portId']        = row[11]

			result.append(temp)
	except:
		print 'not execute'

	return result

@synchronize.route('/topology/',methods=['GET'])
def topology():
	result = []
	try:
		cursor.execute("SELECT sysName1, IP1, MAC1 FROM topology;")
		
		rows = cursor.fetchall()
		for row in rows:
			temp             = {}
			temp['sysName1'] = row[0]
			temp['IP1']      = row[1]
			temp['MAC1']     = row[2]
			temp['sysName2'] = row[0]
			temp['IP2']      = row[1]
			temp['MAC2']     = row[2]

			result.append(temp)
	except:
		print 'not execute'

	return result