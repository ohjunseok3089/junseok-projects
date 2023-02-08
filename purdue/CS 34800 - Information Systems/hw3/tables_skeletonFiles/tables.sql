CREATE TABLE IF NOT EXISTS `placeAvailability` (
   place_id integer,
   ava_date date,
   available TINYINT,
   price DECIMAL(8,2),
   primary key(place_id, ava_date)
);

CREATE TABLE IF NOT EXISTS `cheapestPrices` (
  `place_id` int(11) DEFAULT NULL,
  `startDate` date DEFAULT NULL,
  `endDate` date DEFAULT NULL,
  `total` decimal(8,2) DEFAULT NULL
); 

CREATE TABLE businessHosts (
   host_id integer,
   n_count integer
);


Insert into placeAvailability values  (2539, '2022-02-20', 1, 100.0);
Insert into placeAvailability values  (2539, '2022-02-21', 1, 100.0);
Insert into placeAvailability values  (2539, '2022-02-22', 0, 0.0);
Insert into placeAvailability values  (2539, '2022-02-23', 0, 0.0);
Insert into placeAvailability values  (2539, '2022-02-24', 1, 100.0);

Insert into placeAvailability values  (2595, '2022-02-20', 1, 120);
Insert into placeAvailability values  (2595, '2022-02-21', 1, 100);
Insert into placeAvailability values  (2595, '2022-02-22', 1, 90);
Insert into placeAvailability values  (2595, '2022-02-23', 0, 0);
Insert into placeAvailability values  (2595, '2022-02-24', 0, 0);

Insert into placeAvailability values  (3647, '2022-02-20', 0, 0);
Insert into placeAvailability values  (3647, '2022-02-21', 1, 120);
Insert into placeAvailability values  (3647, '2022-02-22', 0, 0);
Insert into placeAvailability values  (3647, '2022-02-23', 1, 120);
Insert into placeAvailability values  (3647, '2022-02-24', 0, 0);

Insert into placeAvailability values  (3831, '2022-02-20', 1, 95);
Insert into placeAvailability values  (3831, '2022-02-21', 1, 100);
Insert into placeAvailability values  (3831, '2022-02-22', 1, 150);
Insert into placeAvailability values  (3831, '2022-02-23', 1, 60);
Insert into placeAvailability values  (3831, '2022-02-24', 1, 130);

