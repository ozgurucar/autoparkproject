//#include <LiquidCrystal.h>
#include <Servo.h>  // Servo kütüphanesini dahil et

Servo myServo;  // Servo nesnesini oluştur

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
    // Ultrasonik sensör ile mesafe ölçümü
    long duration;
    float distance;

    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    duration = pulseIn(ECHO_PIN, HIGH);
    distance = duration * 0.034 / 2;

    Serial.println(distance);  // Mesafeyi Python'a gönder
    delay(500);  // Veri aktarımı için bekleme

  if (Serial.available() > 0) {  // Seri port üzerinden veri geldi mi?
    char command = Serial.read();  // Gelen komutu oku
    if (command == '1') {  // Eğer komut '1' ise LED'i yak
      ledstate = 1; // Pin 13'ü HIGH yap (LED yanar)
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
    myServo.write(90);
    delay(1000);
    myServo.write(0);
    
  }
  else {
    digitalWrite(YLED_PIN, LOW);
    digitalWrite(BLED_PIN, LOW);
    digitalWrite(RLED_PIN, HIGH);
    delay(500);
    digitalWrite(RLED_PIN, LOW);

  } 
   
  }


    // // Python’dan gelen state'i oku
    // if (Serial.available() > 0) {
    //     String state = Serial.readStringUntil('\n');  // Satır sonuna kadar oku
    //     state.trim();  // Boşlukları temizle

    //     lcd.setCursor(0, 1);
    //     lcd.print("                "); // Önceki veriyi temizle
    //     lcd.setCursor(0, 1);
    //     lcd.print(state);  // Ekrana durumu yazdır
    // }

