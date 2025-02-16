import serial
import time

arduino = serial.Serial('COM4', 9600)
time.sleep(2)  # Arduino'nun başlatılmasını beklemek için 2 saniye bekle

while True:
    if arduino.in_waiting > 0:  # Arduino'dan veri geldiyse
        data = arduino.readline().decode('utf-8').strip()  # Veriyi oku ve temizle
        print(f"Arduino'dan gelen veri: {data}")  # Veriyi ekrana yazdır

print('sanırım baglanmadı')