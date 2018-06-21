import easysnmp, json
from easysnmp import snmp_get, snmp_set, snmp_walk


def decodePhysAddress(addr):
    return ':'.join(['%0.2x' % ord(x) for x in addr ])

def searchportIdFromFdbPortandIp(dot1dTpFdbPort, ip, db, community):
    # dot1dTpFdbPort give you the number of port, from that, you
    # need to find the index of that port, compare with ifTable to file portID 
    temp = snmp_get("1.3.6.1.2.1.17.1.4.1.2."+dot1dTpFdbPort, hostname=ip, community=community, version=2)
    postIndex = temp.value
    cursor = db.cursor()
    exe = "SELECT portId, deviceId, address, ifPhysAddress FROM ifTable WHERE address = %s AND ifIndex = %s ;" % ("\"" + ip +"\"", "\"" + postIndex +"\"")
    cursor.execute(exe)
    result = cursor.fetchone()
    
    if result == None:
        return False
    # print result
    return result

def searchportIdFromMAC(MAC , db):
    # Find the port have that MAC and return its portID
    cursor = db.cursor()
    exe = "SELECT portId, deviceId, address, ifPhysAddress FROM ifTable WHERE ifPhysAddress = %s ;" % ("\"" + MAC +"\"" )
    cursor.execute(exe)
    result = cursor.fetchone()
    # print type(result[0]), result[0]
    if result == None:
        return False
    # print result
    return result

def checkExistConnTopo(portId1, portId2, db):
    # Return True if that conn not exist in topologu table and otherwise
    cursor = db.cursor()
    exe = "SELECT * FROM topology WHERE portId1 = %ld AND portId2 = %ld;" % (portId1, portId2)
    cursor.execute(exe)
    result = cursor.fetchone()
    if result != None:
        return True
    exe = "SELECT * FROM topology WHERE portId1 = %d AND portId2 = %d;" % (portId2, portId1)
    cursor.execute(exe)
    result = cursor.fetchone()
    if result != None:
        return True
    return False

def addNewTopoConnWithMac(portId, MAC, db):
    # In some case, from MAC you can find portId in ifTable, you should get it in MAC  
    cursor = db.cursor()
    exe = "SELECT * FROM topology WHERE portId1 = %d AND deviceId1 = %d AND IP1 = %s AND MAC1 = %s AND MAC2 = %s;" % (portId[0], portId[1], "\""+portId[2]+"\"", "\""+portId[3]+"\"", "\""+MAC+"\"")
    cursor.execute(exe)
    result = cursor.fetchone()
    if result != None:
        return
    exe = "INSERT INTO topology(portId1, deviceId1, IP1, MAC1, MAC2) VALUES (%d, %d, %s, %s, %s);" % (portId[0], portId[1], "\""+portId[2]+"\"", "\""+portId[3]+"\"", "\""+MAC+"\"")
    print exe
    try:
       # Execute the SQL command
        cursor.execute(exe)
       # Commit your changes in the database
        db.commit()
    except:
       # Rollback in case there is any error
        # print "error" 
        db.rollback()
def addNewTopoConnWith2portId(portId1, portId2, db):
    # print portId1, portId2
    if checkExistConnTopo(portId1[0], portId2[0] , db) == True:
        return
    elif portId1[0] == portId2[0]:
        return
    else:
        if portId1[0] > portId2[0]:
            portId1, portId2 = portId2, portId2
        cursor = db.cursor()
        exe = "INSERT INTO topology(portId1, deviceId1, IP1, MAC1, portId2, deviceId2, IP2, MAC2) VALUES (%d, %d, %s, %s, %d, %d, %s, %s);" % (portId1[0], portId1[1], "\""+portId1[2]+"\"", "\""+portId1[3]+"\"", portId2[0], portId2[1], "\""+portId2[2]+"\"", "\""+portId2[3]+"\"")
        # print exe
        try:
       # Execute the SQL command
            cursor.execute(exe)
       # Commit your changes in the database
            db.commit()
        except:
       # Rollback in case there is any error
            db.rollback()

def ip2deviceId(ip, db):
    cursor = db.cursor()
    exe = "SELECT deviceId FROM deviceIp WHERE ip = %s;" % ('\"'+ip+'\"')
    cursor.execute(exe)
    result = cursor.fetchone()
    if result == None:
        return False
    return result

def getAllIpOfDeviceId(deviceId, db):
    cursor = db.cursor()
    exe = "SELECT ip FROM deviceIp WHERE deviceId = %s;" % deviceId
    cursor.execute(exe)
    result = cursor.fetchall()
    if result == None:
        return False
    
    return [i[0] for i in result]
