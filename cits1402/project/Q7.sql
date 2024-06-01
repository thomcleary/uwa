DELIMITER ++
CREATE FUNCTION isNutFree(coneNumber INT)
RETURNS INT DETERMINISTIC
BEGIN

IF (SELECT coneType
    FROM cone
    WHERE id = coneNumber) = 'Waffle' THEN
    RETURN 0;

ELSEIF 'Coconut' IN (SELECT name 
                 FROM Scoop
                 WHERE id IN (SELECT DISTINCT scoopID
                              FROM ScoopsInCone
                              WHERE coneId = coneNumber))
	OR
    'Macadamia' IN (SELECT name 
                    FROM Scoop
                    WHERE id IN (SELECT DISTINCT scoopID
                                 FROM ScoopsInCone
                                 WHERE coneId = coneNumber)) THEN
	RETURN 0;
END IF;
                              
RETURN 1;

END++
DELIMITER ;