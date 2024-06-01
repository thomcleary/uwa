DELIMITER ++
CREATE PROCEDURE createMonthlyWinners()
BEGIN

DECLARE currPeriod VARCHAR(20);
DECLARE currMax INT;
DECLARE cursorFinished INT DEFAULT FALSE;

DECLARE PeriodMaximums CURSOR FOR
	SELECT dateYear, MAX(purchases)
    FROM ( SELECT CONCAT(MONTHNAME(buyDate), ' ', YEAR(buydate)) AS dateYear, 
                  store, COUNT(*) AS purchases 
           FROM Purchase
	       GROUP by store, dateYear ) A
	GROUP BY dateYear;

DECLARE CONTINUE HANDLER FOR NOT FOUND
	SET cursorFinished = TRUE;

DROP TABLE IF EXISTS MonthlyWinners;
CREATE TABLE MonthlyWinners (
	month VARCHAR(20),
    store VARCHAR(20),
    numPurchases INT
);

OPEN PeriodMaximums;

read_loop : LOOP
	
    FETCH PeriodMaximums INTO currPeriod, currMax;
    
    IF cursorFinished THEN
		LEAVE read_loop;
	END IF;
    
    INSERT INTO MonthlyWinners
    SELECT CONCAT(MONTHNAME(buyDate), ' ', YEAR(buydate)) AS dateYear, 
		   store, COUNT(*) AS purchases 
	FROM Purchase
	GROUP by store, dateYear
	HAVING (dateYear, purchases) IN ((currPeriod, currMax));

END LOOP;

CLOSE PeriodMaximums;
    
END++
DELIMITER ;