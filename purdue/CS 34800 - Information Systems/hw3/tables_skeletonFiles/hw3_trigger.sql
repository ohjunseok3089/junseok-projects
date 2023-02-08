DELIMITER //

CREATE TRIGGER beforePlaceInsert
BEFORE INSERT
ON place FOR EACH ROW

BEGIN
    DECLARE host_count INTEGER;
    DECLARE exist INTEGER;
    
    SET host_count = (SELECT count(host_id) + 1 FROM place WHERE host_id = NEW.host_id);
    IF (host_count = 1) THEN
        DELETE FROM businessHosts WHERE businessHosts.host_id = NEW.host_id;
    END IF;
    SET exist = (SELECT count(host_id) FROM businessHosts WHERE businessHosts.host_id = NEW.host_id);
    IF (exist > 0) THEN
        UPDATE businessHosts SET n_count = host_count WHERE businessHosts.host_id = NEW.host_id;
    ELSE
        INSERT INTO businessHosts VALUES (NEW.host_id, host_count);
    END IF;
END //

DELIMITER ;


