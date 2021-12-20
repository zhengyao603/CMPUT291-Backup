DROP TABLE IF EXISTS Apartments;
DROP TABLE IF EXISTS Suites;
DROP TABLE IF EXISTS Tenants;

PRAGMA foreign_keys = ON;

CREATE TABLE Apartments (
  aID	INTEGER,
  address	TEXT,
  numberOfSuites  INTEGER,
  builtYear	INTEGER,
  PRIMARY KEY (aID)
);

CREATE TABLE Suites (
  sID     INTEGER,
  type     TEXT,
  unitNumber     INTEGER,
  price INTEGER,
  aID      INTEGER,
  PRIMARY KEY (sID),
  FOREIGN KEY (aID) REFERENCES Apartments
);

CREATE TABLE Tenants (
  tID    INTEGER,
  name     TEXT,
  yearOfOccup INTEGER,
  sID     INTEGER,
  PRIMARY KEY (tID),
  FOREIGN KEY (sID) REFERENCES Suites
);

-- Apartments
INSERT INTO Apartments VALUES (0, 'Whyte Ave', 10, 1980);
INSERT INTO Apartments VALUES (1, 'Whyte Ave', 6, 1985);
INSERT INTO Apartments VALUES (2, 'Jasper Ave', 8, 1975);

-- Suites
INSERT INTO Suites VALUES (0, '2 bedrooms', 101, 1100 , 0);
INSERT INTO Suites VALUES (1, '1 bedroom', 102, 900 , 0);
INSERT INTO Suites VALUES (2, '1 bedrooms', 103, 900 , 0);
INSERT INTO Suites VALUES (3, '1 bedrooms', 104, 900 , 0);
INSERT INTO Suites VALUES (4, '2 bedrooms', 105, 1100 , 0);
INSERT INTO Suites VALUES (5, '2 bedrooms', 201, 1200 , 0);
INSERT INTO Suites VALUES (6, '2 bedrooms', 202, 1200 , 0);
INSERT INTO Suites VALUES (7, '1 bedroom', 203, 1100 , 0);
INSERT INTO Suites VALUES (8, '1 bedroom', 204, 1100 , 0);
INSERT INTO Suites VALUES (9, '2 bedrooms', 205, 1200 , 0);

INSERT INTO Suites VALUES (10, '2 bedrooms', 101, 1150 , 1);
INSERT INTO Suites VALUES (11, 'bachelor', 102, 850 , 1);
INSERT INTO Suites VALUES (12, '1 bedrooms', 201, 1200 , 1);
INSERT INTO Suites VALUES (13, '1 bedrooms', 202, 1200 , 1);
INSERT INTO Suites VALUES (14, 'bachelor', 301, 1000 , 1);
INSERT INTO Suites VALUES (15, 'bachelor', 302, 1000 , 1);

INSERT INTO Suites VALUES (16, '2 bedrooms', 101, 1300 , 2);
INSERT INTO Suites VALUES (17, 'bachelor', 102, 950 , 2);
INSERT INTO Suites VALUES (18, '1 bedrooms', 201, 1200 , 2);
INSERT INTO Suites VALUES (19, '1 bedrooms', 202, 1200 , 2);
INSERT INTO Suites VALUES (20, 'bachelor', 301, 1000 , 2);
INSERT INTO Suites VALUES (21, '1 bedroom', 302, 1200 , 2);
INSERT INTO Suites VALUES (22, '2 bedrooms', 401, 1300 , 2);
INSERT INTO Suites VALUES (23, 'bachelor', 402, 1050 , 2);

-- Tenants
INSERT INTO Tenants VALUES (0, 'McDavid', 2004, 0);
INSERT INTO Tenants VALUES (1, 'Neal', 2002, 1);
INSERT INTO Tenants VALUES (2, 'Bear', 2000, 3);
INSERT INTO Tenants VALUES (3, 'Smith', 2000, 4);
INSERT INTO Tenants VALUES (4, 'Hopkins', 2001, 7);
INSERT INTO Tenants VALUES (5, 'Kassian', 1998, 9);

INSERT INTO Tenants VALUES (6, 'Yamamto', 2003, 10);
INSERT INTO Tenants VALUES (7, 'Bouchard', 2001, 11);
INSERT INTO Tenants VALUES (8, 'Graunlund', 1996, 12);
INSERT INTO Tenants VALUES (9, 'Haas', 1999, 13);
INSERT INTO Tenants VALUES (10, 'Sheahan', 2000, 14);
INSERT INTO Tenants VALUES (11, 'Koshinen', 2004, 15);

INSERT INTO Tenants VALUES (12, 'Persson', 2000, 16);
INSERT INTO Tenants VALUES (13, 'Khaira', 2003, 18);
INSERT INTO Tenants VALUES (14, 'Archibald', 1995, 20);
INSERT INTO Tenants VALUES (15, 'Chiasson', 2005, 21);
INSERT INTO Tenants VALUES (16, 'Russel', 2002, 23);

