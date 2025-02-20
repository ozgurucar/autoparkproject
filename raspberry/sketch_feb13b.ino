//#include <LiquidCrystal.h>
#include <Servo.h>  // Servo k�t�phanesini dahil et

Servo myServo;  // Servo nesnesini olu�tur

#define BLED_PIN 13
#define YLED_PIN 12
#define RLED_PIN 8
#define TRIG_PIN 9
#define ECHO_PIN 10
int ledstate = -1;

// LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(YLED_PIN, OUTPUT);
    pinMode(RLED_PIN, OUTPUT);
    pinMode(BLED_PIN, OUTPUT);
    // lcd.begin(16, 2);
    // lcd.setCursor(0, 0);
    // lcd.print("State:");
    myServo.attach(7);
    myServo.write(90);
}

void loop() {
    // Ultrasonik sens�r ile mesafe �l��m�
    long duration;
    float distance;

    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    duration = pulseIn(ECHO_PIN, HIGH);
    distance = duration * 0.034 / 2;

    Serial.println(distance);  // Mesafeyi Python'a g�nder
    delay(500);  // Veri aktar�m� i�in bekleme

  if (Serial.available() > 0) {  // Seri port �zerinden veri geldi mi?
    char command = Serial.read();  // Gelen komutu oku
    if (command == '1') {  // E�er komut '1' ise LED'i yak
      ledstate = 1; // Pin 13'� HIGH yap (LED yanar)
    } else if(command == '2') {
      ledstate = 2;
    } else if(command == '3') {
      ledstate = 3;
    } else {
      ledstate = -1;
    }
   
  }

  if(ledstate == 1){
    digitalWrite(YLED_PIN, HIGH);
    digitalWrite(BLED_PIN, LOW);
    digitalWrite(RLED_PIN, LOW);

  } else if(ledstate == 2) {
    digitalWrite(YLED_PIN, LOW);
    digitalWrite(BLED_PIN, LOW);
    digitalWrite(RLED_PIN, HIGH);
  } else if(ledstate == 3) {
    digitalWrite(RLED_PIN, LOW);
    digitalWrite(YLED_PIN, LOW);
    digitalWrite(BLED_PIN, HIGH);
    myServo.write(180);
    delay(1500);
    myServo.write(0);
    delay(1500);
    myServo.write(90);
    
  }
  else {
    digitalWrite(YLED_PIN, LOW);
    digitalWrite(BLED_PIN, LOW);
    digitalWrite(RLED_PIN, HIGH);
    delay(500);
    digitalWrite(RLED_PIN, LOW);

  } 
   
  }


    // // Python�dan gelen state'i oku
    // if (Serial.available() > 0) {
    //     String state = Serial.readStringUntil('\n');  // Sat�r sonuna kadar oku
    //     state.trim();  // Bo�luklar� temizle

    //     lcd.setCursor(0, 1);
    //     lcd.print("                "); // �nceki veriyi temizle
    //     lcd.setCursor(0, 1);
    //     lcd.print(state);  // Ekrana durumu yazd�r
    // }
