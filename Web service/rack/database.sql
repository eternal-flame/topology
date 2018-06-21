-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: zabbix2
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `arpTable`
--

DROP TABLE IF EXISTS `arpTable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `arpTable` (
  `MAC` text NOT NULL,
  `IP` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arpTable`
--

LOCK TABLES `arpTable` WRITE;
/*!40000 ALTER TABLE `arpTable` DISABLE KEYS */;
INSERT INTO `arpTable` VALUES ('a0:2b:b8:40:eb:7d','192.168.10.82'),('6c:88:14:a4:a7:d4','192.168.10.63'),('ac:b5:7d:30:94:fa','192.168.10.29'),('10:a5:d0:1d:ce:dc','192.168.10.28'),('68:17:29:53:f3:54','192.168.10.26'),('64:5a:04:ac:ea:06','192.168.10.25'),('88:b1:11:8d:4a:b4','192.168.10.24'),('0c:f5:a4:ae:12:42','192.168.10.1'),('2c:3e:cf:be:e1:c1','192.168.10.2'),('0c:f5:a4:e3:c1:41','192.168.10.3'),('20:d3:90:21:23:a2','192.168.0.139'),('68:17:29:53:f3:54','192.168.10.43'),('70:db:98:1c:f9:e0','192.168.0.2'),('54:13:79:5b:c6:07','192.168.10.42'),('70:db:98:1c:f9:e1','192.168.1.1'),('68:17:29:53:f3:54','192.168.10.73'),('0c:f5:a4:ae:12:43','192.168.20.1'),('0c:f5:a4:e3:c1:42','192.168.20.3'),('2c:3e:cf:be:e1:c2','192.168.20.2'),('b0:83:fe:59:14:ca','192.168.10.30'),('70:1a:04:c2:d4:22','192.168.10.31'),('0c:f5:a4:ae:12:41','192.168.1.10'),('c0:4a:00:a4:8b:c2','192.168.0.1');
/*!40000 ALTER TABLE `arpTable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device` (
  `deviceId` int(11) NOT NULL AUTO_INCREMENT,
  `IP` text,
  `sysDescr` text,
  `sysUpTime` text,
  `sysContact` text,
  `sysName` text,
  `type` text,
  `sysLocation` text,
  `sysServices` text,
  `note` text,
  `community` text,
  `fixed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`deviceId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'192.168.1.1','Cisco IOS Software, C1900 Software (C1900-UNIVERSALK9-M), Version 15.4(3)M3, RELEASE SOFTWARE (fc2)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2015 by Cisco Systems, Inc.\r\nCompiled Fri 05-Jun-15 12:31 by prod_rel_team','225311924','BKCS','Router1','Router','BKCS P405','78','Null','BKCS',0),(2,'192.168.10.1','Cisco IOS Software, C3560C Software (C3560c405ex-UNIVERSALK9-M), Version 15.0(2)SE5, RELEASE SOFTWARE (fc1)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2013 by Cisco Systems, Inc.\r\nCompiled Fri 25-Oct-13 14:53 by prod_rel_team','43993656','BKCS','SwitchC.bkcs','Switch','P405 BKCS','6','Null','BKCS',0),(3,'192.168.10.2','Cisco IOS Software, C2960C Software (C2960c405-UNIVERSALK9-M), Version 12.2(55)EX3, RELEASE SOFTWARE (fc2)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\r\nCompiled Wed 10-Aug-11 06:40 by prod_rel_team','225312571','BKCS','SwitchD.bkcs','Switch','BKCS P405','6','Null','BKCS',0),(4,'192.168.10.3','Cisco IOS Software, C2960C Software (C2960c405-UNIVERSALK9-M), Version 15.0(2)SE5, RELEASE SOFTWARE (fc1)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2013 by Cisco Systems, Inc.\r\nCompiled Fri 25-Oct-13 14:35 by prod_rel_team','305847589','BKCS','SwitchA1.bkcs','Switch','P405 BKCS','6','Null','BKCS',0);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deviceAdmin`
--

DROP TABLE IF EXISTS `deviceAdmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deviceAdmin` (
  `deviceId` int(11) NOT NULL AUTO_INCREMENT,
  `IP` text,
  `sysDescr` text,
  `sysUpTime` text,
  `sysContact` text,
  `sysName` text,
  `type` text,
  `sysLocation` text,
  `sysServices` text,
  `note` text,
  `community` text,
  `fixed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`deviceId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceAdmin`
--

LOCK TABLES `deviceAdmin` WRITE;
/*!40000 ALTER TABLE `deviceAdmin` DISABLE KEYS */;
INSERT INTO `deviceAdmin` VALUES (1,'192.168.1.1','Cisco IOS Software, C1900 Software (C1900-UNIVERSALK9-M), Version 15.4(3)M3, RELEASE SOFTWARE (fc2)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2015 by Cisco Systems, Inc.\r\nCompiled Fri 05-Jun-15 12:31 by prod_rel_team','128493508','BKCS','Router1',NULL,'BKCS P405','78','Null','BKCS',NULL),(2,'192.168.10.1','Cisco IOS Software, C3560C Software (C3560c405ex-UNIVERSALK9-M), Version 15.0(2)SE5, RELEASE SOFTWARE (fc1)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2013 by Cisco Systems, Inc.\nCompiled Fri 25-Oct-13 14:53 by prod_rel_team','209026797','BKCS','SwitchC',NULL,'P405 BKCS','6','Null','BKCS',NULL),(3,'192.168.10.2','Cisco IOS Software, C2960C Software (C2960c405-UNIVERSALK9-M), Version 12.2(55)EX3, RELEASE SOFTWARE (fc2)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\r\nCompiled Wed 10-Aug-11 06:40 by prod_rel_team','128494607','BKCS','SwitchD',NULL,'BKCS P405','6','Null','BKCS',NULL),(4,'192.168.10.3','Cisco IOS Software, C2960C Software (C2960c405-UNIVERSALK9-M), Version 15.0(2)SE5, RELEASE SOFTWARE (fc1)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2013 by Cisco Systems, Inc.\r\nCompiled Fri 25-Oct-13 14:35 by prod_rel_team','209029802','BKCS','SwitchA1',NULL,'P405 BKCS','6','Null','BKCS',NULL);
/*!40000 ALTER TABLE `deviceAdmin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deviceIp`
--

DROP TABLE IF EXISTS `deviceIp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deviceIp` (
  `deviceId` int(11) NOT NULL,
  `ip` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceIp`
--

LOCK TABLES `deviceIp` WRITE;
/*!40000 ALTER TABLE `deviceIp` DISABLE KEYS */;
INSERT INTO `deviceIp` VALUES (1,'192.168.0.2'),(1,'192.168.1.1'),(2,'192.168.1.10'),(2,'192.168.10.1'),(2,'192.168.20.1'),(3,'192.168.10.2'),(3,'192.168.20.2'),(4,'192.168.10.3'),(4,'192.168.20.3');
/*!40000 ALTER TABLE `deviceIp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ifTable`
--

DROP TABLE IF EXISTS `ifTable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ifTable` (
  `ifIndex` int(11) DEFAULT NULL,
  `ifDescr` text,
  `ifType` text,
  `ifMtu` int(11) DEFAULT NULL,
  `ifSpeed` text,
  `ifPhysAddress` text,
  `ifAdminStatus` text,
  `ifOperStatus` text,
  `ifLastChange` text,
  `note` text,
  `address` text,
  `portId` int(11) NOT NULL AUTO_INCREMENT,
  `deviceId` int(11) DEFAULT NULL,
  PRIMARY KEY (`portId`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ifTable`
--

LOCK TABLES `ifTable` WRITE;
/*!40000 ALTER TABLE `ifTable` DISABLE KEYS */;
INSERT INTO `ifTable` VALUES (1,'Embedded-Service-Engine0/0','6',1500,'10000000','00:00:00:00:00:00','2','2','3408',NULL,'192.168.1.1',1,1),(3,'GigabitEthernet0/1','6',1500,'1000000000','70:db:98:1c:f9:e1','1','1','216146452',NULL,'192.168.1.1',2,1),(2,'GigabitEthernet0/0','6',1500,'1000000000','70:db:98:1c:f9:e0','1','1','2452',NULL,'192.168.1.1',3,1),(5,'NVI0','1',1514,'56000','','1','1','3201',NULL,'192.168.1.1',4,1),(4,'Null0','1',1500,'4294967295','','1','1','0',NULL,'192.168.1.1',5,1),(10,'Vlan10','53',1500,'1000000000','0c:f5:a4:ae:12:42','1','1','11131',NULL,'192.168.10.1',6,2),(10110,'GigabitEthernet0/10','6',1500,'10000000','0c:f5:a4:ae:12:0a','1','2','7582',NULL,'192.168.10.1',7,2),(20,'Vlan20','53',1500,'1000000000','0c:f5:a4:ae:12:43','1','1','11131',NULL,'192.168.10.1',8,2),(1,'Vlan1','53',1500,'1000000000','0c:f5:a4:ae:12:40','2','2','7553',NULL,'192.168.10.1',9,2),(10501,'Null0','1',1500,'4294967295','','1','1','0',NULL,'192.168.10.1',10,2),(10109,'GigabitEthernet0/9','6',1500,'10000000','0c:f5:a4:ae:12:09','1','2','7582',NULL,'192.168.10.1',11,2),(10108,'GigabitEthernet0/8','6',1500,'10000000','0c:f5:a4:ae:12:08','1','2','7582',NULL,'192.168.10.1',12,2),(10105,'GigabitEthernet0/5','6',1500,'10000000','0c:f5:a4:ae:12:05','1','2','7582',NULL,'192.168.10.1',13,2),(10104,'GigabitEthernet0/4','6',1500,'10000000','0c:f5:a4:ae:12:04','1','2','7582',NULL,'192.168.10.1',14,2),(10107,'GigabitEthernet0/7','6',1500,'10000000','0c:f5:a4:ae:12:07','1','2','7582',NULL,'192.168.10.1',15,2),(10106,'GigabitEthernet0/6','6',1500,'10000000','0c:f5:a4:ae:12:06','1','2','7582',NULL,'192.168.10.1',16,2),(10101,'GigabitEthernet0/1','6',1500,'1000000000','0c:f5:a4:ae:12:41','1','1','34828177',NULL,'192.168.10.1',17,2),(10103,'GigabitEthernet0/3','6',1500,'10000000','0c:f5:a4:ae:12:03','1','2','7582',NULL,'192.168.10.1',18,2),(10102,'GigabitEthernet0/2','6',1500,'1000000000','0c:f5:a4:ae:12:02','1','1','8230',NULL,'192.168.10.1',19,2),(10004,'FastEthernet0/4','6',1500,'10000000','2c:3e:cf:be:e1:84','1','2','5866',NULL,'192.168.10.2',20,3),(10,'Vlan10','53',1500,'1000000000','2c:3e:cf:be:e1:c1','1','1','9351',NULL,'192.168.10.2',21,3),(10006,'FastEthernet0/6','6',1500,'10000000','2c:3e:cf:be:e1:86','1','2','5866',NULL,'192.168.10.2',22,3),(10007,'FastEthernet0/7','6',1500,'10000000','2c:3e:cf:be:e1:87','1','2','5866',NULL,'192.168.10.2',23,3),(20,'Vlan20','53',1500,'1000000000','2c:3e:cf:be:e1:c2','1','1','9351',NULL,'192.168.10.2',24,3),(10001,'FastEthernet0/1','6',1500,'100000000','2c:3e:cf:be:e1:81','1','1','6450',NULL,'192.168.10.2',25,3),(10002,'FastEthernet0/2','6',1500,'10000000','2c:3e:cf:be:e1:82','1','2','5866',NULL,'192.168.10.2',26,3),(10003,'FastEthernet0/3','6',1500,'10000000','2c:3e:cf:be:e1:83','1','2','5866',NULL,'192.168.10.2',27,3),(10008,'FastEthernet0/8','6',1500,'10000000','2c:3e:cf:be:e1:88','1','2','5866',NULL,'192.168.10.2',28,3),(1,'Vlan1','53',1500,'1000000000','2c:3e:cf:be:e1:c0','1','1','9351',NULL,'192.168.10.2',29,3),(10501,'Null0','1',1500,'4294967295','','1','1','0',NULL,'192.168.10.2',30,3),(10101,'GigabitEthernet0/1','6',1500,'1000000000','2c:3e:cf:be:e1:89','1','1','181326578',NULL,'192.168.10.2',31,3),(10005,'FastEthernet0/5','6',1500,'10000000','2c:3e:cf:be:e1:85','1','2','5866',NULL,'192.168.10.2',32,3),(10102,'GigabitEthernet0/2','6',1500,'10000000','2c:3e:cf:be:e1:8a','1','2','5866',NULL,'192.168.10.2',33,3),(10004,'FastEthernet0/4','6',1500,'100000000','0c:f5:a4:e3:c1:04','1','1','7043',NULL,'192.168.10.3',34,4),(10,'Vlan10','53',1500,'1000000000','0c:f5:a4:e3:c1:41','1','1','9906',NULL,'192.168.10.3',35,4),(10006,'FastEthernet0/6','6',1500,'10000000','0c:f5:a4:e3:c1:06','1','2','6742',NULL,'192.168.10.3',36,4),(10007,'FastEthernet0/7','6',1500,'100000000','0c:f5:a4:e3:c1:07','1','2','243155466',NULL,'192.168.10.3',37,4),(20,'Vlan20','53',1500,'1000000000','0c:f5:a4:e3:c1:42','1','1','80544801',NULL,'192.168.10.3',38,4),(10001,'FastEthernet0/1','6',1500,'100000000','0c:f5:a4:e3:c1:01','1','1','80541900',NULL,'192.168.10.3',39,4),(10002,'FastEthernet0/2','6',1500,'10000000','0c:f5:a4:e3:c1:02','1','2','6741',NULL,'192.168.10.3',40,4),(10003,'FastEthernet0/3','6',1500,'100000000','0c:f5:a4:e3:c1:03','1','1','235762791',NULL,'192.168.10.3',41,4),(10008,'FastEthernet0/8','6',1500,'100000000','0c:f5:a4:e3:c1:08','1','2','89450165',NULL,'192.168.10.3',42,4),(1,'Vlan1','53',1500,'1000000000','0c:f5:a4:e3:c1:40','2','2','6705',NULL,'192.168.10.3',43,4),(10501,'Null0','1',1500,'4294967295','','1','1','0',NULL,'192.168.10.3',44,4),(10101,'GigabitEthernet0/1','6',1500,'100000000','0c:f5:a4:e3:c1:09','1','2','89466945',NULL,'192.168.10.3',45,4),(10005,'FastEthernet0/5','6',1500,'100000000','0c:f5:a4:e3:c1:05','1','1','7043',NULL,'192.168.10.3',46,4),(10102,'GigabitEthernet0/2','6',1500,'10000000','0c:f5:a4:e3:c1:0a','1','2','6742',NULL,'192.168.10.3',47,4);
/*!40000 ALTER TABLE `ifTable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inputIp`
--

DROP TABLE IF EXISTS `inputIp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inputIp` (
  `ip` varchar(15) NOT NULL,
  `community` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inputIp`
--

LOCK TABLES `inputIp` WRITE;
/*!40000 ALTER TABLE `inputIp` DISABLE KEYS */;
/*!40000 ALTER TABLE `inputIp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `link`
--

DROP TABLE IF EXISTS `link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `link` (
  `connectId` int(11) NOT NULL AUTO_INCREMENT,
  `portId1` int(11) NOT NULL,
  `portId2` int(11) NOT NULL,
  PRIMARY KEY (`connectId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `link`
--

LOCK TABLES `link` WRITE;
/*!40000 ALTER TABLE `link` DISABLE KEYS */;
INSERT INTO `link` VALUES (1,23,99),(2,5,57);
/*!40000 ALTER TABLE `link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topoInfo`
--

DROP TABLE IF EXISTS `topoInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topoInfo` (
  `topoId` int(11) NOT NULL,
  `topoName` varchar(50) NOT NULL,
  `rackId` int(11) NOT NULL,
  `rackName` varchar(50) NOT NULL,
  `rackIp` varchar(50) NOT NULL,
  `deviceId` int(11) NOT NULL,
  `deviceIp` varchar(50) NOT NULL,
  `deviceComString` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topoInfo`
--

LOCK TABLES `topoInfo` WRITE;
/*!40000 ALTER TABLE `topoInfo` DISABLE KEYS */;
INSERT INTO `topoInfo` VALUES (1,'New Topology',1,'New rack controller','192.168.10.10',1,'192.168.10.1','BKCS'),(2,'New Topology',1,'New rack controller','1',1,'3','3'),(2,'New Topology',1,'New rack controller','1',2,'2','2'),(2,'New Topology',2,'New rack controller','2',3,'5','5'),(2,'New Topology',2,'New rack controller','2',4,'4','4'),(2,'New Topology',2,'New rack controller','2',5,'6','6');
/*!40000 ALTER TABLE `topoInfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology`
--

DROP TABLE IF EXISTS `topology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology` (
  `connectId` int(11) NOT NULL AUTO_INCREMENT,
  `portId1` int(11) DEFAULT NULL,
  `sysName1` text,
  `IP1` text,
  `MAC1` text,
  `deviceId1` int(11) DEFAULT NULL,
  `portId2` int(11) DEFAULT NULL,
  `sysName2` text,
  `IP2` text,
  `MAC2` text,
  `deviceId2` int(11) DEFAULT NULL,
  PRIMARY KEY (`connectId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology`
--

LOCK TABLES `topology` WRITE;
/*!40000 ALTER TABLE `topology` DISABLE KEYS */;
INSERT INTO `topology` VALUES (1,2,NULL,'192.168.1.1','70:db:98:1c:f9:e1',1,17,NULL,'192.168.1.10','0c:f5:a4:ae:12:41',2),(2,19,NULL,'192.168.10.1','0c:f5:a4:ae:12:02',2,31,NULL,'192.168.10.2','2c:3e:cf:be:e1:89',3),(3,25,NULL,'192.168.10.2','2c:3e:cf:be:e1:81',3,39,NULL,'192.168.10.3','0c:f5:a4:e3:c1:01',4),(4,41,NULL,'192.168.10.3','0c:f5:a4:e3:c1:03',4,NULL,NULL,NULL,'2c:3e:cf:6b:05:81',NULL);
/*!40000 ALTER TABLE `topology` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-13 15:17:52
