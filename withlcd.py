import serial
import time
import cv2
import pytesseract

# Seri Port Ayarları
SERIAL_PORT = "COM9"  # Windows için
BAUD_RATE = 9600

# Tesseract OCR Yolu (Windows için)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Kamera Aç
cap = cv2.VideoCapture(1)  # Harici kamera için doğru indeks


# Arduino ile Bağlantıyı Başlat
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(3)  # Bağlantının başlaması için bekleme
except serial.SerialException as e:
    print(f"Seri port hatası: {e}")
    exit()

while True:
    # 📷 Kamera Görüntüsünü Oku
    ret, frame = cap.read()
    if not ret:
        print("Kamera açılmadı!")
        break

    # 📡 Mesafe Verisini Al
    if arduino.in_waiting > 0:
        mesafe_str = arduino.readline().decode("utf-8").strip()

        if mesafe_str:
            try:
                mesafe = float(mesafe_str)  # Mesafeyi float'a çevir

                # 🟢 Durumları Belirle
                if 0 <= mesafe < 10:
                    state = "state1"
                elif 10 <= mesafe < 20:
                    state = "state2"
                elif 20 <= mesafe < 30:
                    state = str(mesafe)
                else:
                    state = "Arac bekleniyor"

                print(f"Mesafe: {mesafe} cm, Durum: {state}")

                # 🔄 Durumu Arduino'ya Gönder
                arduino.write(state.encode() + b'\n')

            except ValueError:
                print("Geçersiz veri alındı.")

    # 📏 Koordinatları belirle (Yukarıdan aşağıya ve soldan sağa)
    x_start, x_end = 0, 640   # Genişlik (Width) -> Sütunlar
    y_start, y_end = 300, 480   # Yükseklik (Height) -> Satırlar

    # 📸 Görüntünün belirli bir kısmını kırp (ROI - Region of Interest)
    roi = frame[y_start:y_end, x_start:x_end]

    # 📺 Kırpılmış Görüntüyü Göster
    cv2.imshow("Original", frame)
    cv2.imshow("Cropped ROI", roi)

    # 🖼️ Görüntü İşleme
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Adaptif Eşikleme (Yazıları Daha Net Almak İçin)
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 8
    )

    # Gürültü Azaltma (Dilate + Erode)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed = cv2.dilate(processed, kernel, iterations=1)
    processed = cv2.erode(processed, kernel, iterations=1)

    # 🏷️ OCR ile Metin Okuma
    custom_config = r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6"
    text = pytesseract.image_to_string(gray, lang="eng", config=custom_config)

    print("Okunan veri:", text.strip())

    # 📺 Görüntüleri Göster
    cv2.imshow("Camera", frame)
    cv2.imshow("Processed", gray)


    # Çıkış için 'q' tuşuna bas
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 🚪 Kaynakları Serbest Bırak
cap.release()
cv2.destroyAllWindows()
arduino.close()
