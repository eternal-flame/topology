from db import connect

cursor = connect.cursor()


def getFixed(topoId, connectId):
	check = cursor.execute("""
		SELECT fixed FROM topology WHERE topoId = %s AND connectId = %s
	""", (topoId, connectId))

	return None if (check == 0) else cursor.fetchone()[0]


def editEdge(topoId, data):
	deviceA = data['data']['DeviceA']
	deviceB = data['data']['DeviceB']

	cursor.execute("""
		UPDATE ifTable SET ifOperStatus = %s WHERE topoId = %s AND deviceId = %s AND ifPhysAddress = %s
	""", (1 if deviceA['status'] else 2, topoId, deviceA['id'], deviceA['mac'],))

	cursor.execute("""
		UPDATE ifTable SET ifOperStatus = %s WHERE topoId = %s AND deviceId = %s AND ifPhysAddress = %s
	""", (1 if deviceB['status'] else 2, topoId, deviceB['id'], deviceB['mac'],))


def deleteEdge(topoId, connectId):

	fixed = getFixed(topoId, connectId)

	if fixed is not None and fixed == 0:

		cursor.execute("""
			DELETE FROM topology WHERE topoId = %s AND connectId = %s
		""", (topoId, connectId,))

	else:
		return {"status": "fixed"}

	return {"status": "success"}


def addEdge(topoId, data):
	# print data

	deviceA = data['Device A']
	deviceB = data['Device B']

	cursor.execute("""
		INSERT INTO topology (topoId, rackId, MAC1, IP1, MAC2, IP2, fixed)
		VALUES (%s,%s,%s,%s,%s,%s,%s)
	""", (topoId, 0, deviceA['MAC'], deviceA['IP'], deviceB['MAC'], deviceB['IP'], 0))
