CREATE FUNCTION numScoops(coneNumber INT)
RETURNS INT DETERMINISTIC
RETURN (SELECT COUNT(*)
		FROM ScoopsInCone
        WHERE coneID = coneNumber);

DELIMITER ++
CREATE FUNCTION costOfPurchase(purchaseNumber INT)
RETURNS DECIMAL(8, 0) DETERMINISTIC
BEGIN

DECLARE total DECIMAL(8, 3);
DECLARE dayOfWeek VARCHAR(20);
DECLARE currCone INT;
DECLARE numScoops INT;
DECLARE discount DECIMAL(8, 3);
DECLARE cursorFinished INT DEFAULT FALSE;

DECLARE OrderCones CURSOR FOR
	SELECT coneID
    FROM ConesInPurchase
    WHERE purchaseID = purchaseNumber;

DECLARE CONTINUE HANDLER FOR NOT FOUND
	SET cursorFinished = TRUE;

SET total = 50;
SET dayOfWeek = ( SELECT DAYNAME(buyDate)
			      FROM Purchase
                  WHERE id = purchaseNumber );

IF dayOfWeek = 'Sunday' THEN
	SET total = 3 * total;
ELSEIF dayOfWeek = 'Saturday' THEN
	SET total = 2 * total;
END IF;

OPEN OrderCones;

-- For each cone in order
read_loop : LOOP
	
    FETCH OrderCones INTO currCone;
    
    IF cursorFinished THEN
		LEAVE read_loop;
	END IF;
    
    -- Add cone cost
    SET total = total + ( SELECT coneCost
						              FROM Cone
                          WHERE id = currCone );
	-- Add scoops cost
    SET total = total + ( SELECT sum(costInCents)
                          FROM Scoop JOIN ScoopsInCone
                                     ON id = ScoopId
						              WHERE coneID = currCone);
	
    SET numScoops = numScoops(currCone);
    
    -- Check for multiscoop discount
    IF numScoops <=> 2 THEN
		SET total = total - 50;
    ELSEIF numScoops <=> 3 THEN
		SET total = total - 150;
	END IF;
    
END LOOP;

CLOSE OrderCones;

SET discount = ( SELECT discountApplied
                 FROM CustomerPurchases
                 WHERE purchaseID = purchaseNumber ) / 100;


RETURN total * (1 -  discount);
                          
END ++
DELIMITER ;