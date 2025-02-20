import sqlite3


conn = sqlite3.connect('database.db')


cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS plates (
    plate_number TEXT PRIMARY KEY
)
''')


plate_number = '45DNM123'
cursor.execute("INSERT INTO plates (plate_number) VALUES (?)", (plate_number,))


conn.commit()


conn.close()
