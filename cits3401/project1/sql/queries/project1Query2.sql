-- Query 2
--
-- a) In Sept 2020, how many recovered cases are there in the region of the Americas? 
-- b) How many recovered cases in the United States, Canada and Mexico, respectively, in Sep 2020?


-- a)
SELECT SUM(Recoveries) totalRecovered

FROM FactCovidData
JOIN DimTime ON FactCovidData.TimeID = DimTime.TimeID
JOIN DimLocation ON FactCovidData.LocationID = DimLocation.LocationID

WHERE (Region = 'North America' OR Region = 'South America')
	AND Year = 2020 
	AND Month = 'September'


-- b)
SELECT Country, Month, Year, Recoveries

FROM FactCovidData
JOIN DimTime ON FactCovidData.TimeID = DimTime.TimeID
JOIN DimLocation ON FactCovidData.LocationID = DimLocation.LocationID

WHERE (Country = 'United States' OR Country = 'Canada' OR Country = 'Mexico')
	AND Month = 'September'
	AND Year = '2020'

