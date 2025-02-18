import cv2
import pytesseract

# Tesseract yolu ayarı
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Kamerayı aç
cap = cv2.VideoCapture(1)  # Harici kamera için doğru indeks

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera açılmadı!")
        break

    # Görüntüyü gri tona çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Adaptif eşikleme (yalnızca siyah yazıları almak için)
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 8
    )

    # Gürültüyü azaltmak için morfolojik işlemler (dilate + erode)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed = cv2.dilate(processed, kernel, iterations=1)
    processed = cv2.erode(processed, kernel, iterations=1)

    # OCR işlemi (sadece harf ve rakamları oku)
    custom_config = r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 --psm 6"
    text = pytesseract.image_to_string(processed, lang="eng", config=custom_config)

    print("Okunan veri:", text.strip())

    # Görüntüyü göster
    cv2.imshow("Camera", frame)
    cv2.imshow("Processed", processed)

    # Çıkış için 'q' tuşuna bas
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
