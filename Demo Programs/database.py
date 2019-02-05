import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

""" INTEGER is used for auto incremental purpose"""
create_table = "CREATE TABLE IF NOT EXISTS users (username text, password text UNIQUE)"
cursor.execute(create_table)

query = "INSERT INTO users VALUES(?, ?)"
cursor.execute(query, ('rishi', 'kumar1'))

query = "SELECT rowid from users WHERE password=? "
res = cursor.execute(query, ('kumar1',))
print(res.lastrowid)

connection.commit()
connection.close()