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
) ENGINE=InnoDB DEFAULT CHARSET=utf8

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8

