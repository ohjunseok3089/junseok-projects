

-- Stored Prcoedure Code
DELIMITER //
CREATE PROCEDURE prepWindowPrices (
	IN startDate DATE, IN endDate Date, IN duration integer)
    BEGIN
        DECLARE cheapestPrice INT default 10000;
        DECLARE currDate DATE default startDate;
        DECLARE maxDate DATE default (endDate - INTERVAL (duration - 1) DAY);
        DECLARE tempPrice DECIMAL(8,2);
        DECLARE tempSTART DATE;
        DECLARE tempEND DATE;
        DECLARE tempID integer;
        
        DELETE FROM cheapestPrices;

        dateloop: LOOP
            IF currDate > maxDate THEN
                LEAVE dateloop;
            END IF;
            queryProcedure: BEGIN
                DECLARE finished INTEGER DEFAULT 0;

                DECLARE avaRoom CURSOR FOR
                    SELECT place_id, currDate as startDate, (currDate + INTERVAL (duration - 1) DAY) as endDate, SUM(price) as total
                    FROM placeAvailability
                    WHERE ava_date BETWEEN currDate AND (currDate + INTERVAL (duration - 1) DAY)
                    GROUP BY place_id
                    HAVING SUM(available) = duration;
                DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
                OPEN avaRoom;
                priceQuery: LOOP
                    FETCH avaRoom INTO tempID, tempSTART, tempEND, tempPrice;
                    IF finished = 1 THEN
                        LEAVE priceQuery;
                    END IF;
                    INSERT INTO cheapestPrices VALUES (tempID, tempSTART, tempEND, tempPrice);
                    IF (tempPrice <= cheapestPrice) THEN
                        SET cheapestPrice = tempPrice;
                    END IF;
                END LOOP priceQuery;
                CLOSE avaRoom;
            SET currDate = DATE_ADD(currDate, INTERVAL 1 day);
            END queryProcedure;
        END LOOP dateloop;
        DELETE FROM cheapestPrices WHERE total > cheapestPrice;
    END //
DELIMITER ; 

-- Calling code, remove the double dashes in the beginning when calling the stored procedure
-- set @startDate = '2022-02-20';
-- set @endDate  = '2022-02-24';
-- set @duration = 2;
 
-- call prepWindowPrices(@startDate, @endDate, @duration);
