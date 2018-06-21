import easysnmp, json, logging
from easysnmp import snmp_get, snmp_set, snmp_walk
import MySQLdb
# listIP = ["192.168.1.1", '192.168.10.1','192.168.10.2','192.168.10.3','192.168.20.1','192.168.20.2','192.168.20.3']
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"

logging.basicConfig(filename='link.log', level=logging.INFO, format=FORMAT)
logging.info('Started')
# listIP = ["192.168.1.1", '192.168.10.1','192.168.10.2','192.168.10.3']



def readJson(fn):
    with open(fn, "r") as json_file:
        json_data = json.load(json_file)
        return json_data
# print readJson("brigde.json")

def searchPortIdFromFdbPortandIp(dot1dTpFdbPort, ip, db, community):
    temp = snmp_get("1.3.6.1.2.1.17.1.4.1.2."+dot1dTpFdbPort, hostname=ip, community=community, version=2)
    postIndex = temp.value
    cursor = db.cursor()
    exe = "SELECT portId FROM ifTable WHERE address = %s AND ifIndex = %s ;" % ("\"" + ip +"\"", "\"" + postIndex +"\"")
    cursor.execute(exe)
    result = cursor.fetchone()
    if result == None:
        logging.warning("No  found portID from FdbPort %s and Ip %s", dot1dTpFdbPort, ip)
        return None
    return result[0]
    return result[0]

def searchPortIdFromMAC(MAC , db):
    cursor = db.cursor()
    exe = "SELECT portId FROM ifTable WHERE ifPhysAddress = %s ;" % ("\"" + MAC +"\"" )
    cursor.execute(exe)
    result = cursor.fetchone()
    if result == None:
        logging.warning("No  found portID from MAC %s", MAC)
        return None
    return result[0]

def checkExistConnTopo(portId1, portId2, db):
    cursor = db.cursor()
    exe = "SELECT * FROM link WHERE portId1 = %ld AND portId2 = %ld;" % (portId1, portId2)
    cursor.execute(exe)
    result = cursor.fetchone()
    if result != None:
        return True
    exe = "SELECT * FROM link WHERE portId1 = %d AND portId2 = %d;" % (portId2, portId1)
    cursor.execute(exe)
    result = cursor.fetchone()
    if result != None:
        return True
    return False

def addNewTopoConnWith2portId(portId1, portId2, db):
    if checkExistConnTopo(portId1, portId2 , db) == True:
        logging.warning("Connect is exist! PortID %s and portID %s",portId1, portId2)
        # logging.warning('%s before you %s', 'Look', 'leap!')
        return
    elif portId1 == portId2:
        logging.warning("portId cant be the same %s %s",portId1, portId2)
        return
    else:
        if portId1 > portId2:
            portId1, portId2 = portId2, portId1
        cursor = db.cursor()
        exe = "INSERT INTO link(portId1, portId2) VALUES (%d, %d);" % (portId1, portId2)
        print exe
        try:
       # Execute the SQL command
            cursor.execute(exe)
       # Commit your changes in the database
            db.commit()
        except:
       # Rollback in case there is any error
            print "error" 
            db.rollback()

def updateToTable(ipList, db):
    listConn = {}
   
    for i in ipList:
        print i
        ip , community_string = i[0], i[1]
        print  ip , community_string
        a = snmp_walk("BRIDGE-MIB:dot1dTpFdbTable", hostname=ip, community=community_string, version=2)
    
        listInter = {}
        
        for i in a:
        
            try:
                listInter[i.oid_index]={}
            except:
                pass
                # print i.value
        for i in a:
           
            if i.oid == "dot1dTpFdbAddress":
                listInter[i.oid_index][i.oid]= ':'.join(['%0.2x' % ord(x) for x in i.value ])
            else:
                listInter[i.oid_index][i.oid]= i.value
            
                x = searchPortIdFromFdbPortandIp(listInter[i.oid_index]['dot1dTpFdbPort'], ip, db, community_string)
                y = searchPortIdFromMAC(listInter[i.oid_index]['dot1dTpFdbAddress'], db)
                if x == None or y == None:
                    continue
                addNewTopoConnWith2portId(x,y, db)
        listConn[ip]=listInter
        
    	# print listConn[ip]
    listConn = json.dumps(listConn,sort_keys=True, indent=4)
    print listConn
    # with open("brigde.json", "w") as json_file:
    #     json_data = json.dump(listConn, json_file)


def show(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM link;")
    print "___link______"
    for i in cursor.fetchall():
        print i

def drop(db):
    # delete all value in arpTable
    cursor = db.cursor()
    try:
        cursor.execute("TRUNCATE link;")
        db.commit()
        print "Delete link complete!"
    except:
        db.rollback()

try:
    db = MySQLdb.connect("localhost", "root", "toor", "zabbix")
    print "connect to db is ok!"
   	 	
except:
	print "error connect to db !"
	exit()
ipList = [("192.168.1.1", "BKCS"), ('192.168.10.1', "BKCS"),('192.168.10.2', "BKCS"),('192.168.10.3', "BKCS")] 
# drop(db) 
 
# show(db)
# addNewTopoConnWith2portId(23, 99, db)
# updateToTable(ipList, db)
# print checkExistConnTopo(23, 99 , db)
# printlink(db)
# db.close()
print searchPortIdFromMAC("2c:3e:cf:be:e1:89", db)