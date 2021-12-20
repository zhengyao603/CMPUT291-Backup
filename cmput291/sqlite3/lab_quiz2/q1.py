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


p_name = input("Enter a product name: ")
cursor.execute(''' SELECT name
	               FROM (SELECT Persons.name
	                     FROM Persons
	                     EXCEPT
	                     SELECT Persons.name
	                     FROM Persons, Product, Orders
	                     WHERE Persons.personID = Orders.personID
	                           AND Product.productID = orders.productID
	                           AND Product.name = ?)
	               ORDER BY name;
	           ''', (p_name,))
result = cursor.fetchall()
connection.commit()
for row in result:
	print(row[0])

connection.close()