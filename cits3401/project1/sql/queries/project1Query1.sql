-- Query 1
--
-- a) What is the total number of confirmed cases in Australia in 2020? 
-- b) What is the number of confirmed cases in each quarter of 2020 in Australia? 
-- c) What is the number of confirmed cases in each month of 2020 in Australia?


-- a)
SELECT Country, Year, SUM(ConfirmedCases) AS totalConfirmed2020

FROM FactCovidData
JOIN DimTime ON FactCovidData.TimeID = DimTime.TimeID
JOIN DimLocation ON FactCovidData.LocationID = DimLocation.LocationID

WHERE Country = 'Australia'
	AND Year = 2020

GROUP BY Country, Year


-- b)
SELECT Country, Quarter, SUM(ConfirmedCases) AS totalConfirmedInQuarter

FROM FactCovidData
JOIN DimTime ON FactCovidData.TimeID = DimTime.TimeID
JOIN DimLocation ON FactCovidData.LocationID = DimLocation.LocationID

WHERE Country = 'Australia'
	AND Year = 2020

GROUP BY Country, Quarter


-- c)
SELECT Country, Month, ConfirmedCases

FROM FactCovidData
JOIN DimTime ON FactCovidData.TimeID = DimTime.TimeID
JOIN DimLocation ON FactCovidData.LocationID = DimLocation.LocationID

WHERE Country = 'Australia'
	AND Year = 2020