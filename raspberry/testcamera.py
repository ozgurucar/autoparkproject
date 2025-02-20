import cv2
import pytesseract
import re  # For regular expression filtering

# Make sure tesseract is correctly installed and set up.
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  # Path where tesseract is installed

cap = cv2.VideoCapture(0) 

# Set camera resolution and FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the camera resolution to 640x480
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 5)  # Set FPS to 5
cap.set(cv2.CAP_PROP_FOCUS, 0)  

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to grayscale for better OCR results
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text
    raw_text = pytesseract.image_to_string(gray, lang="eng")

    # Filter the text to contain only uppercase English letters and digits
    filtered_text = re.sub(r'[^A-Z0-9]', '', raw_text)

    # If the filtered text is not empty, print it
    if filtered_text:
        print("Detected License Plate: ", filtered_text)

    # Display the grayscale image
    cv2.imshow("Camera - OCR", gray)

    # Exit loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
