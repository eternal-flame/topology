from easysnmp import snmp_get, snmp_set, snmp_walk
import easysnmp, json
import MySQLdb

def checkDuplicate(deviceId, ip, db):
    cursor = db.cursor()
    exe = "SELECT deviceId, ip from deviceIp WHERE deviceId = %d AND ip = %s;" % (deviceId, '\"'+ip+'\"')
    cursor.execute(exe)
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True

def updateToTable(db):
    cursor = db.cursor()
    exe = "SELECT deviceId, IP, community FROM device;"
    cursor.execute(exe)
    result = cursor.fetchall()
    for i in result:
        # print i
        a = snmp_walk("RFC1213-MIB::ipAdEntAddr", hostname=i[1], community=i[2], version=2)
        for j in a:
            if not checkDuplicate(i[0],j.value, db):
                exe = "INSERT INTO deviceIp (deviceId, ip) VALUES (%s, %s);" % (i[0], '\"'+j.value+'\"')
                cursor.execute(exe)
    db.commit()

def drop(db):
    # delete all value in arpTable
    cursor = db.cursor()
    try:
        cursor.execute("TRUNCATE deviceIp;")
        db.commit()
    except:
        db.rollback()

def show(db):
    # show all value in arpTable
    cursor = db.cursor()
    cursor.execute("SELECT * FROM deviceIp;")
    print "_______deviceIp___________"
    for i in cursor.fetchall():
        print "%3s --- %3s" % (i[0],i[1])


# drop(db)
# updateDeviceIp(db)
# show(db)
