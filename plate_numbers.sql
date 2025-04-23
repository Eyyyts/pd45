-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 23, 2025 at 06:49 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `plate_recognition`
--

-- --------------------------------------------------------

--
-- Table structure for table `plate_numbers`
--

CREATE TABLE `plate_numbers` (
  `id` int(10) UNSIGNED NOT NULL,
  `plate_number` varchar(255) NOT NULL,
  `vehicle_image` varchar(191) DEFAULT NULL,
  `scanned_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `date_time_scanned` timestamp NOT NULL DEFAULT current_timestamp(),
  `detected` tinyint(1) NOT NULL DEFAULT 0,
  `car_color` varchar(50) DEFAULT NULL,
  `location` varchar(100) NOT NULL,
  `vehicle_type` varchar(50) NOT NULL,
  `face_image_path` varchar(255) NOT NULL,
  `face_name` varchar(255) NOT NULL,
  `is_complete_record` tinyint(1) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `plate_numbers`
--

INSERT INTO `plate_numbers` (`id`, `plate_number`, `vehicle_image`, `scanned_at`, `created_at`, `updated_at`, `date_time_scanned`, `detected`, `car_color`, `location`, `vehicle_type`, `face_image_path`, `face_name`, `is_complete_record`, `status`) VALUES
(1, 'DAM1579', NULL, '2025-04-04 06:16:24', NULL, NULL, '2025-04-04 06:16:24', 0, 'Unknown', '', '', '', '', 0, 0),
(2, 'NCP3396', NULL, '2025-04-04 06:16:28', NULL, NULL, '2025-04-04 06:16:28', 0, 'Unknown', '', '', '', '', 0, 0),
(3, 'HLP888', NULL, '2025-04-04 06:16:39', NULL, NULL, '2025-04-04 06:16:39', 0, 'Unknown', '', '', '', '', 0, 0),
(4, 'WQ5066', NULL, '2025-04-04 06:17:00', NULL, NULL, '2025-04-04 06:17:00', 0, 'Unknown', '', '', '', '', 0, 0),
(5, 'HLP8881', NULL, '2025-04-04 07:41:00', NULL, NULL, '2025-04-04 07:41:00', 0, 'Unknown', '', '', '', '', 0, 0),
(6, 'DAM1579', NULL, '2025-04-04 07:41:05', NULL, NULL, '2025-04-04 07:41:05', 0, 'Unknown', '', '', '', '', 0, 0),
(7, 'NCP3396', NULL, '2025-04-04 07:41:37', NULL, NULL, '2025-04-04 07:41:37', 0, 'Unknown', '', '', '', '', 0, 0),
(8, '0JO', NULL, '2025-04-04 07:42:06', NULL, NULL, '2025-04-04 07:42:06', 0, 'Unknown', '', '', '', '', 0, 0),
(9, '0O', NULL, '2025-04-04 07:42:12', NULL, NULL, '2025-04-04 07:42:12', 0, 'Unknown', '', '', '', '', 0, 0),
(10, 'WQ5066', NULL, '2025-04-04 07:42:13', NULL, NULL, '2025-04-04 07:42:13', 0, 'Unknown', '', '', '', '', 0, 0),
(11, '447XG', NULL, '2025-04-04 07:42:36', NULL, NULL, '2025-04-04 07:42:36', 0, 'Unknown', '', '', '', '', 0, 0),
(12, '447XGI', NULL, '2025-04-04 07:42:38', NULL, NULL, '2025-04-04 07:42:38', 0, 'Unknown', '', '', '', '', 0, 0),
(13, 'E06', NULL, '2025-04-04 07:42:46', NULL, NULL, '2025-04-04 07:42:46', 0, 'Unknown', '', '', '', '', 0, 0),
(14, 'NBC1234', NULL, '2025-04-04 07:43:41', NULL, NULL, '2025-04-04 07:43:41', 0, 'Unknown', '', '', '', '', 0, 0),
(15, '841TCP', NULL, '2025-04-04 07:43:41', NULL, NULL, '2025-04-04 07:43:41', 0, 'Unknown', '', '', '', '', 0, 0),
(16, 'NI3345', NULL, '2025-04-07 01:23:53', NULL, NULL, '2025-04-07 01:23:53', 0, 'Unknown', 'Back Parking', '', '', '', 0, 0),
(17, '3ONA', NULL, '2025-04-07 01:24:27', NULL, NULL, '2025-04-07 01:24:27', 0, 'Unknown', 'Main Entrance', '', '', '', 0, 0),
(18, '340QNX', NULL, '2025-04-07 01:24:28', NULL, NULL, '2025-04-07 01:24:28', 0, 'Unknown', 'Main Entrance', '', '', '', 0, 0),
(19, 'NBC1234', NULL, '2025-04-07 03:35:24', NULL, NULL, '0000-00-00 00:00:00', 0, 'Unknown', 'Main Entrance', '', '', '', 0, 0),
(20, 'NBC1234', NULL, '2025-04-07 03:37:37', NULL, NULL, '0000-00-00 00:00:00', 0, 'Unknown', 'Back Parking', '', '', '', 0, 0),
(21, 'DBA4658', NULL, '2025-04-07 05:17:43', NULL, NULL, '2025-04-07 05:17:43', 0, 'Unknown', 'Main Entrance', '', '', '', 0, 0),
(22, 'NBC1234', NULL, '2025-04-07 05:19:11', NULL, NULL, '2025-04-07 05:19:11', 0, 'Unknown', 'Back Parking', '', '', '', 0, 0),
(23, 'NBC1234', NULL, '2025-04-07 06:31:48', NULL, NULL, '2025-04-07 06:31:48', 0, 'Unknown', 'Main Entrance', 'Sedan', '', '', 0, 0),
(24, 'ABY8512', NULL, '2025-04-07 06:43:45', NULL, NULL, '2025-04-07 06:43:45', 0, 'Unknown', 'Main Entrance', 'Sedan', 'faces/ABY8512_20250407144345.jpg', '', 0, 0),
(25, 'DBA4658', NULL, '2025-04-07 06:45:26', NULL, NULL, '2025-04-07 06:45:26', 0, 'Unknown', 'Back Parking', 'Sedan', '', '', 0, 0),
(26, 'NBC1234', NULL, '2025-04-07 07:40:24', NULL, NULL, '2025-04-07 07:40:24', 0, 'Unknown', 'Back Parking', 'Sedan', 'faces/NBC1234_20250407154024.jpg', '', 0, 0),
(27, 'RPC7777', NULL, '2025-04-07 07:40:42', NULL, NULL, '2025-04-07 07:40:42', 0, 'Unknown', 'Main Entrance', 'Sedan', '', '', 0, 0),
(28, 'CAX3260', NULL, '2025-04-07 07:42:57', NULL, NULL, '2025-04-07 07:42:57', 0, 'Unknown', 'Back Parking', 'Sedan', 'faces/CAX3260_20250407154257.jpg', '', 0, 0),
(29, 'CAX3266', NULL, '2025-04-07 07:43:03', NULL, NULL, '2025-04-07 07:43:03', 0, 'Unknown', 'Back Parking', 'Sedan', 'faces/CAX3266_20250407154303.jpg', '', 0, 0),
(30, 'CAX3200', NULL, '2025-04-07 07:43:19', NULL, NULL, '2025-04-07 07:43:19', 0, 'Unknown', 'Main Entrance', 'Sedan', '', '', 0, 0),
(31, 'CAX3200', NULL, '2025-04-07 15:10:39', NULL, NULL, '2025-04-07 15:10:39', 0, 'Unknown', 'Main Entrance', 'Sedan', 'faces/CAX3200_20250407231039.jpg', '', 0, 0),
(32, 'NXX8870', NULL, '2025-04-07 15:10:55', NULL, NULL, '2025-04-07 15:10:55', 0, 'Unknown', 'Back Parking', 'Sedan', '', '', 0, 0),
(33, 'NGP3944', NULL, '2025-04-07 15:11:49', NULL, NULL, '2025-04-07 15:11:49', 0, 'Unknown', 'Back Parking', 'Sedan', '', '', 0, 0),
(34, 'DBA4658', NULL, '2025-04-07 15:12:04', NULL, NULL, '2025-04-07 15:12:04', 0, 'Unknown', 'Main Entrance', 'Sedan', 'faces/DBA4658_20250407231204.jpg', '', 0, 0),
(35, 'CAX3200', NULL, '2025-04-07 15:22:11', NULL, NULL, '2025-04-07 15:22:11', 0, 'blue', 'Main Entrance', 'Sedan', 'faces/CAX3200_20250407232211.jpg', '', 0, 0),
(36, 'CAX3260', NULL, '2025-04-07 15:22:12', NULL, NULL, '2025-04-07 15:22:12', 0, 'blue', 'Main Entrance', 'Sedan', 'faces/CAX3260_20250407232212.jpg', '', 0, 0),
(37, 'NGP3944', NULL, '2025-04-07 15:23:31', NULL, NULL, '2025-04-07 15:23:31', 0, 'blue', 'Back Parking', 'Sedan', 'faces/NGP3944_20250407232331.jpg', '', 0, 0),
(38, 'RPC7777', NULL, '2025-04-07 15:23:40', NULL, NULL, '2025-04-07 15:23:40', 0, 'blue', 'Back Parking', 'Sedan', '', '', 0, 0),
(39, 'CAU9802', NULL, '2025-04-10 02:01:29', NULL, NULL, '2025-04-10 02:01:29', 0, 'white', 'Main Entrance', 'Sedan', 'faces/CAU9802_20250410100129.jpg', '', 0, 0),
(40, 'CAU9802', NULL, '2025-04-10 05:56:27', NULL, NULL, '2025-04-10 05:56:27', 0, 'white', 'Main Entrance', 'Sedan', '', '', 0, 0),
(41, 'NBC1234', NULL, '2025-04-10 05:57:13', NULL, NULL, '2025-04-10 05:57:13', 0, 'black', 'Main Entrance', 'Sedan', '', '', 0, 0),
(42, 'MBC1230', NULL, '2025-04-10 06:28:21', NULL, NULL, '2025-04-10 06:28:21', 0, 'black', 'Main Entrance', 'Sedan', '', '', 0, 0),
(43, 'NBC1234', NULL, '2025-04-10 06:28:24', NULL, NULL, '2025-04-10 06:28:24', 0, 'white', 'Main Entrance', 'Sedan', '', '', 0, 0),
(44, 'NBC1234', NULL, '2025-04-10 07:11:50', NULL, NULL, '2025-04-10 07:11:50', 0, 'white', 'Main Entrance', 'Sedan', '', '', 0, 0),
(45, 'DBA4658', NULL, '2025-04-10 07:25:57', NULL, NULL, '2025-04-10 07:25:57', 0, 'black', 'Main Entrance', 'Sedan', '', '', 0, 0),
(46, 'RPC7777', NULL, '2025-04-10 16:51:32', NULL, NULL, '2025-04-10 16:51:32', 0, 'blue', 'Back Parking', 'Sedan', '', '', 0, 0),
(47, 'NGP3944', NULL, '2025-04-10 16:52:03', NULL, NULL, '2025-04-10 16:52:03', 0, 'blue', 'Back Parking', 'Sedan', 'faces/NGP3944_20250411005203.jpg', '', 0, 0),
(48, 'ABY8512', NULL, '2025-04-10 16:52:16', NULL, NULL, '2025-04-10 16:52:16', 0, 'blue', 'Main Entrance', 'Sedan', '', '', 0, 0),
(49, 'ABY8512', NULL, '2025-04-10 16:58:27', NULL, NULL, '2025-04-10 16:58:27', 0, 'blue', 'Back Parking', 'Unknown', '', '', 0, 0),
(50, 'NGP3944', NULL, '2025-04-10 16:58:35', NULL, NULL, '2025-04-10 16:58:35', 0, 'blue', 'Back Parking', 'Unknown', '', '', 0, 0),
(51, 'RPC7777', NULL, '2025-04-10 16:58:42', NULL, NULL, '2025-04-10 16:58:42', 0, 'blue', 'Back Parking', 'Unknown', '', '', 0, 0),
(52, 'CAX3200', NULL, '2025-04-10 16:59:24', NULL, NULL, '2025-04-10 16:59:24', 0, 'blue', 'Back Parking', 'Unknown', '', '', 0, 0),
(53, 'DBA4658', NULL, '2025-04-10 16:59:31', NULL, NULL, '2025-04-10 16:59:31', 0, 'blue', 'Back Parking', 'Unknown', '', '', 0, 0),
(54, '', NULL, '2025-04-10 18:04:20', NULL, NULL, '2025-04-10 18:04:20', 0, 'Unknown', 'GATE 1', 'Unknown', 'faces/20250411020420.jpg', 'Unknown', 0, 0),
(55, '', NULL, '2025-04-10 18:05:20', NULL, NULL, '2025-04-10 18:05:20', 0, 'Unknown', 'GATE 1', 'Unknown', 'faces/20250411020520.jpg', 'Unknown', 0, 0),
(56, 'NBC 1234', NULL, '2025-04-10 18:05:43', NULL, NULL, '2025-04-10 18:05:43', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(57, '', NULL, '2025-04-10 18:06:20', NULL, NULL, '2025-04-10 18:06:20', 0, 'Unknown', 'GATE 1', 'Unknown', 'faces/20250411020620.jpg', 'Unknown', 0, 0),
(58, 'DBA 4658', NULL, '2025-04-10 18:06:33', NULL, NULL, '2025-04-10 18:06:33', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(59, 'dbA 4658', NULL, '2025-04-10 18:06:35', NULL, NULL, '2025-04-10 18:06:35', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(60, 'DBA_4658', NULL, '2025-04-10 18:06:37', NULL, NULL, '2025-04-10 18:06:37', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(61, 'DBA4658', NULL, '2025-04-10 18:06:37', NULL, NULL, '2025-04-10 18:06:37', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(62, 'DBA 4658]', NULL, '2025-04-10 18:06:38', NULL, NULL, '2025-04-10 18:06:38', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(63, 'IDBA 4658', NULL, '2025-04-10 18:06:39', NULL, NULL, '2025-04-10 18:06:39', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(64, 'Idba 4658', NULL, '2025-04-10 18:06:40', NULL, NULL, '2025-04-10 18:06:40', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(65, 'DBA  4658', NULL, '2025-04-10 18:06:40', NULL, NULL, '2025-04-10 18:06:40', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(66, 'DBA  46581', NULL, '2025-04-10 18:06:41', NULL, NULL, '2025-04-10 18:06:41', 0, 'blue', 'GATE 1', 'Unknown', 'Unknown', 'Unknown', 0, 0),
(67, '', NULL, '2025-04-10 18:07:20', NULL, NULL, '2025-04-10 18:07:20', 0, 'Unknown', 'GATE 1', 'Unknown', 'faces/20250411020720.jpg', 'Unknown', 0, 0),
(68, '', NULL, '2025-04-10 18:19:55', NULL, NULL, '2025-04-10 18:19:55', 0, '', 'GATE 1', '', 'faces/20250411021955.jpg', 'Hyacinth', 0, 0),
(69, '', NULL, '2025-04-10 18:20:55', NULL, NULL, '2025-04-10 18:20:55', 0, '', 'GATE 1', '', 'faces/20250411022055.jpg', 'Hyacinth', 0, 0),
(70, 'RPC 7777', NULL, '2025-04-10 18:21:10', NULL, NULL, '2025-04-10 18:21:10', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(71, '', NULL, '2025-04-10 18:30:48', NULL, NULL, '2025-04-10 18:30:48', 0, '', 'GATE 1', '', 'faces/20250411023048.jpg', 'Hyacinth', 0, 0),
(72, '', NULL, '2025-04-10 18:31:48', NULL, NULL, '2025-04-10 18:31:48', 0, '', 'GATE 1', '', 'faces/20250411023148.jpg', 'Hyacinth', 0, 0),
(73, 'RPC 7777', NULL, '2025-04-10 18:31:52', NULL, NULL, '2025-04-10 18:31:52', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(74, 'NGp 3944', NULL, '2025-04-10 18:32:17', NULL, NULL, '2025-04-10 18:32:17', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(75, 'ABY', NULL, '2025-04-10 18:32:20', NULL, NULL, '2025-04-10 18:32:20', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(76, 'ABY 8512 |', NULL, '2025-04-10 18:32:21', NULL, NULL, '2025-04-10 18:32:21', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(77, 'ABY 8512|', NULL, '2025-04-10 18:32:21', NULL, NULL, '2025-04-10 18:32:21', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(78, 'ABY 8512', NULL, '2025-04-10 18:32:21', NULL, NULL, '2025-04-10 18:32:21', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(79, 'ABY 8512]', NULL, '2025-04-10 18:32:23', NULL, NULL, '2025-04-10 18:32:23', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(80, 'ABY 8512 ', NULL, '2025-04-10 18:32:23', NULL, NULL, '2025-04-10 18:32:23', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(81, '', NULL, '2025-04-10 18:36:55', NULL, NULL, '2025-04-10 18:36:55', 0, '', 'GATE 1', '', 'faces/20250411023655.jpg', 'Hyacinth', 0, 0),
(82, '', NULL, '2025-04-10 18:37:55', NULL, NULL, '2025-04-10 18:37:55', 0, '', 'GATE 1', '', 'faces/20250411023755.jpg', 'Hyacinth', 0, 0),
(83, 'DBA 4658', NULL, '2025-04-10 18:37:59', NULL, NULL, '2025-04-10 18:37:59', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(84, 'cax 3200', NULL, '2025-04-10 18:38:08', NULL, NULL, '2025-04-10 18:38:08', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(85, 'Cax 3200', NULL, '2025-04-10 18:38:09', NULL, NULL, '2025-04-10 18:38:09', 0, 'blue', 'GATE 1', 'Unknown', '', '', 0, 0),
(86, 'Cax', NULL, '2025-04-10 18:38:13', NULL, NULL, '2025-04-10 18:38:13', 0, 'white', 'GATE 1', 'Unknown', '', '', 0, 0),
(87, '', NULL, '2025-04-10 18:45:01', NULL, NULL, '2025-04-10 18:45:01', 0, '', 'Gate 1', '', 'faces/20250411024501.jpg', 'Hyacinth', 0, 0),
(88, '', NULL, '2025-04-10 18:46:01', NULL, NULL, '2025-04-10 18:46:01', 0, '', 'Gate 1', '', 'faces/20250411024601.jpg', 'Hyacinth', 0, 0),
(89, 'DBA4658', NULL, '2025-04-10 18:46:26', NULL, NULL, '2025-04-10 18:46:26', 0, 'blue', 'Gate 1', 'Unknown', '', '', 0, 0),
(90, 'NBC1234', NULL, '2025-04-10 18:46:46', NULL, NULL, '2025-04-10 18:46:46', 0, 'blue', 'Gate 1', 'Unknown', '', '', 0, 0),
(91, 'NBC1234', NULL, '2025-04-12 14:29:26', NULL, NULL, '2025-04-12 14:29:26', 0, 'Unknown', 'Main Entrance', 'Sedan', 'faces/NBC1234_20250412222926.jpg', '', 0, 0),
(92, 'DBA4658', NULL, '2025-04-12 14:30:27', NULL, NULL, '2025-04-12 14:30:27', 0, 'Unknown', 'Back Parking', 'Sedan', '', '', 0, 0),
(93, '191TPV', NULL, '2025-04-12 16:35:49', NULL, NULL, '2025-04-12 16:35:49', 0, 'red', 'Gate 1', 'Large Vehicle', 'faces/20250413003549.jpg', 'Hyacinth', 1, 0),
(94, '191TPV', NULL, '2025-04-12 16:46:24', NULL, NULL, '2025-04-12 16:46:24', 0, 'red', 'Gate 1', 'SUV/Truck', 'faces/20250413004624.jpg', 'Hyacinth', 1, 0),
(95, '191TPV', NULL, '2025-04-12 16:46:24', NULL, NULL, '2025-04-12 16:46:24', 0, 'red', 'Gate 1', 'SUV/Truck', 'faces/20250413004624.jpg', 'Hyacinth', 1, 0),
(96, 'RPC7777', NULL, '2025-04-12 16:47:00', NULL, NULL, '2025-04-12 16:47:00', 0, 'white', 'Gate 1', 'Large Vehicle', 'faces/20250413004700.jpg', 'Hyacinth', 1, 0),
(97, 'RPC7777', NULL, '2025-04-12 16:47:00', NULL, NULL, '2025-04-12 16:47:00', 0, 'white', 'Gate 1', 'Large Vehicle', 'faces/20250413004700.jpg', 'Hyacinth', 1, 0),
(98, 'DDD1000', NULL, '2025-04-12 16:47:19', NULL, NULL, '2025-04-12 16:47:19', 0, 'white', 'Gate 1', 'SUV/Truck', 'faces/20250413004719.jpg', 'JohnRae', 1, 0),
(99, 'DDD1000', NULL, '2025-04-12 16:47:19', NULL, NULL, '2025-04-12 16:47:19', 0, 'white', 'Gate 1', 'SUV/Truck', 'faces/20250413004719.jpg', 'JohnRae', 1, 0),
(100, '71', NULL, '2025-04-12 18:02:25', NULL, NULL, '2025-04-12 18:02:25', 0, 'red', 'Gate 1', 'Large Vehicle', 'faces/20250413020220.jpg', 'JohnRae', 1, 0),
(101, 'NGP3944', NULL, '2025-04-12 21:05:31', NULL, NULL, '2025-04-12 21:05:31', 0, 'red', 'Gate 1', 'Large Vehicle', 'faces/20250413050531.jpg', 'Hyacinth', 1, 0),
(102, 'DBA4658', NULL, '2025-04-12 21:05:56', NULL, NULL, '2025-04-12 21:05:56', 0, 'white', 'Gate 1', 'SUV/Truck', 'faces/20250413050555.jpg', 'Hyacinth', 1, 0),
(103, 'RPC7777', NULL, '2025-04-12 22:29:25', NULL, NULL, '2025-04-12 22:29:25', 0, 'black', 'Gate 1', 'Large Vehicle', 'faces/20250413062924.jpg', 'JohnRae', 1, 0),
(104, 'NGP3944', NULL, '2025-04-12 22:29:31', NULL, NULL, '2025-04-12 22:29:31', 0, 'red', 'Gate 1', 'SUV/Truck', 'faces/20250413062930.jpg', 'JohnRae', 1, 0),
(105, 'DBA4658', NULL, '2025-04-12 22:29:34', NULL, NULL, '2025-04-12 22:29:34', 0, 'white', 'Gate 1', 'SUV/Truck', 'faces/20250413062934.jpg', 'JohnRae', 1, 0),
(106, 'CAX3260', NULL, '2025-04-12 22:29:43', NULL, NULL, '2025-04-12 22:29:43', 0, 'black', 'Gate 1', 'Large Vehicle', 'faces/20250413062943.jpg', 'JohnRae', 1, 0),
(107, 'AB1312', NULL, '2025-04-13 00:20:47', NULL, NULL, '2025-04-13 00:20:47', 0, 'white', 'Gate 1', 'Motorcycle', 'faces/20250413082047.jpg', 'Hyacinth', 1, 0),
(108, '123SNA', NULL, '2025-04-13 00:21:19', NULL, NULL, '2025-04-13 00:21:19', 0, 'blue', 'Gate 1', 'Large Vehicle', 'faces/20250413082119.jpg', 'Hyacinth', 1, 0),
(109, 'RPC7777', NULL, '2025-04-13 01:18:20', NULL, NULL, '2025-04-13 01:18:20', 0, 'black', 'Gate 1', 'Car', 'faces/20250413091820.jpg', 'Hyacinth', 1, 0),
(110, 'RPC7777', NULL, '2025-04-13 01:18:20', NULL, NULL, '2025-04-13 01:18:20', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250413091820.jpg', 'Hyacinth', 1, 0),
(111, 'RPC7777', NULL, '2025-04-13 01:18:20', NULL, NULL, '2025-04-13 01:18:20', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250413091820.jpg', 'Hyacinth', 1, 0),
(112, 'RPC7777', NULL, '2025-04-13 01:18:20', NULL, NULL, '2025-04-13 01:18:20', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250413091820.jpg', 'Hyacinth', 1, 0),
(113, 'RPC7777', NULL, '2025-04-13 01:18:21', NULL, NULL, '2025-04-13 01:18:21', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250413091820.jpg', 'Hyacinth', 1, 0),
(114, 'RPC7777', NULL, '2025-04-13 01:18:21', NULL, NULL, '2025-04-13 01:18:21', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250413091821.jpg', 'Hyacinth', 1, 0),
(115, 'RPC7777', NULL, '2025-04-13 01:18:21', NULL, NULL, '2025-04-13 01:18:21', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250413091821.jpg', 'Hyacinth', 1, 0),
(116, 'RPC7777', NULL, '2025-04-13 01:18:21', NULL, NULL, '2025-04-13 01:18:21', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250413091821.jpg', 'Hyacinth', 1, 0),
(117, 'RPC7777', NULL, '2025-04-13 01:18:21', NULL, NULL, '2025-04-13 01:18:21', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250413091821.jpg', 'Hyacinth', 1, 0),
(118, 'RPC7777', NULL, '2025-04-13 03:31:37', NULL, NULL, '2025-04-13 03:31:37', 0, 'black', 'Gate 1', 'Car', 'faces/20250413113137.jpg', 'Hyacinth', 1, 0),
(119, 'NGP3944', NULL, '2025-04-13 03:32:02', NULL, NULL, '2025-04-13 03:32:02', 0, 'red', 'Gate 1', 'Car', 'faces/20250413113202.jpg', 'Hyacinth', 1, 0),
(120, 'NBC1234', NULL, '2025-04-13 22:56:10', NULL, NULL, '2025-04-13 22:56:10', 0, 'blue', 'Gate 1', 'Car', 'faces/20250414065610.jpg', 'JohnRae', 1, 0),
(121, 'DBA4658', NULL, '2025-04-13 22:56:34', NULL, NULL, '2025-04-13 22:56:34', 0, 'blue', 'Gate 1', 'Car', 'faces/20250414065633.jpg', 'Hyacinth', 1, 0),
(122, 'DBA4658', NULL, '2025-04-13 23:05:15', NULL, NULL, '2025-04-13 23:05:15', 0, 'blue', 'Gate 1', 'Car', 'faces/20250414070514.jpg', 'Hyacinth', 1, 0),
(123, 'ABY8512', NULL, '2025-04-13 23:05:27', NULL, NULL, '2025-04-13 23:05:27', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250414070527.jpg', 'Hyacinth', 1, 0),
(124, 'ABY8512', NULL, '2025-04-13 23:13:04', NULL, NULL, '2025-04-13 23:13:04', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250414071304.jpg', 'Hyacinth', 1, 0),
(125, 'NBC1234', NULL, '2025-04-13 23:46:38', NULL, NULL, '2025-04-13 23:46:38', 0, 'blue', 'Gate 1', 'SUV/Truck', 'faces/20250414074637.jpg', 'Hyacinth', 1, 0),
(126, 'DBA4658', NULL, '2025-04-13 23:49:29', NULL, NULL, '2025-04-13 23:49:29', 0, 'blue', 'Gate 1', 'Car', 'faces/20250414074929.jpg', 'Hyacinth', 1, 0),
(127, 'NBC1234', NULL, '2025-04-14 03:15:28', NULL, NULL, '2025-04-14 03:15:28', 0, 'black', 'Gate 1', 'Car', 'faces/20250414111528.jpg', 'Hyacinth', 1, 0),
(128, '329XSB', NULL, '2025-04-14 03:26:07', NULL, NULL, '2025-04-14 03:26:07', 0, 'black', 'Gate 1', 'SUV/Truck', 'faces/20250414112607.jpg', 'CHI', 1, 0),
(129, 'CAX3200', NULL, '2025-04-14 03:27:44', NULL, NULL, '2025-04-14 03:27:44', 0, 'white', 'Gate 1', 'SUV/Truck', 'faces/20250414112744.jpg', 'CHI', 1, 0),
(130, 'CAX3260', NULL, '2025-04-14 03:27:45', NULL, NULL, '2025-04-14 03:27:45', 0, 'white', 'Gate 1', 'SUV/Truck', 'faces/20250414112744.jpg', 'CHI', 1, 0),
(131, 'NBC1234', NULL, '2025-04-21 00:57:56', NULL, NULL, '2025-04-21 00:57:56', 0, 'black', 'Gate 1', 'cell phone', 'faces/20250421085756.jpg', 'Hyacinth', 1, 0),
(132, 'NXX8870', NULL, '2025-04-21 00:58:50', NULL, NULL, '2025-04-21 00:58:50', 0, 'blue', 'Gate 1', 'person', 'faces/20250421085850.jpg', 'Hyacinth', 1, 0),
(133, 'NKX8870', NULL, '2025-04-21 00:58:50', NULL, NULL, '2025-04-21 00:58:50', 0, 'blue', 'Gate 1', 'person', 'faces/20250421085850.jpg', 'Hyacinth', 1, 0),
(134, 'CAX3200', NULL, '2025-04-21 01:02:51', NULL, NULL, '2025-04-21 01:02:51', 0, 'black', 'Gate 1', 'cell phone', 'faces/20250421090251.jpg', 'Hyacinth', 1, 0),
(135, 'CAX3260', NULL, '2025-04-21 01:02:52', NULL, NULL, '2025-04-21 01:02:52', 0, 'blue', 'Gate 1', 'cell phone', 'faces/20250421090252.jpg', 'Hyacinth', 1, 0),
(136, 'CAX3200', NULL, '2025-04-21 01:06:37', NULL, NULL, '2025-04-21 01:06:37', 0, 'white', 'Gate 1', 'license_plate', 'faces/20250421090636.jpg', 'Hyacinth', 1, 0),
(137, 'CAX3260', NULL, '2025-04-21 01:06:38', NULL, NULL, '2025-04-21 01:06:38', 0, 'white', 'Gate 1', 'license_plate', 'faces/20250421090637.jpg', 'Hyacinth', 1, 0),
(138, 'NXX8870', NULL, '2025-04-21 01:22:09', NULL, NULL, '2025-04-21 01:22:09', 0, 'white', 'Gate 1', 'license_plate', 'faces/20250421092208.jpg', 'Hyacinth', 1, 0),
(139, 'NKX8870', NULL, '2025-04-21 01:23:01', NULL, NULL, '2025-04-21 01:23:01', 0, 'blue', 'Gate 1', 'face_recognition', 'faces/20250421092301.jpg', 'JohnRae', 1, 0),
(140, 'NXX8875', NULL, '2025-04-21 01:47:47', NULL, NULL, '2025-04-21 01:47:47', 0, 'blue', 'Gate 1', 'face_recognition', 'faces/20250421094747.jpg', 'Hyacinth', 1, 0),
(141, 'NXX8870', NULL, '2025-04-21 01:47:47', NULL, NULL, '2025-04-21 01:47:47', 0, 'blue', 'Gate 1', 'face_recognition', 'faces/20250421094747.jpg', 'Hyacinth', 1, 0),
(142, 'NXX8876', NULL, '2025-04-21 01:47:48', NULL, NULL, '2025-04-21 01:47:48', 0, 'blue', 'Gate 1', 'face_recognition', 'faces/20250421094748.jpg', 'Hyacinth', 1, 0),
(143, 'DBA4658', NULL, '2025-04-21 01:48:25', NULL, NULL, '2025-04-21 01:48:25', 0, 'white', 'Gate 1', 'license_plate', 'faces/20250421094824.jpg', 'Hyacinth', 1, 0),
(144, '46', NULL, '2025-04-21 01:48:27', NULL, NULL, '2025-04-21 01:48:27', 0, 'white', 'Gate 1', 'license_plate', 'faces/20250421094827.jpg', 'Hyacinth', 1, 0),
(145, 'DBA4658', NULL, '2025-04-21 01:52:50', NULL, NULL, '2025-04-21 01:52:50', 0, 'white', 'Gate 1', 'license_plate', 'faces/20250421095250.jpg', 'Hyacinth', 1, 0),
(146, 'NBC1234', NULL, '2025-04-21 06:21:19', NULL, NULL, '2025-04-21 06:21:19', 0, 'Red', 'Gate 1', 'pickup', 'faces/20250421142118.jpg', 'Hyacinth', 1, 0),
(147, 'RPC7777', NULL, '2025-04-21 06:21:53', NULL, NULL, '2025-04-21 06:21:53', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142151.jpg', 'Hyacinth', 1, 0),
(148, 'RPC7717', NULL, '2025-04-21 06:21:54', NULL, NULL, '2025-04-21 06:21:54', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142152.jpg', 'Hyacinth', 1, 0),
(149, '17', NULL, '2025-04-21 06:21:55', NULL, NULL, '2025-04-21 06:21:55', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142152.jpg', 'Hyacinth', 1, 0),
(150, '3', NULL, '2025-04-21 06:22:57', NULL, NULL, '2025-04-21 06:22:57', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142256.jpg', 'CHI', 1, 0),
(151, '6', NULL, '2025-04-21 06:22:58', NULL, NULL, '2025-04-21 06:22:58', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142256.jpg', 'CHI', 1, 0),
(152, '1', NULL, '2025-04-21 06:23:02', NULL, NULL, '2025-04-21 06:23:02', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142301.jpg', 'Hyacinth', 1, 0),
(153, '12', NULL, '2025-04-21 06:23:03', NULL, NULL, '2025-04-21 06:23:03', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142302.jpg', 'Hyacinth', 1, 0),
(154, 'NBC1234', NULL, '2025-04-21 06:23:04', NULL, NULL, '2025-04-21 06:23:04', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142303.jpg', 'Hyacinth', 1, 0),
(155, 'NBC1234', NULL, '2025-04-21 06:27:37', NULL, NULL, '2025-04-21 06:27:37', 0, 'Red', 'Gate 1', 'pickup', 'faces/20250421142736.jpg', 'Hyacinth', 1, 0),
(156, '60', NULL, '2025-04-21 06:27:43', NULL, NULL, '2025-04-21 06:27:43', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142742.jpg', 'Hyacinth', 1, 0),
(157, '8', NULL, '2025-04-21 06:27:44', NULL, NULL, '2025-04-21 06:27:44', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421142742.jpg', 'Hyacinth', 1, 0),
(158, 'NBC1234', NULL, '2025-04-21 06:34:47', NULL, NULL, '2025-04-21 06:34:47', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421143446.jpg', 'Hyacinth', 1, 0),
(159, '1', NULL, '2025-04-21 06:34:53', NULL, NULL, '2025-04-21 06:34:53', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421143451.jpg', 'Hyacinth', 1, 0),
(160, '12', NULL, '2025-04-21 06:44:19', NULL, NULL, '2025-04-21 06:44:19', 0, 'Red', 'Gate 1', 'pickup', 'faces/20250421144418.jpg', 'Hyacinth', 1, 0),
(161, 'NBC1234', NULL, '2025-04-21 06:44:33', NULL, NULL, '2025-04-21 06:44:33', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421144432.jpg', 'Hyacinth', 1, 0),
(162, 'RPC7777', NULL, '2025-04-21 06:45:03', NULL, NULL, '2025-04-21 06:45:03', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421144502.jpg', 'Hyacinth', 1, 0),
(163, 'PPC7773', NULL, '2025-04-21 07:28:54', NULL, NULL, '2025-04-21 07:28:54', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421152853.jpg', 'Hyacinth', 1, 0),
(164, 'RPC7777', NULL, '2025-04-21 07:28:55', NULL, NULL, '2025-04-21 07:28:55', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421152854.jpg', 'Hyacinth', 1, 0),
(165, 'RPC7777', NULL, '2025-04-21 07:35:10', NULL, NULL, '2025-04-21 07:35:10', 0, 'Red', 'Gate 1', 'pickup', 'faces/20250421153510.jpg', 'Hyacinth', 1, 0),
(166, 'DBA4658', NULL, '2025-04-21 07:35:58', NULL, NULL, '2025-04-21 07:35:58', 0, 'Red', 'Gate 1', 'pickup', 'faces/20250421153557.jpg', 'Hyacinth', 1, 0),
(167, 'DBA4658', NULL, '2025-04-21 07:48:50', NULL, NULL, '2025-04-21 07:48:50', 0, 'Red', 'Gate 1', 'pickup', 'faces/20250421154850.jpg', 'Hyacinth', 1, 0),
(168, '6', NULL, '2025-04-21 07:51:15', NULL, NULL, '2025-04-21 07:51:15', 0, 'Red', 'Gate 1', 'pickup', 'faces/20250421155114.jpg', 'Hyacinth', 1, 0),
(169, '4', NULL, '2025-04-21 07:53:16', NULL, NULL, '2025-04-21 07:53:16', 0, 'Red', 'Gate 1', 'face_recognition', 'faces/20250421155316.jpg', 'Hyacinth', 1, 0),
(170, 'RPC7777', NULL, '2025-04-21 07:56:43', NULL, NULL, '2025-04-21 07:56:43', 0, 'Green', 'Gate 1', 'coupe', 'faces/20250421155643.jpg', 'Hyacinth', 1, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `plate_numbers`
--
ALTER TABLE `plate_numbers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plate_numbers_plate_number_index` (`plate_number`),
  ADD KEY `plate_numbers_scanned_at_index` (`scanned_at`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `plate_numbers`
--
ALTER TABLE `plate_numbers`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=171;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
