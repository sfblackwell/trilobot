-- phpMyAdmin SQL Dump
-- version 5.0.4deb2+deb11u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 10, 2023 at 10:29 PM
-- Server version: 10.5.15-MariaDB-0+deb11u1
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trilobot`
--
CREATE DATABASE IF NOT EXISTS `trilobot` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `trilobot`;

-- --------------------------------------------------------

--
-- Table structure for table `6Dof`
--

CREATE TABLE `6Dof` (
  `id` int(11) NOT NULL,
  `timeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `accelerX` float NOT NULL,
  `accelerY` float NOT NULL,
  `accelerZ` float NOT NULL,
  `magnetoX` float NOT NULL,
  `magnetoY` float NOT NULL,
  `magnetoZ` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `bme280`
--

CREATE TABLE `bme280` (
  `id` int(11) NOT NULL,
  `temperature` float NOT NULL DEFAULT -9999,
  `humidity` float NOT NULL DEFAULT -9999,
  `pressure` float NOT NULL DEFAULT -9999,
  `timeStamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `frontTOF`
--

CREATE TABLE `frontTOF` (
  `id` int(11) NOT NULL,
  `timeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `minCell` float NOT NULL,
  `min` float NOT NULL,
  `max` float NOT NULL,
  `avg` float NOT NULL,
  `p0` float NOT NULL,
  `p1` float NOT NULL,
  `p2` float NOT NULL,
  `p3` float NOT NULL,
  `p4` float NOT NULL,
  `p5` float NOT NULL,
  `p6` float NOT NULL,
  `p7` float NOT NULL,
  `p8` float NOT NULL,
  `p9` float NOT NULL,
  `p10` float NOT NULL,
  `p11` float NOT NULL,
  `p12` float NOT NULL,
  `p13` float NOT NULL,
  `p14` float NOT NULL,
  `p15` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `GPSdata`
--

CREATE TABLE `GPSdata` (
  `id` int(11) NOT NULL,
  `timeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `timestampGPS` datetime DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float NOT NULL,
  `altitude` float NOT NULL,
  `num_sats` int(11) NOT NULL,
  `gps_qual` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `parameters`
--

CREATE TABLE `parameters` (
  `id` int(11) NOT NULL,
  `timeStamp` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
  `collectData` varchar(50) NOT NULL DEFAULT '1',
  `showData` varchar(50) NOT NULL DEFAULT '1',
  `collectGPS` varchar(50) NOT NULL DEFAULT '1',
  `showGPS` varchar(50) NOT NULL DEFAULT '1',
  `collectTOF` varchar(50) NOT NULL DEFAULT '1',
  `collectGRD` varchar(50) NOT NULL,
  `showGRD` varchar(50) NOT NULL,
  `showTOF` varchar(50) NOT NULL DEFAULT '1',
  `collectULT` varchar(50) NOT NULL DEFAULT '1',
  `showULT` varchar(50) NOT NULL DEFAULT '1',
  `collectENV` varchar(50) NOT NULL DEFAULT '1',
  `showENV` varchar(50) NOT NULL DEFAULT '1',
  `collectFrequency` int(11) NOT NULL DEFAULT 60,
  `showFrequency` int(11) NOT NULL DEFAULT 120,
  `ScrollMessage` varchar(50) NOT NULL DEFAULT '',
  `gameController` varchar(50) NOT NULL,
  `collectDOF` varchar(20) NOT NULL DEFAULT 'Enabled',
  `showDOF` varchar(20) NOT NULL DEFAULT 'Enabled',
  `startupMessage` varchar(50) NOT NULL DEFAULT 'Startup',
  `shutdownMessage` varchar(50) NOT NULL DEFAULT 'Shutdown',
  `stopEnvCollection` varchar(20) NOT NULL,
  `motorStatic` varchar(20) NOT NULL,
  `motorButtonBig` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `RearUltrasound`
--

CREATE TABLE `RearUltrasound` (
  `id` int(11) NOT NULL,
  `timeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `distance` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `6Dof`
--
ALTER TABLE `6Dof`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bme280`
--
ALTER TABLE `bme280`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `frontTOF`
--
ALTER TABLE `frontTOF`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `GPSdata`
--
ALTER TABLE `GPSdata`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `parameters`
--
ALTER TABLE `parameters`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `RearUltrasound`
--
ALTER TABLE `RearUltrasound`
  ADD PRIMARY KEY (`id`),
  ADD KEY `timeStamp` (`timeStamp`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `6Dof`
--
ALTER TABLE `6Dof`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bme280`
--
ALTER TABLE `bme280`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `frontTOF`
--
ALTER TABLE `frontTOF`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `GPSdata`
--
ALTER TABLE `GPSdata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `parameters`
--
ALTER TABLE `parameters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `RearUltrasound`
--
ALTER TABLE `RearUltrasound`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
