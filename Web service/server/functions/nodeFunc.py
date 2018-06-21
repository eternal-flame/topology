from db import connect

cursor = connect.cursor()


def getFixed(topoId, deviceId):
	check = cursor.execute("""
		SELECT fixed FROM device WHERE topoId = %s AND deviceId = %s
	""", (topoId, deviceId))

	return None if (check == 0) else cursor.fetchone()[0]


def getNodeDetail(topoId, deviceId):
	nodeDetail = {}

	cursor.execute("""
		SELECT sysName, IP, sysDescr, sysLocation, sysUpTime, note, fixed, type
		FROM device WHERE topoId = %s AND deviceId = %s
	""", (topoId, deviceId,))

	detail = cursor.fetchone()

	if detail:
		nodeDetail['general'] = {
			'Name'       : detail[0],
			'IP'         : detail[1],
			'Description': detail[2],
			'Location'   : detail[3],
			'Up Time'    : detail[4],
			'Note'		 : detail[5],
		}
		nodeDetail['fixed'] = True if (detail[6] == 1) else False
		nodeDetail['Type']  = detail[7]
	else:
		return False

	ports = {}

	cursor.execute("""
		SELECT ifIndex, ifDescr, ifSpeed, ifPhysAddress, ifOperStatus, note, fixed
		FROM ifTable WHERE topoId=%s AND deviceId=%s
	""", (topoId, deviceId,))

	for port in cursor.fetchall():
		ports[port[0]] = {
			'des'   : port[1],
			'speed' : port[2],
			'mac'   : port[3],
			'status': True if (port[4] == 1) else False,
			'note'  : port[5],
		}

	nodeDetail['portList'] = ports

	return nodeDetail


def editNode(topoId, data):

	deviceId      = data['node']
	generalData = data['data']['general']
	portsData   = data['data']['ports']

	fixed = getFixed(topoId, deviceId)

	if fixed is not None and fixed == 0:
		cursor.execute("""
			UPDATE device SET IP=%s,sysDescr=%s,sysUpTime=%s,sysName=%s,
			type=%s,sysLocation=%s, note=%s WHERE topoId=%s AND deviceId=%s
		""", (generalData['IP'], generalData['Description'], generalData['Up Time'], generalData['Name'],
			data['data']['type'], generalData['Location'], generalData['Note'], topoId, deviceId,))

		for (ifIndex, port) in portsData.iteritems():
			cursor.execute("""
				UPDATE ifTable SET ifDescr=%s, ifSpeed=%s, ifOperStatus=%s,
				note=%s WHERE topoId=%s AND deviceId=%s AND ifIndex=%s
			""", (port['des'], port['speed'], '1' if port['status'] else '2',
				port['note'], topoId, deviceId, ifIndex,))

	else:
		return {"status": "fixed"}

	return {"status": "success"}


def addNode(topoId, data):

	generalData = data['general']
	portsData   = data['ports']

	cursor.execute("""
		INSERT INTO device (topoId,rackId,IP,sysDescr,sysUpTime,
		sysName,type,sysLocation,note,fixed) VALUES
		(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
	""", (topoId, 0, generalData['IP'], generalData['Description'], generalData['Up Time'],
		generalData['Name'], data['type'], generalData['Location'], generalData['Note'], 0,))

	newDeviceId = cursor.lastrowid

	for (id, port) in portsData.iteritems():
		cursor.execute("""
			INSERT INTO ifTable (topoId,rackId,deviceId,deviceIp,ifIndex,
			ifDescr,ifPhysAddress,ifSpeed,ifOperStatus,note,fixed)
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		""", (topoId, 0, newDeviceId, generalData['IP'], port['id'], port['des'], port['mac'],
			port['speed'], '1' if port['status'] else '2', port['note'], 0, ))


def deleteNode(topoId, deviceId):

	fixed = getFixed(topoId, deviceId)

	if fixed is not None and fixed == 0:
		cursor.execute("""
			DELETE FROM topology WHERE IP1 = (SELECT IP FROM device WHERE topoId = %s AND deviceId = %s)
			OR IP2 = (SELECT IP FROM device WHERE topoId = %s AND deviceId = %s)
		""", (topoId, deviceId, topoId, deviceId,))
		cursor.execute("""
			DELETE FROM ifTable WHERE topoId = %s AND deviceId = %s
		""", (topoId, deviceId,))
		cursor.execute("""
			DELETE FROM device WHERE topoId = %s AND deviceId = %s
		""", (topoId, deviceId,))
	else:
		return {"status": "fixed"}

	return {"status": "success"}
