SELECT Suites.aID, Suites.unitNumber, Suites.type, Suites.price, Tenants.name
FROM Suites left outer join Tenants using (sID);