from requests import get, post
import json

from db import connect

cursor = connect.cursor()


def discoverNetwork(topoId):
	def getRackDevice(topoId, rackId):
		listDevice = {}

		cursor.execute("""
			SELECT deviceIp, deviceComString FROM topoInfo WHERE
			rackId = %s AND topoId = %s
		""", (rackId, topoId,))

		devices = cursor.fetchall()
		for device in devices:
			listDevice[device[0]] = device[1]

		return listDevice

	cursor.execute("""
		SELECT rackId, rackIp FROM topoInfo WHERE topoId=%s
	""", (topoId,))
	racksList = cursor.fetchall()

	for rack in racksList:
		rackId = rack[0]
		rackIp = rack[1]

		devices = getRackDevice(topoId, rackId)
		post('http://' + rackIp + ':1234/snmp/discover/', data=devices)


def syncTable(topoId):

	def syncDevice(topoId, rackId, rackIp):

		def getDeviceId(ip):
			check = cursor.execute("""
				SELECT deviceId FROM device WHERE topoId=%s AND IP=%s
			""", (topoId, ip,))

			return 0 if (check == 0) else cursor.fetchone()[0]

		def updateDevice(deviceId, device):
			cursor.execute("""
				UPDATE device SET sysDescr=%s, sysUpTime=%s, sysName=%s,
				sysLocation=%s, sysServices=%s, fixed=2 WHERE deviceId=%s
			""", (device['sysDescr'], device['sysUpTime'], device['sysName'],
				device['sysLocation'], device['sysServices'], deviceId,))

		def insertDevice(device):
			cursor.execute("""
				INSERT INTO device (topoId,rackId,IP,sysDescr,sysUpTime,sysName,type,sysLocation,sysServices,fixed)
				VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
			""", (topoId, rackId, device['IP'], device['sysDescr'], device['sysUpTime'],
				device['sysName'], device['type'], device['sysLocation'], device['sysServices'], 2,))

		def deleteOldData():
			cursor.execute("""
				DELETE FROM device WHERE fixed=1 AND topoId=%s AND rackId=%s
			""", (topoId, rackId,))
			cursor.execute("""
				UPDATE device SET fixed=1 WHERE fixed=2 AND topoId=%s AND rackId=%s
			""", (topoId, rackId,))

		rackURL  = 'http://' + rackIp + ':1234/sync/'
		r_device = get(rackURL + 'device/')

		if r_device.status_code != 200:
			return

		deviceData = json.loads(r_device.content)

		for device in deviceData:
			deviceId = getDeviceId(device['IP'])

			if (deviceId != 0):
				updateDevice(deviceId, device)
			else:
				insertDevice(device)

		deleteOldData()

	def syncIfTable(topoId, rackId, rackIp):

		def getDeviceId(ip):
			check = cursor.execute("""
				SELECT deviceId FROM device WHERE topoId=%s AND IP=%s
			""", (topoId, ip,))

			return 0 if (check == 0) else cursor.fetchone()[0]

		def getPortId(deviceId, ifIndex):
			check = cursor.execute("""
				SELECT portId FROM ifTable WHERE topoId=%s AND deviceId=%s AND ifIndex=%s
			""", (topoId, deviceId, ifIndex,))

			return 0 if (check == 0) else cursor.fetchone()[0]

		def updateIfTable(portId, port):
			cursor.execute("""
				UPDATE ifTable SET ifDescr=%s, ifType=%s, ifMtu=%s, ifSpeed=%s, ifPhysAddress=%s,
				ifAdminStatus=%s, ifOperStatus=%s, ifLastChange=%s, fixed=2 WHERE topoId=%s AND portId=%s
			""", (port['ifDescr'], port['ifType'], port['ifMtu'], port['ifSpeed'], port['ifPhysAddress'],
				port['ifAdminStatus'], port['ifOperStatus'], port['ifLastChange'], topoId, portId,))

		def insertIfTable(port, deviceId):
			cursor.execute("""
				INSERT INTO ifTable (topoId,rackId,deviceId,deviceIp,ifIndex,ifDescr,ifType,ifMtu,
				ifSpeed,ifPhysAddress,ifAdminStatus,ifOperStatus,ifLastChange,fixed)
				VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,2)
			""", (topoId, rackId, deviceId, port['address'], port['ifIndex'], port['ifDescr'], port['ifType'], port['ifMtu'],
			port['ifSpeed'], port['ifPhysAddress'], port['ifAdminStatus'], port['ifOperStatus'], port['ifLastChange'],))

		def deleteOldData():
			cursor.execute("""
				DELETE FROM ifTable WHERE fixed=1 AND topoId=%s AND rackId=%s
			""", (topoId, rackId,))
			cursor.execute("""
				UPDATE ifTable SET fixed=1 WHERE fixed=2 AND topoId=%s AND rackId=%s
			""", (topoId, rackId,))

		rackURL   = 'http://' + rackIp + ':1234/sync/'
		r_ifTable = get(rackURL + 'ifTable/')

		if r_ifTable.status_code != 200:
			return
		ifTableData = json.loads(r_ifTable.content)

		for port in ifTableData:
			deviceId = getDeviceId(port['address'])
			if (deviceId == 0):
				continue

			portId = getPortId(deviceId, port['ifIndex'])

			if (portId != 0):
				updateIfTable(portId, port)
			else:
				insertIfTable(port, deviceId)

		deleteOldData()

	def syncTopology(topoId, rackId, rackIp):

		def getLinkId(data):
			cursor.execute("""
				SELECT connectId, MAC1, MAC2 FROM topology WHERE topoId = %s AND rackId = %s
			""", (topoId, rackId))
			links = cursor.fetchall()

			for link in links:
				if ((data['MAC1'] == link[1] and data['MAC2'] == link[2]) or (data['MAC1'] == link[2] and data['MAC2'] == link[1])):
					return link[0]
			return 0

		def updateTopology(linkId):
			
			cursor.execute("""
				UPDATE topology SET fixed = %s WHERE topoId = %s AND connectId = %s
			""", (2, topoId, linkId,))

		def insertTopology(link):
			
			cursor.execute("""
				INSERT INTO topology (topoId, rackId, IP1, MAC1, IP2, MAC2, fixed) VALUES (%s,%s,%s,%s,%s,%s,%s)
			""", (topoId, rackId, link['IP1'], link['MAC1'], link['IP2'], link['MAC2'], 2,))

		def deleteOldData():
			cursor.execute("""
				DELETE FROM topology WHERE topoId = %s AND rackId = %s AND fixed = %s
			""", (topoId, rackId, 1,))

			cursor.execute("""
				UPDATE topology SET fixed = %s WHERE topoId = %s AND rackId = %s AND fixed = %s
			""", (1, topoId, rackId, 2,))

		rackURL = 'http://' + rackIp + ':1234/sync/'
		r_topology = get(rackURL + 'topology/')

		if r_topology.status_code != 200:
			return
		topology = json.loads(r_topology.content)

		for link in topology:
			linkId  = getLinkId(link)

			if (linkId != 0):
				updateTopology(linkId)
			else:
				insertTopology(link)

		deleteOldData()

	cursor.execute("""
		SELECT rackId, rackIp FROM topoInfo WHERE topoId=%s
	""", (topoId,))
	racksList = cursor.fetchall()

	for rack in racksList:
		rackId = rack[0]
		rackIp = rack[1]

		syncDevice(topoId, rackId, rackIp)
		syncIfTable(topoId, rackId, rackIp)
		syncTopology(topoId, rackId, rackIp)


