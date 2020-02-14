-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: dbd
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.11-MariaDB-1:10.4.11+maria~bionic

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
-- Table structure for table `dbd_new_query`
--

DROP TABLE IF EXISTS `dbd_new_query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbd_new_query` (
  `DBD_COMPANY_ID` varchar(45) NOT NULL,
  `DBD_TYPECODE` varchar(45) DEFAULT NULL,
  `DBD_STATUS` text DEFAULT NULL,
  `DBD_LAST_RUN` datetime DEFAULT NULL,
  `DBD_IGNORE` tinyint(1) DEFAULT 0,
  `DBD_CHANGE` int(11) DEFAULT NULL,
  `C_DBD_NAME_TH` text DEFAULT NULL,
  `C_DBD_STATUS` text DEFAULT NULL,
  `C_DBD_OBJECTIVE` text DEFAULT NULL,
  `C_DBD_BUSINESS_TYPE` text DEFAULT NULL,
  `C_DBD_ADDRESS` text DEFAULT NULL,
  PRIMARY KEY (`DBD_COMPANY_ID`),
  UNIQUE KEY `DBD_COMPANY_ID_UNIQUE` (`DBD_COMPANY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbd_query`
--

DROP TABLE IF EXISTS `dbd_query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbd_query` (
  `DBD_COMPANY_ID` varchar(45) NOT NULL,
  `DBD_TYPECODE` varchar(45) DEFAULT NULL,
  `DBD_STATUS` text DEFAULT NULL,
  `DBD_LAST_RUN` datetime DEFAULT NULL,
  `DBD_IGNORE` tinyint(1) DEFAULT 0,
  `DBD_CHANGE` int(11) DEFAULT NULL,
  `C_DBD_NAME_TH` text DEFAULT NULL,
  `C_DBD_STATUS` text DEFAULT NULL,
  `C_DBD_OBJECTIVE` text DEFAULT NULL,
  `C_DBD_BUSINESS_TYPE` text DEFAULT NULL,
  `C_DBD_ADDRESS` text DEFAULT NULL,
  PRIMARY KEY (`DBD_COMPANY_ID`),
  UNIQUE KEY `DBD_COMPANY_ID_UNIQUE` (`DBD_COMPANY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbdcompany`
--

DROP TABLE IF EXISTS `dbdcompany`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbdcompany` (
  `DBD_ID` varchar(45) NOT NULL,
  `DBD_TYPE` varchar(45) DEFAULT NULL,
  `DBD_NAME_TH` varchar(255) DEFAULT NULL,
  `DBD_NAME_EN` varchar(255) DEFAULT NULL,
  `DBD_REGISTRATION_DATE` date DEFAULT NULL,
  `DBD_STATUS` varchar(100) DEFAULT NULL,
  `DBD_REGISTRATION_MONEY` bigint(20) DEFAULT NULL,
  `DBD_ADDRESS` text DEFAULT NULL,
  `DBD_OBJECTIVE` text DEFAULT NULL,
  `DBD_STREET` text DEFAULT NULL,
  `DBD_SUBDISTRICT` text DEFAULT NULL,
  `DBD_DISTRICT` text DEFAULT NULL,
  `DBD_PROVINCE` text DEFAULT NULL,
  `DBD_ZIPCODE` varchar(5) DEFAULT NULL,
  `DBD_BUSINESS_TYPE_CODE` text DEFAULT NULL,
  `DBD_BUSINESS_TYPE` text DEFAULT NULL,
  `DBD_DIRECTORS` text DEFAULT NULL,
  PRIMARY KEY (`DBD_ID`),
  UNIQUE KEY `dbd_id_UNIQUE` (`DBD_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `m_dbdcompany`
--

DROP TABLE IF EXISTS `m_dbdcompany`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `m_dbdcompany` (
  `DBD_ID` varchar(45) NOT NULL,
  `DBD_TYPE` varchar(45) DEFAULT NULL,
  `DBD_NAME_TH` varchar(255) DEFAULT NULL,
  `DBD_NAME_EN` varchar(255) DEFAULT NULL,
  `DBD_REGISTRATION_DATE` date DEFAULT NULL,
  `DBD_STATUS` varchar(100) DEFAULT NULL,
  `DBD_REGISTRATION_MONEY` bigint(20) DEFAULT NULL,
  `DBD_ADDRESS` text DEFAULT NULL,
  `DBD_OBJECTIVE` text DEFAULT NULL,
  `DBD_STREET` text DEFAULT NULL,
  `DBD_SUBDISTRICT` text DEFAULT NULL,
  `DBD_DISTRICT` text DEFAULT NULL,
  `DBD_PROVINCE` text DEFAULT NULL,
  `DBD_ZIPCODE` varchar(5) DEFAULT NULL,
  `DBD_BUSINESS_TYPE_CODE` text DEFAULT NULL,
  `DBD_BUSINESS_TYPE` text DEFAULT NULL,
  `DBD_DIRECTORS` text DEFAULT NULL,
  PRIMARY KEY (`DBD_ID`),
  UNIQUE KEY `dbd_id_UNIQUE` (`DBD_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mdbd`
--

DROP TABLE IF EXISTS `mdbd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mdbd` (
  `id` int(10) NOT NULL,
  `regisid` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `regisid` (`regisid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zipcodes`
--

DROP TABLE IF EXISTS `zipcodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zipcodes` (
  `PROVINCE` varchar(255) DEFAULT NULL,
  `DISTRICT` varchar(255) DEFAULT NULL,
  `SUBDISTRICT` varchar(255) DEFAULT NULL,
  `ZIP` varchar(5) DEFAULT NULL,
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID`),
  KEY `PROVINCE` (`PROVINCE`),
  KEY `DISTRICT` (`DISTRICT`),
  KEY `SUBDISTRICT` (`SUBDISTRICT`)
) ENGINE=InnoDB AUTO_INCREMENT=7830 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-13  4:37:51
