import ConfigParser

config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section('MySQL')
config.set('MySQL', 'DBHost', 'localhost')
config.set('MySQL', 'DBName', 'zabbix')
config.set('MySQL', 'DBUser', 'root')
config.set('MySQL', 'DBPassword', 'toor')



# Writing our configuration file to 'example.cfg'
with open('SNMP.conf', 'w') as configfile:
    config.write(configfile)
