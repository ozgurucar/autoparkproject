import cv2
import pytesseract
import serial
import time
import aiosqlite
import asyncio

# Tesseract'ın yolunu belirle
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
distance_history = []  # Mesafeyi saklayacak liste (en son 3 okuma)

def process_image(image_path):
    # Görüntü işleme (örnek olarak, resmi okuyup gösteriyoruz)
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Görüntü işleme işlemi burada yapılabilir.
    # Örneğin, kenar algılama, yüz tanıma vb. işlemleri ekleyebilirsiniz.
    # Görüntüyü gri tona çevir

    # OCR işlemi
    text = pytesseract.image_to_string(gray, lang="tur")
    print('Okunan veri: ' + text)
    asyncio.run(check_plate(text.strip()))
    if(str(text).strip().lower() == 'kablo'):
        arduino.write(b'1')
        cv2.imshow("Processed Image", gray)

    else:
        arduino.write(b'0')

    cv2.waitKey(0)
    cv2.destroyAllWindows()


async def check_plate(plate_number):
    # Veritabanına bağlan (asenkron)
    async with aiosqlite.connect('database.db') as conn:
        async with conn.cursor() as cursor:
            # SQL sorgusunu yaz
            query = "SELECT * FROM plates WHERE plate_number = ?"

            # Sorguyu çalıştır
            await cursor.execute(query, (plate_number,))

            # Sonucu al
            result = await cursor.fetchone()

            # Sonuç kontrolü
            if result:
                print(f"Plaka numarası {plate_number} veritabanında mevcut.")
                arduino.write(b'1')
            else:
                print(f"Plaka numarası {plate_number} veritabanında bulunamadı.")

arduino = serial.Serial('COM4', 9600)
time.sleep(2)  # Arduino'nun başlatılmasını beklemek için 2 saniye bekle

# Kamerayı başlat
cap = cv2.VideoCapture(0)

while True:
    distance = arduino.readline().decode('utf-8').strip()  # Mesafeyi oku
    # Geçerli mesafeyi listeye ekle
    distance_history.append(int(distance))

    # Liste sadece son 3 ölçümü tutar
    if len(distance_history) > 3:
        distance_history.pop(0)

    # Son üç ölçüm arasındaki farkı kontrol et
    if len(distance_history) == 3:
        diff1 = abs(distance_history[1] - distance_history[0])
        diff2 = abs(distance_history[2] - distance_history[1])
        diff3 = abs(distance_history[2] - distance_history[0])
        avg = (distance_history[0] + distance_history[1] + distance_history[2]) / 3
        if (diff1 + diff2 + diff3 <= 3 and avg < 20):
            print("Veri istikrarlı, fotoğraf çekiliyor...")
            ret, frame = cap.read()  # Bir kare al

            if ret:
                # Fotoğrafı kaydet
                filename = "captured_image.jpg"
                cv2.imwrite(filename, frame)
                print(f"Fotoğraf {filename} olarak kaydedildi.")

            # Kamera kaynağını serbest bırak
            cap.release()
            break

process_image("captured_image.jpg")




#     print("Tespit Edilen Metin:", text)
#     print(f"Ultrasonik sensörden gelen mesafe: {distance} cm")  # Mesafeyi yazdır
#
#
#     # Görüntüyü göster
#     cv2.imshow("Kamera - OCR", gray)
#
#     # 'q' tuşuna basılırsa çık
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

