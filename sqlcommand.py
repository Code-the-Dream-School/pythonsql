import sys
import sqlite3

print(dir(sqlite3))
print(sqlite3.sqlite_version)
print(sqlite3.sqlite_version_info)
connection = sqlite3.connect("./db/lesson.db",isolation_level='IMMEDIATE')
connection.execute("PRAGMA foreign_keys = 1")
print(dir(connection))

cursor = connection.cursor()
print(dir(cursor))
# raise Exception("stop here")

tables = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY 'name'").fetchall()
print("The tables in this database are:")
for row in tables:
    print(row[0])
print("Enter SQL statements below, ending with a semicolon.  Or, type Ctrl-C to quit.")

line = ""
print("==> ", end = "")
while True:
    line += input()
    if ";" in line:
        try:
            result = cursor.execute(line)
            connection.commit()
            rows = result.fetchall()
            if len(rows) > 0:
                for description in result.description:
                    print(description[0],end="\t")
                print("")
                for row in rows:
                    for column in row:
                        print(str(column), end="\t")
                    print("")
            else:
                print("OK")
        except sqlite3.OperationalError as e:
            print(e)
        line = ""
        print("==> ", end = "")

             

 