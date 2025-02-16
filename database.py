import sqlite3

# Veritabanına bağlan
conn = sqlite3.connect('database.db')

# Cursor (imleç) oluştur
cursor = conn.cursor()

# Plates adında bir tablo oluştur (plate_number primary key olacak)
cursor.execute('''
CREATE TABLE IF NOT EXISTS plates (
    plate_number TEXT PRIMARY KEY
)
''')

# Plates tablosuna bir plaka numarası ekleyelim
plate_number = '34ABC123'
cursor.execute("INSERT INTO plates (plate_number) VALUES (?)", (plate_number,))

# Değişiklikleri kaydet
conn.commit()

# Bağlantıyı kapat
conn.close()
