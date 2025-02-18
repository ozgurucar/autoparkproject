import asyncio
import aiosqlite
import serial
import time
import cv2
import pytesseract

# Seri Port Ayarları
SERIAL_PORT = "COM9"  # Windows için
BAUD_RATE = 9600

# Tesseract OCR Yolu (Windows için)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
distance_history = []  # Mesafeyi saklayacak liste (en son 3 okuma)
# Kamera Aç
cap = cv2.VideoCapture(1)  # Harici kamera için doğru indeks

def process_image(image_path):
    # Görüntü işleme (örnek olarak, resmi okuyup gösteriyoruz)
    img = cv2.imread(image_path)

    # Görüntü işleme işlemi burada yapılabilir.
    # Örneğin, kenar algılama, yüz tanıma vb. işlemleri ekleyebilirsiniz.
    # Görüntüyü gri tona çevir

    # 📏 Koordinatları belirle (Yukarıdan aşağıya ve soldan sağa)
    x_start, x_end = 0, 640   # Genişlik (Width) -> Sütunlar
    y_start, y_end = 300, 480   # Yükseklik (Height) -> Satırlar

    # 📸 Görüntünün belirli bir kısmını kırp (ROI - Region of Interest)
    roi = img[y_start:y_end, x_start:x_end]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # 🏷️ OCR ile Metin Okuma
    custom_config = r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6"
    text = pytesseract.image_to_string(gray, lang="eng", config=custom_config)

    # OCR işlemi
    # text = pytesseract.image_to_string(roi, lang="tur")
    print('Okunan veri: ' + text)
    asyncio.run(check_plate(text.strip()))


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

# Arduino ile Bağlantıyı Başlat
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(3)  # Bağlantının başlaması için bekleme
except serial.SerialException as e:
    print(f"Seri port hatası: {e}")
    exit()

while True:
    # 📷 Kamera Görüntüsünü Oku
    ret, frame = cap.read(1)
    if not ret:
        print("Kamera açılmadı!")
        break

    # 📡 Mesafe Verisini Al
    mesafe_str = arduino.readline().decode("utf-8").strip()

    distance_history.append(float(mesafe_str))

    # Liste sadece son 3 ölçümü tutar
    if len(distance_history) > 3:
        distance_history.pop(0)

            # try:
            #     mesafe = float(mesafe_str)  # Mesafeyi float'a çevir
            #
            #     # 🟢 Durumları Belirle
            #     if 0 <= mesafe < 10:
            #         state = "state1"
            #     elif 10 <= mesafe < 20:
            #         state = "state2"
            #     elif 20 <= mesafe < 30:
            #         state = str(mesafe)
            #     else:
            #         state = "Arac bekleniyor"
            #
            #     print(f"Mesafe: {mesafe} cm, Durum: {state}")
            #
            #     # 🔄 Durumu Arduino'ya Gönder
            #     arduino.write(state.encode() + b'\n')




    # Son üç ölçüm arasındaki farkı kontrol et
    if len(distance_history) == 3:
        diff1 = abs(distance_history[1] - distance_history[0])
        diff2 = abs(distance_history[2] - distance_history[1])
        diff3 = abs(distance_history[2] - distance_history[0])
        avg = (distance_history[0] + distance_history[1] + distance_history[2]) / 3
        if (diff1 + diff2 + diff3 <= 3 and (avg > 30.5 and avg < 35)):
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

#     # 📺 Kırpılmış Görüntüyü Göster
#     cv2.imshow("Original", frame)
#     cv2.imshow("Cropped ROI", roi)
#
#     # 🖼️ Görüntü İşleme
#     gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#
#     # Adaptif Eşikleme (Yazıları Daha Net Almak İçin)
#     processed = cv2.adaptiveThreshold(
#         gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 8
#     )
#
#     # # Gürültü Azaltma (Dilate + Erode)
#     # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#     # processed = cv2.dilate(processed, kernel, iterations=1)
#     # processed = cv2.erode(processed, kernel, iterations=1)
#
#     # 🏷️ OCR ile Metin Okuma
#     custom_config = r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6"
#     text = pytesseract.image_to_string(gray, lang="eng", config=custom_config)
#
#     print("Okunan veri:", text.strip())
#
#     # 📺 Görüntüleri Göster
#     # cv2.imshow("Camera", frame)
#     # cv2.imshow("Processed", gray)
#
#
#     # Çıkış için 'q' tuşuna bas
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
#
# # 🚪 Kaynakları Serbest Bırak
# cap.release()
# cv2.destroyAllWindows()
# arduino.close()
