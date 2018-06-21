from easysnmp import snmp_get, snmp_set, snmp_walk
import easysnmp, json

def get(ip, community):
    # get arp table from an ip by SNMP
    data = snmp_walk("RFC1213-MIB::atPhysAddress", hostname=ip, community=community, version=2)
    # snmp walk to get data arp table from ip, return a list SNMP object
    listArp = {}    
    # the dict store data arp
    for i in data:
        listArp['.'.join(i.oid_index.split('.')[2:])]=(':'.join(['%0.2x' % ord(x) for x in i.value ]))
        # the index of SNMP object has 4 last number is IP address, and the value is MAC address in OCTES STRING
    
    return listArp
       
def getFromIpList(ipList):
    listArpItems = []
    for i in ipList:
        data = get(i[0], i[1])
        listArpItems += data.items()
    return dict(listArpItems)

def updateToTable(ipList,db):
    cursor = db.cursor()
    for i in getFromIpList(ipList).items():
        mac = '\"'+i[1]+'\"'
        ip = '\"'+i[0]+'\"'
        sql = "INSERT INTO arpTable (MAC, IP)  VALUES (%s, %s);" % (mac, ip)
        cursor.execute(sql)
    db.commit()

def insertToTable(ipList,db):
    cursor = db.cursor()
    for i in getFromIpList(ipList).items():
        mac = '\"'+i[1]+'\"'
        ip = '\"'+i[0]+'\"'
        sql = "INSERT INTO arpTable (MAC, IP)  VALUES (%s, %s);" % (mac, ip)
        cursor.execute(sql)
    db.commit()


def drop(db):
    # delete all value in arpTable
    cursor = db.cursor()
    try:
        cursor.execute("TRUNCATE arpTable;")
        db.commit()
    except:
        db.rollback()

def show(db):
    # show all value in arpTable
    cursor = db.cursor()
    cursor.execute("SELECT * FROM arpTable;")
    print "_______arp_table___________"
    for i in cursor.fetchall():
        print "%3s --- %3s" % (i[0],i[1])
