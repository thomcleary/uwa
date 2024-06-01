-- Query 4
--
-- a) Do countries with a life expectancy greater than 75 have a higher recovery rate?

-- a)
SELECT 
	LifeExpGreaterThan75,
	SUM(Recoveries) AS totalRecovered,
	SUM(ConfirmedCases) AS totalConfirmed,
	CAST(SUM(Recoveries) AS FLOAT) / CAST(SUM(ConfirmedCases) AS FLOAT) AS recoveryRate

FROM FactCovidData
JOIN DimLifeExpectancy ON FactCovidData.LifeExpectancyID = DimLifeExpectancy.LifeExpectancyID

GROUP BY LifeExpGreaterThan75