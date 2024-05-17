-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: trip
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blogs`
--

DROP TABLE IF EXISTS `blogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blogs` (
  `blog_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` varchar(50) DEFAULT NULL,
  `place_id` int DEFAULT NULL,
  PRIMARY KEY (`blog_id`),
  KEY `user_id` (`user_id`),
  KEY `place_id` (`place_id`),
  CONSTRAINT `blogs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `blogs_ibfk_2` FOREIGN KEY (`place_id`) REFERENCES `places` (`place_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blogs`
--

LOCK TABLES `blogs` WRITE;
/*!40000 ALTER TABLE `blogs` DISABLE KEYS */;
INSERT INTO `blogs` VALUES (10,'vijayawada Blog','Vijayawada boasts ancient landmarks that stand as testaments to its glorious past. The Kanaka Durga Temple, perched atop the Indrakeeladri Hill, is a revered pilgrimage site where devotees seek solace and blessings from the goddess. Nearby, the awe-inspiring Undavalli Caves showcase intricate rock-cut architecture dating back centuries, offering a glimpse into the region\'s storied past.','2024-05-16 07:24:07','usha',2),(11,'Explore Hyderabad','Hyderabad, a city rich in history and culture, boasts iconic landmarks like the Charminar and Golconda Fort. The Chowmahalla Palace offers a glimpse into its royal past, showcasing opulent architecture and artifacts. Food enthusiasts can\'t miss the aromatic flavors of Hyderabadi biryani and other culinary delights. Ramoji Film City offers a unique experience for movie buffs and families, with film sets and amusement rides. Hyderabad\'s modern side shines through its upscale malls, vibrant nightlife, and thriving IT industry in areas like HITEC City. This vibrant blend of old-world charm and modernity makes Hyderabad a captivating destination for travelers.','2024-05-17 09:06:08','usha',3);
/*!40000 ALTER TABLE `blogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `number_of_rooms` int DEFAULT NULL,
  `hotel_id` int DEFAULT NULL,
  PRIMARY KEY (`booking_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `contact_number` (`contact_number`),
  KEY `hotel_id` (`hotel_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`hotel_id`) REFERENCES `hotels` (`hotel_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotel_registration`
--

DROP TABLE IF EXISTS `hotel_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel_registration` (
  `hotel_id` int NOT NULL AUTO_INCREMENT,
  `hotel_email` varchar(100) NOT NULL,
  `hotel_phone_number` varchar(20) DEFAULT NULL,
  `hotel_name` varchar(100) NOT NULL,
  `hotel_place` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `hotel_username` varchar(50) NOT NULL,
  PRIMARY KEY (`hotel_id`),
  UNIQUE KEY `hotel_email` (`hotel_email`),
  UNIQUE KEY `hotel_username` (`hotel_username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel_registration`
--

LOCK TABLES `hotel_registration` WRITE;
/*!40000 ALTER TABLE `hotel_registration` DISABLE KEYS */;
INSERT INTO `hotel_registration` VALUES (4,'vijayalakshmi@codegnan.com','9876543210','AA\'s Kitchens','Bengaluru','1234','vijayalakshmi'),(5,'usharanireddy901@gmail.com','456789','usha','vijayawada','123','usha'),(8,'balakoppu999@gmail.com','9010524369','balatripura','vijayawada','123','bts');
/*!40000 ALTER TABLE `hotel_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotels`
--

DROP TABLE IF EXISTS `hotels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotels` (
  `hotel_id` int NOT NULL AUTO_INCREMENT,
  `hotel_name` varchar(100) NOT NULL,
  `hotel_picture` varchar(200) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address_details` text,
  `timings` varchar(100) DEFAULT NULL,
  `total_rooms` int DEFAULT NULL,
  `room_cost` decimal(10,2) DEFAULT NULL,
  `hotel_description` text,
  `room_images` varchar(255) DEFAULT NULL,
  `room_availability` enum('available','not available') DEFAULT 'available',
  `available_rooms` int DEFAULT NULL,
  `place_id` int DEFAULT NULL,
  `added_by` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`hotel_id`),
  UNIQUE KEY `hotel_name` (`hotel_name`),
  UNIQUE KEY `contact_number` (`contact_number`),
  UNIQUE KEY `email` (`email`),
  KEY `place_id` (`place_id`),
  KEY `added_by` (`added_by`),
  CONSTRAINT `hotels_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`place_id`),
  CONSTRAINT `hotels_ibfk_2` FOREIGN KEY (`added_by`) REFERENCES `hotel_registration` (`hotel_username`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotels`
--

LOCK TABLES `hotels` WRITE;
/*!40000 ALTER TABLE `hotels` DISABLE KEYS */;
INSERT INTO `hotels` VALUES (46,'Ilapuram Hotel','Y1pD3gH4h','0987654332','usharanireddy901@gmail.com','GJ8G+86P, Besant Rd, Gandhi Nagar, Vijayawada, Andhra Pradesh 520002','9 Am to 11PM',30,2000.00,'Guests looking for a luxury dining restaurant in Vijayawada will delight in our award winning Thai, contemporary Chinese, all day international fine dining restaurant and colonial style bar. Exquisitely decorated and refreshed with garden views, each offers a unique ambience, unparalleled cuisine and matchless service.','Y1aW2eL9j','available',29,2,'usha'),(48,'Novotel','C4dS6eP2b','9010524368','chandumannepalli16@gmail.com','Bag 1101 Cyberabad, Post Office, Novotel & HICC Complex, P.O, near Hitec City, Hyderabad, Telangana 500081','9 Am to 11PM',50,10000.00,'Novotel caters to business and leisure travelers, with hotels located in the heart of major international cities, business districts and tourist destinations. Novotel manages 559 hotels in 65 countries (2021).','C3xK2tC9r','available',25,3,'usha');
/*!40000 ALTER TABLE `hotels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `places`
--

DROP TABLE IF EXISTS `places`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `places` (
  `place_id` int NOT NULL AUTO_INCREMENT,
  `place_name` varchar(100) NOT NULL,
  `place_pic` varchar(200) DEFAULT NULL,
  `added_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`place_id`),
  UNIQUE KEY `place_name` (`place_name`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `places`
--

LOCK TABLES `places` WRITE;
/*!40000 ALTER TABLE `places` DISABLE KEYS */;
INSERT INTO `places` VALUES (2,'vijayawada','F9qV6rK9v','lemon@1'),(3,'hyderabad','O4zP9sR6w','Abhi'),(18,'Tirupathi','W7xP3yX4u','usha'),(19,'varanasi','J3zF2rD3e','usha'),(20,'munar','W9lN6jI7m','usha'),(21,'kochi','M2sR7wE5s','usha'),(22,'bengalore','Z8uG2iY7o','usha'),(23,'Goa','K8mT3rS0e','usha');
/*!40000 ALTER TABLE `places` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trip_bookings`
--

DROP TABLE IF EXISTS `trip_bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trip_bookings` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `package_id` int DEFAULT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `package_id` (`package_id`),
  CONSTRAINT `trip_bookings_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `trip_package` (`package_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trip_bookings`
--

LOCK TABLES `trip_bookings` WRITE;
/*!40000 ALTER TABLE `trip_bookings` DISABLE KEYS */;
/*!40000 ALTER TABLE `trip_bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trip_package`
--

DROP TABLE IF EXISTS `trip_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trip_package` (
  `package_id` int NOT NULL AUTO_INCREMENT,
  `place_id` int DEFAULT NULL,
  `package_name` varchar(255) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `duration_days` int DEFAULT NULL,
  `includes_amenities` text,
  `excludes_amenities` text,
  `company_name` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`package_id`),
  UNIQUE KEY `company_name` (`company_name`),
  KEY `place_id` (`place_id`),
  KEY `fk_username` (`username`),
  CONSTRAINT `fk_username` FOREIGN KEY (`username`) REFERENCES `tripplanner_registration` (`username`),
  CONSTRAINT `trip_package_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`place_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trip_package`
--

LOCK TABLES `trip_package` WRITE;
/*!40000 ALTER TABLE `trip_package` DISABLE KEYS */;
INSERT INTO `trip_package` VALUES (14,2,'vijayawada trip','Vijayawada is a major city located on the banks of the Krishna River in the Indian state of Andhra Pradesh. It serves as the headquarters of the Krishna district. Historically, it has been a significant center for trade and commerce due to its strategic location along major transportation routes.',10000.00,'2024-05-16','2024-05-20',5,'Sri Durga Malleswari Temple,Bhavani Isand,Gandhi Hill,Rajiv Gandhi Park,Undavalli Caves,Lenin Statue,Bapu Museum','air fare,train fare,insurnace premium','hyma','usha'),(21,3,'Hyderabad Trip','Hyderabad is known as The City of Pearls, as once it was the only global centre for trade of large diamonds, emeralds and natural pearls. Many traditional and historical bazaars are located around the city.',10000.00,'2024-05-18','2024-05-24',NULL,'Historical monuments.\r\nReligious places.\r\nMuseums and planetarium.\r\nLakes of Hyderabad.\r\nParks and gardens.\r\nShopping Malls and modern places.','Flights: We do not manage flights as part of our trip packages. Check out our article on Flight Best Practices for more info! \r\n\r\nAdditional Food and Drink: Your trip will list which meals are included in your itinerary. Anything extra will be at your own discretion and expense. \r\n\r\nExtraneous Activities: Your trip will always include a set list of activities, experiences, and/or workshops. Some trips will even have additional optional activities to add to your booking for an additional price. However, if you wish to participate in other activities outside of Trova, you will be responsible for the cost. ','usha','usha');
/*!40000 ALTER TABLE `trip_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tripplanner_registration`
--

DROP TABLE IF EXISTS `tripplanner_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tripplanner_registration` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tripplanner_registration`
--

LOCK TABLES `tripplanner_registration` WRITE;
/*!40000 ALTER TABLE `tripplanner_registration` DISABLE KEYS */;
INSERT INTO `tripplanner_registration` VALUES (7,'usha','usharanireddy901@gmail.com','09876543','lkjhgfxcvbnmdfghj','1234');
/*!40000 ALTER TABLE `tripplanner_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('usha','usharanireddy901@gmail.com','9010524368','Jagarla mudi vari street','123');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-17 15:19:49
