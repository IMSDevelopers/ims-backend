CREATE TABLE `items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(240) NOT NULL,
  `quantity` int NOT NULL,
  `description` varchar(240) DEFAULT NULL,
  `url_image` text DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time_placed` smalldatetime NOT NULL,
  `accepted` bit(2) NOT NULL,
  `item_id` int NOT NULL,
  `amount` int NOT NULL,
  KEY `item_id` (`item_id`),
  CONSTRAINT `item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`),
  PRIMARY KEY (`id`)
);