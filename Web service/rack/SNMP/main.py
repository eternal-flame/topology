import arptable, iftable, device, topology, deviceip
from db import connect
import time

def getInfo(ipList):
	
	db = connect

	# t0 = time.time()

	# print "Drop all database"
	arptable.drop(db)
	iftable.drop(db)
	device.drop(db)
	topology.drop(db)
	deviceip.drop(db)
	
	# t1 = time.time()
	# print "Running time :", t1-t0, "seconds"
	# t0 = t1
	# print "Get data"
	arptable.updateToTable(ipList, db)
	iftable.updateToTable(ipList, db)
	device.updateToTable(ipList, db)
	iftable.updateDeviceId(db)
	deviceip.updateToTable(db)
	topology.updateToTable(ipList, db)
	# t1 = time.time()
	# print "Running time :", t1-t0, "seconds"
	# t0 = t1
	# print "Show data"
	# arptable.show(db)
	# iftable.show(db)
	# device.show(db)
	# iftable.show(db)
	# topology.show(db)
	# t1 = time.time()
	# print "Running time :", t1-t0, "seconds"
	# t0 = t1
	
	db.commit()
	# print "Records created successfully";
	# db.close()

