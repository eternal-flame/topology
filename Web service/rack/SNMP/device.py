from easysnmp import *
import MySQLdb, logging, getpass

# ipList = [("192.168.1.1", "BKCS"), ('192.168.10.1', "BKCS"),('192.168.10.2', "BKCS"),('192.168.10.3', "BKCS")]
# db = MySQLdb.connect("localhost", "root", "manhkhoa169", "manhdb")

def deviceFormat(string):
	if 'Switch' in string:
		return 'Switch'
	elif 'Router' in string:
		return 'Router'
	else:
		return 'Unknown'


# get function get device information via snmp from an ip address
def get(ip, communityStrings):
	# create a new session
	session = Session(hostname =ip, community =communityStrings, version =2)
	# info contains a list of the fields to retrieve
	info = ['sysContact', 'sysDescr', 'sysLocation', 'sysName', \
			'sysServices', 'sysUpTime']

	deviceInfo = {}
	for item in info:
		try:
			# get information of each data field in the list
			itemValue = session.get('SNMPv2-MIB::' + item + '.0')
			# converting unicode data to ascii format
			deviceInfo[item] = itemValue.value.encode('ascii','ignore')
		except:
			# log the error message to log file if it can not retrieve information 
			# from that ip address
			logging.error("Cannot get device information via SNMP from IP: '%s'", ip)

	if (deviceInfo['sysName']):
		deviceInfo['type'] = deviceFormat(deviceInfo['sysName'])

	# the information retrieved is returned as a Python dictionary	
	return deviceInfo


# getFromIpList function retrieves the snmp information of an ip address list 
# by calling get function multiple times
def getFromIpList(ipList):
    listDeviceInfo = []
    for i in ipList:
    	listDeviceInfo.append(get(i[0], i[1]))

    # return a list of dictionaries containing the collected information
    return listDeviceInfo


# drop function remove all the information of the device table, but retains the structure
def drop(db):
	# create sql statement to remove information in table
	sql = "TRUNCATE TABLE device;"

	try:
		# initialization pointers and process information
		cursor = db.cursor()
		cursor.execute(sql)
		db.commit()
		# logs the database message that has been removed to the log file 
		# for the administrator who is accessing the system
		logging.warning("Database has just been dropped by '%s' ", getpass.getuser())
	except:
		# write the error message to the log file if the database can not be removed
		logging.error("Cannot drop database")
		db.rollback()


# exportInfo function export the device information in the form of a list of python dictionaries
def exportInfo(ipList, db):
	return getFromIpList(ipList)


# insertInfo function inserts the extracted device information of each ip address into the database
def insertInfo(ip, communityStrings, db):
	# device information is obtained by calling the get function and saving it to variable deviceInfo
	deviceInfo = get(ip, communityStrings)
	# create sql statement to insert acquired information into database
	sql = "INSERT INTO device (IP, sysContact, sysDescr, sysLocation, sysName, type, \
			sysServices, sysUpTime, note, community) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', \
			'%s', '%s', '%s', '%s');" % (ip, deviceInfo['sysContact'], deviceInfo['sysDescr'], \
			deviceInfo['sysLocation'], deviceInfo['sysName'], deviceInfo['type'], \
			deviceInfo['sysServices'], deviceInfo['sysUpTime'], 'Null', communityStrings)

	try:
		cursor = db.cursor()
		cursor.execute(sql)
		db.commit()
	except:
		# write the error message to the log file 
		# if the information can not be inserted into the database
		logging.error("Cannot insert device information to database!")
		db.rollback()


# checkDuplicateRecord function check the data already available in the database,
# avoiding the insertion of duplicate records into the database
def checkDuplicateRecord(ipList, db):
	# create sql statement get ip list from device table
    	sql = "SELECT IP FROM device;"

	try:
		cursor = db.cursor()
		cursor.execute(sql)
		# The ipInDtb variable stores the ip tuple in the device table
		ipInDtb = cursor.fetchall()
		db.commit()
	except:
		db.rollback()

	# The ipInDtb variable stores the ip list in the device table
	ipInDatabase = []
	for i in range(len(ipInDtb)):
		ipInDatabase.append(ipInDtb[i][0])

	# ipUpdate variable stores the list of ip addresses that need to update information
	ipUpdate = []
	for ip, communityStrings in ipList:
		# if the IP is not in the database then the list should be updated
		if ip not in ipInDatabase:
			ipUpdate.append(ip)
		else:
			# Otherwise, it will retrieve the snmp information of the ip 
			# and compare the retrieved information with the information already in the database
			deviceInfo = get(ip, communityStrings)
			sql2 = "SELECT sysContact, sysDescr, sysLocation, sysName, type, \
				sysServices, sysUpTime, community FROM device WHERE IP = '%s'" % ip
			try:
				cursor.execute(sql2)
				info2Compare = cursor.fetchall()
				db.commit()
			except:
				db.rollback()

			# if the information is the same then ignore it
			if deviceInfo['sysContact'] == info2Compare[0][0] and \
				deviceInfo['sysDescr'] == info2Compare[0][1] and \
				deviceInfo['sysLocation'] == info2Compare[0][2] and \
				deviceInfo['sysName'] == info2Compare[0][3] and \
				deviceInfo['type'] == info2Compare[0][4] and \
				deviceInfo['sysServices'] == info2Compare[0][5]:
				pass
			else:
				# Again put ip into the list to update, remove the old record in the database
				ipUpdate.append(ip)
				sql3 = "DELETE FROM device WHERE IP = '%s'" % ip
				try:
					cursor.execute(sql3)
					db.commit()
				except:
					db.rollback()

	# returns ip list to update
	return ipUpdate


# updateToTable function call function updateToTable to get a list of ip addresses to update
# then call function insertInfo to insert the retrieved information into the database
def updateToTable(ipList, db):
	ipUpdate = checkDuplicateRecord(ipList, db)

	for ipUp in ipUpdate:
		for ip, communityStrings in ipList:
			if ipUp == ip:
				insertInfo(ip, communityStrings, db)
	# log messages to the log file if the information in the database is updated
	logging.info("Updated device information")


# show function print the information obtained on the console screen
def show(db):
    # show all value in arpTable
    cursor = db.cursor()
    cursor.execute("SELECT deviceId, IP, sysDescr, sysUpTime, sysContact, sysName, type, sysLocation, note  FROM device;")
    print "_______device___________"
    print "| deviceId |        IP       | sysUpTime | sysContact |   sysName	|	type    | sysLocation  |       note       |"    
    # print "portId | deviceId | index |     ifPhysAddress         |      addrres   |"
    for i in cursor.fetchall():
        print "| %8s | %15s | %9s | %10s | %12s | %12s | %12s | %16s |" % (i[0], i[1], i[3], i[4], i[5], i[6], i[7], i[8])
                

