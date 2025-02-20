import cv2
import pytesseract
import serial
import time
import aiosqlite
import asyncio

# Set the path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract" 
distance_history = []  # List to store distance (last 3 readings)

def process_image(image_path):
    # Image processing (for example, reading and displaying the image)
    img = cv2.imread(image_path)

    # Resize the image to 640x480 resolution
    img = cv2.resize(img, (640, 480))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarize the image (convert to black and white) to improve OCR accuracy
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Optionally, apply Gaussian blur to remove noise
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)

    # OCR processing
    text = pytesseract.image_to_string(blurred, lang="eng")
    print('Read data: ' + text)

    # Check the plate number
    if str(text).strip() == '34ABC123':
        arduino.write(b'1')
        cv2.imshow("Processed Image", blurred)

    else:
        arduino.write(b'0')

    cv2.waitKey(0)
    cv2.destroyAllWindows()


async def check_plate(plate_number):
    # Connect to the database (asynchronous)
    async with aiosqlite.connect('database.db') as conn:
        async with conn.cursor() as cursor:
            # Write the SQL query
            query = "SELECT * FROM plates WHERE plate_number = ?"

            # Execute the query
            await cursor.execute(query, (plate_number,))

            # Get the result
            result = await cursor.fetchone()

            # Check the result
            if result:
                print(f"Plate number {plate_number} exists in the database.")
                arduino.write(b'1')
            else:
                print(f"Plate number {plate_number} not found in the database.")
                
def testplate(plate_number):
    if plate_number == '34ABC123':
        arduino.write(b'1')

arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)  # Wait for 2 seconds to let the Arduino initialize

# Start the camera
cap = cv2.VideoCapture(0)

# Set the camera resolution to 640x480
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

while True:
    distance = arduino.readline().decode('utf-8').strip()  # Read the distance
    # Add the current distance to the list
    distance_history.append(int(distance))

    # The list keeps only the last 3 measurements
    if len(distance_history) > 3:
        distance_history.pop(0)

    # Check the difference between the last three measurements
    if len(distance_history) == 3:
        diff1 = abs(distance_history[1] - distance_history[0])
        diff2 = abs(distance_history[2] - distance_history[1])
        diff3 = abs(distance_history[2] - distance_history[0])
        avg = (distance_history[0] + distance_history[1] + distance_history[2]) / 3
        if (diff1 + diff2 + diff3 <= 3 and avg < 20):
            print("Data is stable, taking a photo...")
            ret, frame = cap.read()  # Capture a frame

            if ret:
                # Save the photo
                filename = "captured_image.jpg"
                cv2.imwrite(filename, frame)
                print(f"Photo saved as {filename}.")

            # Release the camera resource
            cap.release()
            break

process_image("captured_image.jpg")