def getTopoDetail(topoId):

	def createUnknownNode(mac, ip):
		newNode = {}

		newNode['id'] = mac if mac else ip
		newNode['ip']   = ip if ip else 'Unknown'
		newNode['name'] = "Unknown device"
		newNode['type'] = 'Unknown'

		return newNode

	def generateNodes():
		nodes = []

		cursor.execute("""
			SELECT deviceId, rackId, IP, sysName, type FROM device WHERE topoId = %s
		""", (topoId, ))

		for node in cursor.fetchall():
			newNode = {}
			
			newNode['id']    = node[0]
			newNode['group'] = node[1]
			newNode['ip']    = node[2]
			newNode['name']  = node[3]
			newNode['type']  = node[4]

			nodes.append(newNode)

		return nodes

	def generateEdges(nodes):
		edges = []

		cursor.execute("""
			SELECT connectId, MAC1, IP1, MAC2, IP2, fixed FROM topology WHERE topoId = %s
		""", (topoId,))

		for edge in cursor.fetchall():
			newEdge = {}
			newEdge['id'] = edge[0]

			cursor.execute("""
				SELECT deviceId, ifIndex, ifOperStatus FROM ifTable
				WHERE topoId = %s AND ifPhysAddress = %s AND deviceIp = %s
			""", (topoId, edge[1], edge[2],))

			device = cursor.fetchone()

			if device:
				newEdge['deviceA'] = device[0]
				newEdge['macA']    = edge[1]
				newEdge['portA']   = device[1]
				newEdge['statusA'] = device[2]
			else:
				newUnknownNode = createUnknownNode(edge[1], edge[2])
				nodes.append(newUnknownNode)

				newEdge['deviceA'] = edge[1] if edge[1] else edge[2]
				newEdge['macA']    = edge[1]
				newEdge['portA']   = 'Unknown'
				newEdge['statusA'] = 1

			cursor.execute("""
				SELECT deviceId, ifIndex, ifOperStatus FROM ifTable
				WHERE topoId = %s AND ifPhysAddress = %s AND deviceIp = %s
			""", (topoId, edge[3], edge[4],))

			device2 = cursor.fetchone()

			if device2:
				newEdge['deviceB'] = device2[0]
				newEdge['macB']    = edge[3]
				newEdge['portB']   = device2[1]
				newEdge['statusB'] = device2[2]
			else:
				newUnknownNode = createUnknownNode(edge[3], edge[4])
				nodes.append(newUnknownNode)

				newEdge['deviceB'] = edge[3] if edge[3] else edge[4]
				newEdge['macB']    = edge[3]
				newEdge['portB']   = 'Unknown'
				newEdge['statusB'] = 1

			edges.append(newEdge)

		return edges

	nodes = generateNodes()
	edges = generateEdges(nodes)

	return {'nodes': nodes, 'edges': edges}
