SELECT C.email, P.store, COUNT(*) AS numPurchases
FROM (Purchase P JOIN CustomerPurchases X 
				 ON P.id = X.purchaseID)
                 JOIN Customer C
                 ON X.customerID = C.id
GROUP BY C.email, P.store
WITH ROLLUP;