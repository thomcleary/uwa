CREATE FUNCTION numScoops(coneNumber INT)
RETURNS INT DETERMINISTIC
RETURN (SELECT COUNT(*)
		FROM ScoopsInCone
        WHERE coneID = coneNumber);

DELIMITER ++
CREATE PROCEDURE purchaseSummary(purchaseNum INT,
                                 OUT oneScoop INT,
                                 OUT twoScoop INT,
                                 OUT threeScoop INT)
BEGIN

DECLARE coneNum INT;
DECLARE scoopNum INT;
DECLARE cursorFinished INT DEFAULT FALSE;

DECLARE purchaseCones CURSOR FOR
	SELECT coneID
    FROM ConesInPurchase
    WHERE purchaseID = purchaseNum;
    
DECLARE CONTINUE HANDLER FOR NOT FOUND
	SET cursorFinished = TRUE;

OPEN purchaseCones;

SET oneScoop = 0;
SET twoScoop = 0;
SET threeScoop = 0;

read_loop : LOOP
	
    FETCH purchaseCones INTO coneNum;
    
    IF cursorFinished THEN
		LEAVE read_loop;
	END IF;
    
    SET scoopNum = numScoops(coneNum);
    
    IF scoopNum <=> 1 THEN
		SET oneScoop = oneScoop + 1;
	
    ELSEIF scoopNum <=> 2 THEN
		SET twoScoop = twoScoop + 1;
	
    ELSEIF scoopNum <=> 3 THEN
		SET threeScoop = threeScoop + 1;
	
    END IF;

END LOOP;

CLOSE purchaseCones;
    
END ++
DELIMITER ;