SELECT name
FROM Scoop 
WHERE costInCents = (SELECT MAX(costInCents)
                     FROM Scoop);