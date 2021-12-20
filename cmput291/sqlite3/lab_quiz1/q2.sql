SELECT AVG(Suites.price)
FROM Apartments, Suites
WHERE Suites.aID = Apartments.aID 
      AND Apartments.address = 'Whyte Ave'
      AND Suites.type = '2 bedrooms';