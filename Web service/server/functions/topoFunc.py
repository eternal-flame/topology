
from db import connect

cursor = connect.cursor()


# Get highest id existing
def getHighestTopoId():
	cursor.execute("""
		SELECT MAX(topoId) FROM topoInfo
	""")
	highestId = cursor.fetchone()[0]

	return (highestId if highestId else 0)


# Get list of topologies available
def getToposList():
	topoList = []
	cursor.execute("""
		SELECT DISTINCT topoId,topoName FROM topoInfo
	""")
	topos = cursor.fetchall()

	for topo in topos:
		newTopo = {'id': topo[0], 'name': topo[1]}
		topoList.append(newTopo)

	return topoList


# Get detail of a topology about rack controllers and devices based on topoId
def getTopoDetail(topoId):

	# General info
	topology       = {}
	topology['id'] = topoId

	cursor.execute("""
		SELECT DISTINCT topoName FROM topoInfo WHERE topoId = %s
	""", (topoId,))

	topology['name']  = cursor.fetchone()[0]
	topology['racks'] = {}

	# Rack info
	cursor.execute("""
		SELECT DISTINCT rackId, rackName, rackIp FROM topoInfo WHERE topoId = %s
	""", (topoId,))

	racks = cursor.fetchall()
	for rack in racks:
		newRack            = {}
		rackId             = rack[0]
		newRack['name']    = rack[1]
		newRack['ip']      = rack[2]
		newRack['devices'] = {}

		# Device info
		cursor.execute("""
			SELECT deviceId, deviceIp, deviceComString FROM topoInfo WHERE topoId = %s AND rackId = %s
		""", (topoId, rackId,))

		devices = cursor.fetchall()

		for device in devices:
			newDevice              = {}
			deviceId               = device[0]
			newDevice['ip']        = device[1]
			newDevice['comString'] = device[2]

			newRack['devices'][deviceId] = newDevice

		topology['racks'][rackId] = newRack

	return topology


# Add new topology to topology list
def addNewTopo(topo):
	# Generate info about the topology
	topoId   = getHighestTopoId() + 1
	topoName = topo['name']

	rackIndex   = 0
	deviceIndex = 0
	for rack in topo['racks'].itervalues():
		# Generate info about each rack controllers

		rackId    = rackIndex + 1
		rackIndex += 1
		rackName  = rack['name']
		rackIp    = rack['ip']

		for device in rack['devices'].itervalues():
			# Generate info about each devices
			deviceId    = deviceIndex + 1
			deviceIndex += 1
			deviceIp    = device['ip']
			comString   = device['comString']

			# Insert to topoInfo table
			cursor.execute("""
				INSERT INTO topoInfo (topoId, topoName, rackId, rackName, rackIp, deviceId, deviceIp, deviceComString)
				VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
			""", (topoId, topoName, rackId, rackName, rackIp, deviceId, deviceIp, comString,))
	connect.commit()


# Edit name, IP, community string of devices in a topology
def editTopo(topo):
	topoId   = topo['id']
	topoName = topo['name']

	cursor.execute("""
		UPDATE topoInfo SET topoName = %s WHERE topoId = %s
	""", (topoName, topoId,))

	for rackId, rack in topo['racks'].iteritems():
		rackIp   = rack['ip']
		rackName = rack['name']

		cursor.execute("""
			UPDATE topoInfo SET rackIp=%s, rackName=%s WHERE topoId=%s AND rackId=%s
		""", (rackIp, rackName, topoId, rackId,))

		for deviceId, device in rack['devices'].iteritems():
			deviceIp  = device['ip']
			comString = device['comString']

			cursor.execute("""
				UPDATE topoInfo SET deviceIp=%s, deviceComString=%s WHERE topoId=%s AND deviceId=%s
			""", (deviceIp, comString, topoId, deviceId,))
	connect.commit()


# Delete a existing topology
def deleteTopo(topoId):
	highestId = getHighestTopoId()

	# Delete this topology
	cursor.execute("""
		DELETE FROM topoInfo WHERE topoId = %s
	""", (topoId,))

	# Reindex another topologies
	for Id in range(topoId, highestId):
		cursor.execute("""
			UPDATE topoInfo SET topoId = %s WHERE topoId = %s
		""", (Id, Id + 1))
	connect.commit()
