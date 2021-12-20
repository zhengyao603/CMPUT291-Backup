import sqlite3

connection = sqlite3.connect("./a2.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


cursor.execute("SELECT * FROM sales;")
row = cursor.fetchone()
print (row.keys())
rows = cursor.fetchall()
for each in rows:
	print (each["sid"], each["lister"])