import sqlite3
import sys

# Read the name of database
if len(sys.argv) != 2:
    print("Invalid argument! One command line argument is required")
    sys.exit(0)
# Connect to the database
database = str(sys.argv[1])
connection = sqlite3.connect(database)
cursor = connection.cursor()


year = str(input("Enter a year: "))
cursor.execute(''' SELECT Product.productID, Product.name, Product.price, Product.descption
                   FROM Product left outer join Orders using (productID)
                   WHERE strftime('%Y', OrderDate) = ?
                   GROUP BY productID
                   HAVING COUNT(orderID) > 1;
	           ''', (year, ))
result = cursor.fetchall()
connection.commit()

cursor.execute(''' CREATE TABLE ? (
	               productID TEXT,
	               name TEXT,
	               price TEXT,
	               descption TEXT,
	               PRIMARY KEY (productID)
	               ); ''', ('Product_'+ year, ))


cursor.executemany(''' INSERT INTO ?
	                   VALUES (?, ?, ?, ?);
	               ''', ('Product_'+ year, result))
connection.commit()

connection.close()