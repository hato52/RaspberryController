import sqlite3

connection = sqlite3.connect("/home/pi/PythonProjects/RaspberryController/signal.db")
c = connection.cursor()
    
data = "test"
id = "asgdhfaslkaa"
json_data = "asdfasdfasdfaaaaa"

#c.execute("SELECT * FROM signals WHERE id = ?", (data,))
try:
    c.execute('INSERT INTO signals VALUES (?,?)', (id, json_data))
except sqlite3.Error as e:
    print(e)
    
connection.commit()

print("success")

for row in c.execute("SELECT * FROM signals"):
    print(row)
    
connection.close()