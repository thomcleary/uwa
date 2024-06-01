SELECT *

FROM FactCovidData
JOIN DimDate ON FactCovidData.DateID = DimDate.DateID
JOIN DimLocation ON FactCovidData.LocationID = DimLocation.LocationID

WHERE Country ='United States'
