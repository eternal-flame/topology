# listIP = [ '192.168.10.1',"192.168.1.1",'192.168.10.2','192.168.10.3','192.168.20.1','192.168.20.2','192.168.20.3']
from easysnmp import snmp_get, snmp_set, snmp_walk 
import easysnmp, json
from easysnmptable import Session

# def mergeTupleToDictIfindex(table):
#     itemIfTable = []
#   for index, row in table.rows.items():
#       row['ifIndex'] = index
#       itemIfTable += row
#   return dict(itemIfTable)    
            
def get(ip, community_string):
    #return iftable in class table of easysnmptable
    with Session(hostname=ip, community=community_string, version=2) as session:
        try:
            table = session.gettable('IF-MIB::ifTable')
            return table
        except:
            pass
        # for index, row in table.rows.items():
        #   print index, row[]

def decodePhysAddress(addr):
    return ':'.join(['%0.2x' % ord(x) for x in addr ])

def getFromIpList(ipList):
    listIftableItems = []
    for i in ipList:
        data = get(i[0], i[1])
        listIftableItems += data.rows.items()
    return dict(listIftableItems)

def updateToTable(ipList,db):
    cursor = db.cursor()
    for i in ipList:
        for index, row in get(i[0], i[1]).rows.items():
        
            exe = """INSERT INTO ifTable(ifIndex, ifDescr, ifType, ifMtu, ifSpeed, ifPhysAddress, ifAdminStatus, ifOperStatus, ifLastChange, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)\
            ;""" % ('\"'+index+'\"', '\"'+row["ifDescr"]+'\"', '\"'+row["ifType"]+'\"', '\"'+row["ifMtu"]+'\"', '\"'+row["ifSpeed"]+'\"', '\"'+decodePhysAddress(row["ifPhysAddress"])+'\"', '\"'+row["ifAdminStatus"]+'\"', '\"'+row["ifOperStatus"]+'\"', '\"'+row["ifLastChange"]+'\"', '\"'+i[0]+'\"')
            # print exe
            cursor.execute(exe)
    db.commit()


def drop(db):
    # delete all value in arpTable
    cursor = db.cursor()
    try:
        cursor.execute("TRUNCATE ifTable;")
        db.commit()
    except:
        db.rollback()

def show(db):
    # show all value in arpTable
    cursor = db.cursor()
    cursor.execute("SELECT portId, deviceId, ifIndex, ifPhysAddress, address FROM ifTable;")
    print "_______if_table___________"
    print "portId | deviceId | index |   ifPhysAddress   |      address      |"    

    for i in cursor.fetchall():
        print "%5d  | %8s | %5s | %17s | %17s |" % (i[0], i[1], i[2], i[3], i[4])
                
        

def updateDeviceId(db):
    cur = db.cursor()
    cur.execute("SELECT deviceId, IP FROM device;")
    
    rows = cur.fetchall()
    # print rows
    for row in rows:
        exe = "UPDATE ifTable SET deviceId = %d WHERE address = %s;" % (row[0],'\"'+row[1]+'\"')
        cur.execute(exe)

    db.commit()
    # conn.close()


# try:
#     db = MySQLdb.connect("localhost", "root", "toor", "zabbix")
#     print "connect to db is ok!"
        
# except:
#     print "error connect to db !"
#     exit()
# ipList = [("192.168.1.1", "BKCS"), ('192.168.10.1', "BKCS"),('192.168.10.2', "BKCS"),('192.168.10.3', "BKCS")] 
    
    
# #   #
# # for i in getFromIpList(ipList).items():
# #       print type(i), i[1]
# # print table
# # drop(db)
# show(db)
# updateToTable(ipList, db)