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

cursor.execute('SELECT * from Product;')
print ("name of the first column: " + cursor.description[0][0])