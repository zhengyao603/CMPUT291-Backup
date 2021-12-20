DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Persons ;
DROP TABLE IF EXISTS Product ;

PRAGMA foreign_keys = ON;

CREATE TABLE Persons (personID INTEGER, name TEXT, gender TEXT, birthDate DATE, PRIMARY KEY (personID));
CREATE TABLE Product (productID INTEGER, name TEXT, price REAL, descption TEXT, PRIMARY KEY (productID));
CREATE TABLE Orders (orderID TEXT, personID INTEGER, productID INTEGER, orderDate DATE, PRIMARY KEY (orderID), FOREIGN KEY (personID) REFERENCES Persons, FOREIGN KEY (productID) REFERENCES Product);


INSERT INTO Persons VALUES (1, "Phil White","Male", "1998-02-20");
INSERT INTO Persons VALUES (2, "Laura Terry","Female", '1992-10-17');
INSERT INTO Persons VALUES (3, "Calvin Simon","Male", '1997-10-02');
INSERT INTO Persons VALUES (4, "Alan Zhang","Male", '1993-04-05');
INSERT INTO Persons VALUES (5, "Zoe Pearson","Female", '1995-07-20');
INSERT INTO Persons VALUES (6, "Rebecca Bennett","Female", '1996-12-03');
INSERT INTO Persons VALUES (7, "Ketti Wong","Female", '1995-01-24');
INSERT INTO Persons VALUES (8, "Juliet Cole","Female", '1999-04-12');
INSERT INTO Persons VALUES (9, "Benjamin James","Male", '1998-02-12');

INSERT INTO Product VALUES (1, "Lipstick", 42, "Cherry Blossom Rouge G Customizable Lipstick");
INSERT INTO Product VALUES (2, "Foundation", 45, "Pro Filt'r Soft Matte Longwear Foundation");
INSERT INTO Product VALUES (3, "Keyboard", 179, "Huntsman Tournament Edition");
INSERT INTO Product VALUES (4, "Controller", 39.46, "Wireless Bluetooth Game Controller");
INSERT INTO Product VALUES (5, "Mouse", 89.98, "Razer Viper Ultralight Ambidextrous Wired Gaming Mouse");
INSERT INTO Product VALUES (6, "Eyeshadow", 86, "The New Nude Eyeshadow Palette");
INSERT INTO Product VALUES (7, "Highlighter", 48, "Killawatt Freestyle Highlighter");
INSERT INTO Product VALUES (8, "Eyeliner", 36, "BOBBI BROWN Long-Wear Gel Eyeliner");
INSERT INTO Product VALUES (9, "Perfume", 122, "Good Girl Eau de Parfum");
INSERT INTO Product VALUES (10, "Steamer", 197, "Pro Facial Steamer");


INSERT INTO Orders VALUES (1, 1, 3, "2019-09-23");
INSERT INTO Orders VALUES (2, 1, 4, "2019-06-01");
INSERT INTO Orders VALUES (3, 2, 1, "2019-10-12");
INSERT INTO Orders VALUES (4, 2, 6, "2018-09-23");
INSERT INTO Orders VALUES (5, 3, 5, "2019-11-01");
INSERT INTO Orders VALUES (6, 3, 3, "2020-02-26");
INSERT INTO Orders VALUES (7, 5, 9, "2018-01-09");
INSERT INTO Orders VALUES (8, 5, 6, "2018-02-21");
INSERT INTO Orders VALUES (9, 6, 10, "2018-09-23");
INSERT INTO Orders VALUES (10, 6, 6, "2020-01-12");
INSERT INTO Orders VALUES (11, 6, 3, "2019-10-24");
INSERT INTO Orders VALUES (12, 7, 6, "2019-05-12");
INSERT INTO Orders VALUES (13, 7, 6, "2020-03-07");
INSERT INTO Orders VALUES (14, 8, 3, "2018-11-12");
INSERT INTO Orders VALUES (15, 8, 6, "2019-11-19");
INSERT INTO Orders VALUES (16, 8, 9, "2016-04-13");
INSERT INTO Orders VALUES (17, 8, 9, "2019-05-01");
INSERT INTO Orders VALUES (18, 9, 5, "2019-12-29");
INSERT INTO Orders VALUES (19, 9, 6, "2018-01-12");
INSERT INTO Orders VALUES (20, 9, 1, "2019-01-10");
INSERT INTO Orders VALUES (21, 9, 1, "2019-10-17");
INSERT INTO Orders VALUES (22, 2, 2, "2019-07-10");
INSERT INTO Orders VALUES (23, 7, 2, "2019-12-30");
INSERT INTO Orders VALUES (24, 5, 2, "2019-02-09");