def addTopoWithLinkArp(arpConnect, db):
    # print arpConnect
    ip1, mac1 = arpConnect[0]
    ip2, mac2 = arpConnect[1]
    portId1 = searchportIdFromMAC(mac1, db)
    portId2 = searchportIdFromMAC(mac2, db)
    deviceId1 = ip2deviceId(ip1, db)
    deviceId2 = ip2deviceId(ip2, db)
    if portId1 == False:
        portId1 = "NULL"
    else:
        portId1 = portId1[0]
    if portId2 == False:
        portId2 = "NULL"
    else:
        portId2 = portId2[0]
    if deviceId1 == False:
        deviceId1 = "NULL"
    else:
        deviceId1 = deviceId1[0]
    if deviceId2 == False:
        deviceId1 = "NULL"
    else:
        deviceId2 = deviceId2[0]

    exe = "INSERT INTO topology(portId1, deviceId1, IP1, MAC1, portId2, deviceId2, IP2, MAC2) VALUES (%d, %d, %s, %s, %d, %d, %s, %s);" % (portId1, deviceId1, "\""+ip1+"\"", "\""+mac1+"\"", portId2, deviceId2, "\""+ip2+"\"", "\""+mac2+"\"")
    # print portId1, deviceId1, "\""+ip1+"\"", "\""+mac1+"\"", portId2, deviceId2, "\""+ip2+"\"", "\""+mac2+"\""
    cursor = db.cursor()
    
    try:
       # Execute the SQL command
        cursor.execute(exe)
       # Commit your changes in the database
        db.commit()
    except:
       # Rollback in case there is any error
        # print "error" 
        db.rollback()
def linkByArp(ip, community, db):
    a = snmp_walk("RFC1213-MIB::atPhysAddress", hostname=ip, community=community, version=2)
    deviceIps = getAllIpOfDeviceId(ip2deviceId(ip, db), db)
    # print deviceIps
    link = {}
    for i in a:
        temp_oid = i.oid_index.split('.')
        index = '.'.join(temp_oid[:2])
        ipAt = '.'.join(temp_oid[2:])
        try:
            link[index].append((ipAt, decodePhysAddress(i.value)))
        except:
            link[index] = []
            link[index].append((ipAt, decodePhysAddress(i.value)))
    for i in link.values():
        if len(i) == 2:
            addTopoWithLinkArp(i, db)



def updateToTable(ipList, db):
    listConn = {}
    for i in ipList:
        ip, community = i[0], i[1]
        a = snmp_walk("BRIDGE-MIB:dot1dTpFdbTable", hostname=ip, community=community, version=2)
    # a = snmp_walk("BRIDGE-MIB:dot1dTpFdbAddress", hostname=ip, community='BKCS', version=2)
        listInter = {}
        if len(a) == 0:
            ### The device cannot get brigde-mib
            linkByArp(ip, community, db)
            continue
        
        for i in a:
        
            try:
                listInter[i.oid_index]={}
            except:
                pass
               
        for i in a:
            # print i
            if i.oid == "dot1dTpFdbAddress":
                listInter[i.oid_index][i.oid]= ':'.join(['%0.2x' % ord(x) for x in i.value ])
                
            else:
                listInter[i.oid_index][i.oid]= i.value
            
                x = searchportIdFromFdbPortandIp(listInter[i.oid_index]['dot1dTpFdbPort'], ip, db, community)
                y = searchportIdFromMAC(listInter[i.oid_index][u'dot1dTpFdbAddress'], db)
                print x, y, ip
                if x != False :
                    if y != False:
                        addNewTopoConnWith2portId(x,y, db)
                    else:
                        addNewTopoConnWithMac(x, listInter[i.oid_index][u'dot1dTpFdbAddress'], db)
        listConn[ip]=listInter
        
    #     # print listConn[ip]
    # listConn = json.dumps(listConn,sort_keys=True, indent=4)
    # print listConn
    # with open("brigde.json", "w") as json_file:
    #     json_data = json.dump(listConn, json_file)

def deviceId2sysName(deviceId, db): 
    cursor = db.cursor()
    exe = "SELECT * FROM device WHERE device1 = %ld AND portId2 = %ld;" % (portId1, portId2)
    cursor.execute(exe)
    result = cursor.fetchone()
    if result != None:
        return True
    exe = "SELECT * FROM topology WHERE portId1 = %d AND portId2 = %d;" % (portId2, portId1)
    cursor.execute(exe)
    result = cursor.fetchone()
    if result != None:
        return True
    return False

def show(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM topology;")
    print "___topology______"
    for i in cursor.fetchall():
        print i

def drop(db):
    # delete all value in arpTable
    cursor = db.cursor()
    try:
        cursor.execute("TRUNCATE topology;")
        db.commit()
    except:
        db.rollback()



# try:
#     db = MySQLdb.connect("localhost", "root", "toor", "zabbix")
#     print "connect to db is ok!"
# except:
#     print "error connect to db !"
#     exit()
# ipList = [("192.168.1.1", "BKCS"), ('192.168.10.1', "BKCS"),('192.168.10.2', "BKCS"),('192.168.10.3', "BKCS")] 
# # drop(db)
# updateToTable(ipList, db)

# getAll(ipList)