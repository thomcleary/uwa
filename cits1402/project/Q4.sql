SELECT customerId, COUNT(*) AS numCones
FROM CustomerPurchases NATURAL JOIN ConesInPurchase
GROUP BY customerId
ORDER BY numCones DESC;