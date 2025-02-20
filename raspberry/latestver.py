import asyncio
import aiosqlite
import serial
import time
import cv2
import pytesseract
import time as pytime

# Serial Port Settings
SERIAL_PORT = "/dev/ttyUSB0"  # Change to "/dev/ttyACM0" if needed
BAUD_RATE = 9600

# Open Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

distance_history = []  # Store the last 3 distance readings
is_reading = True  # Flag to control distance reading
last_stable_time = 0

# Establish Serial Connection
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(3)
except serial.SerialException as e:
    print(f"Serial port error: {e}")
    exit()

async def process_image(image_path):
    img = cv2.imread(image_path)
    roi = img[300:480, 0:640]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang="eng", config=r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6").strip()
    print('Detected plate:', text)
    await check_plate(text)
    cv2.destroyAllWindows()

async def check_plate(plate_number):
    global is_reading, distance_history
    is_reading = False  # Stop distance reading
    distance_history.clear()  # Clear old distances

    async with aiosqlite.connect('database.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM plates WHERE plate_number = ?", (plate_number,))
            result = await cursor.fetchone()

            if result:
                print(f"Plate {plate_number} exists in the database.")
                await send_to_arduino(b'3', 3)
            else:
                print(f"Plate {plate_number} not found in the database.")
                await send_to_arduino(b'2', 3)

    is_reading = True  # Resume distance reading

async def send_to_arduino(command, sleep_time):
    arduino.write(command)
    await asyncio.sleep(sleep_time)

async def read_distance():
    global distance_history, last_stable_time, is_reading
    while True:
        if is_reading:
            arduino.reset_input_buffer()  # Clear buffer
            distance_str = arduino.readline().decode("utf-8").strip()
            if distance_str:
                try:
                    distance = float(distance_str)
                    if len(distance_history) > 1 and distance == distance_history[-1]:
                        continue  # Ignore duplicate values
                    if 31 <= distance <= 35:
                        await send_to_arduino(b'1', 0.1)
                    else:
                        await send_to_arduino(b'0', 0.1)
                    
                    distance_history.append(distance)
                    if len(distance_history) > 3:
                        distance_history.pop(0)
                    
                    print(f"Distance added: {distance}")
                    await asyncio.sleep(0.33)
                except ValueError:
                    continue

        if len(distance_history) == 3:
            avg = sum(distance_history) / 3
            diffs = sum(abs(distance_history[i] - distance_history[i-1]) for i in range(1, 3))
            if diffs <= 5 and 31 <= avg <= 35:
                current_time = pytime.time()
                if current_time - last_stable_time > 5:
                    print("Stable data detected, capturing photo...")
                    last_stable_time = current_time
                    ret, frame = cap.read()
                    if ret:
                        filename = "captured_image.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"Photo saved as {filename}")
                        await process_image(filename)

async def main():
    await asyncio.gather(read_distance())

asyncio.run(main())
