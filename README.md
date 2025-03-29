# AutoPark Project
**DEU Internship Project - Autonomous AutoPark with Raspberry Pi and Arduino**

## 🚀 Usage
### Arduino
- This project utilizes an **Arduino UNO**.
- First, upload the `sketch_feb16a` code to the Arduino UNO.
- Connect the required components:
  - **Servo Motor**
  - **LEDs**
  - **Pins Configuration:**
    ```cpp
    int ledPin = 13;  // LED connected to pin 13
    int trigPin = 9;
    int echoPin = 10;
    int ledstate = -1;
    ```

### Raspberry Pi
- We used **Raspberry Pi 4-B**, but any Linux-based computer can be used.
- **Requirements:** Ensure the following libraries are installed:
  - **Tesseract OCR**
  - **OpenCV**
  - **SQLite**

### SQLite Database
- Run the queries in the `Database.py` file before starting the project.

## 🎯 Final Functionality
1. License plates (created using cardboard) are presented to the system.
2. The system recognizes letters using **Tesseract OCR**.
3. It checks the database for plate validity.
4. If the plate exists in the database, the **servo motor operates**, simulating an autonomous parking barrier by opening and closing.

Enjoy building your **autonomous parking system**! 🚗🔧

