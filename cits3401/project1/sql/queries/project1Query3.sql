-- Query 3
-- 
-- a) What is the total number of covid deaths worldwide in 2020? 
-- b) What is the total number of covid deaths in large countries, medium countries and small countries, respectively, in 2020?


-- a)
SELECT SUM(Deaths) AS totalDeaths

FROM FactCovidData
JOIN DimTime ON FactCovidData.TimeID = DimTime.TimeID

WHERE Year = 2020


-- b)
SELECT CountrySizeType, SUM(Deaths) AS totalDeaths

FROM FactCovidData
JOIN DimTime ON FactCovidData.TimeID = DimTime.TimeID
JOIN DimCountrySize ON FactCovidData.CountrySizeID = DimCountrySize.CountrySizeID

WHERE Year = 2020

GROUP BY CountrySizeType