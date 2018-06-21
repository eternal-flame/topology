import sys

import MySQLdb

HOST="localhost"
USER="zabbix"
PASS="zabbix"
DB="rack"

try:
	connect=MySQLdb.connect(host=HOST,
			   user=USER,
			   passwd=PASS,
			   db=DB)
except:
	print "Can not connect to database!"
	sys.exit()
