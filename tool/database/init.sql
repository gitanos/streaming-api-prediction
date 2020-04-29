CREATE DATABASE IF NOT EXISTS `tooldb`;
USE `tooldb`;

DROP TABLE IF EXISTS `patients`;
 
CREATE TABLE `patients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pat_id` int(11) DEFAULT 0,
  `age` FLOAT(3, 1) DEFAULT 0.0,
  `date_admission` date DEFAULT NULL,
  `date_discharge` date DEFAULT NULL,
  `day` date DEFAULT NULL,
  `hour` int(2) DEFAULT 0,
  `parameter` ENUM('blood_pressure', 'respiration_rate', 'temperature') NOT NULL,
  `value` FLOAT DEFAULT 0.0,
   PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;