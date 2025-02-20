import cv2
import pytesseract
import time
import re

# Set the path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

def process_image(image_path):
    # Image processing (for example, reading and displaying the image)
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to deal with varying lighting conditions
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Apply median blur to remove noise
    blurred = cv2.medianBlur(binary, 3)

    # Alternative thresholding technique to clean up further
    _, binarized = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # OCR processing - Extract text from the image, limiting to letters and digits
    text = pytesseract.image_to_string(binarized, lang="eng", config='--psm 6')

    # Filter out non-alphanumeric characters
    alphanumeric_text = re.sub(r'[^A-Za-z0-9]', '', text)

    return alphanumeric_text

# Start the camera (optional, depending on how you want to trigger photo capture)
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if ret:
        # Save the captured frame
        filename = "captured_image.jpg"
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(filename, frame)
        print(f"Photo saved as {filename}.")

        # Process the saved image and get alphanumeric text
        alphanumeric_text = process_image(filename)

        # Print the detected alphanumeric text
        if alphanumeric_text:
            print("Detected alphanumeric text:", alphanumeric_text)
        else:
            print("No alphanumeric text detected.")

    time.sleep(1)  # Add a delay to prevent excessive resource usage

cap.release()
cv2.destroyAllWindows()
