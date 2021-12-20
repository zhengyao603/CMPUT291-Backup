SELECT Apartments.aID, Apartments.address
FROM Apartments, Suites, Tenants
WHERE Apartments.aID = Suites.aID
      AND Tenants.sID = Suites.sID
      AND Suites.unitNumber >= 200
      AND Suites.unitNUmber < 300
      AND Tenants.yearOfOccup >= 2000