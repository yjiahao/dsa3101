CREATE DATABASE IF NOT EXISTS ocr;
USE ocr;

CREATE TABLE IF NOT EXISTS extraction(
    binCenterName VARCHAR(255) NOT NULL,
    extractedWeight INT NULL,
    manualWeight INT NULL,
    collectionTime VARCHAR(255) NOT NULL,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    selectedSession VARCHAR(255) NOT NULL,
    selectedReportingType VARCHAR(255) NOT NULL,
    PRIMARY KEY (collectionTime)
);

CREATE TABLE IF NOT EXISTS images
(
 collectionTime VARCHAR(255) NOT NULL,
 image VARCHAR(255) NULL,
 PRIMARY KEY (collectionTime)
);

CREATE TABLE IF NOT EXISTS logs
(
 log_time VARCHAR(55) NOT NULL,
 method VARCHAR(6),
 table_name VARCHAR(20) NOT NULL,
 log_message VARCHAR(255),
 log_values VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS bincenters(
   binCenterID INT NOT NULL,
   binCenterName VARCHAR(255) NOT NULL,
   binCenterLat FLOAT NOT NULL,
   binCenterLon FLOAT NOT NULL,
   PRIMARY KEY ( binCenterName )
);

CREATE TABLE IF NOT EXISTS evrekadb(
   RFID VARCHAR(255) NOT NULL,
   binCenterLat FLOAT NOT NULL,
   binCenterLon FLOAT NOT NULL,
   reportedWeight INT NOT NULL,
   collectionTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY ( collectionTime )
);


INSERT INTO bincenters (binCenterID, binCenterName, binCenterLat, binCenterLon) VALUES 
(0, 'NUS - Use for Reference Weight', 1.2966, 103.7764),
(1, 'UTown Residence', 1.3053867028982664, 103.77395411402797),
(2, 'Cinnamon College', 1.3068623859969037, 103.77356978330968),
(3, 'College of Alice & Peter Tan (CAPT)', 1.308133475737056, 103.7732636240817),
(4, 'Residential College 4', 1.3084262413493235, 103.77343958175372),
(5, 'Yale-NUS College', 1.3070708893592056, 103.77185893942554);







