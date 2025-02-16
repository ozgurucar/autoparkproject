int ledPin = 13;  // LED'in bağlı olduğu pin (Pin 13)
int trigPin = 9;
int echoPin = 10;
int ledstate = -1;

// #include <Servo.h>

// Servo myservo;  // Servo nesnesi oluştur

void setup() {
  pinMode(trigPin, OUTPUT);  // Trig pinini çıkış olarak ayarla
  pinMode(echoPin, INPUT);   // Echo pinini giriş olarak ayarla
  pinMode(ledPin, OUTPUT);  // Pin 13'ü çıkış olarak ayarla
  Serial.begin(9600);  // Seri haberleşmeyi başlat
  // myservo.attach(9);
    digitalWrite(ledPin, LOW);


}

void loop() {
  // myservo.write(0);  // Servo motorunu 0 dereceye döndür
  // delay(1000);  // 1 saniye bekle
  // myservo.write(90);  // Servo motorunu 90 dereceye döndür
  // delay(1000);  // 1 saniye bekle
  // myservo.write(180);  // Servo motorunu 180 dereceye döndür
  // delay(1000);  // 1 saniye bekle


  if (Serial.available() > 0) {  // Seri port üzerinden veri geldi mi?
    char command = Serial.read();  // Gelen komutu oku
    if (command == '1') {  // Eğer komut '1' ise LED'i yak
      ledstate = 1; // Pin 13'ü HIGH yap (LED yanar)
    }
   
  }

   long duration, distance;
  if(ledstate == 1){
    digitalWrite(ledPin, HIGH);
  }
  else {
    digitalWrite(ledPin, LOW);
  } 
  // Trig pinine düşük sinyal gönder
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Trig pinine yüksek sinyal gönder
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Echo pininden süreyi oku
  duration = pulseIn(echoPin, HIGH);

  // Mesafeyi hesapla (ses hızını kullanarak)
  distance = (duration / 2) / 29.1;  // Mesafe cm cinsinden

  // Mesafeyi seri port üzerinden gönder
  Serial.println(distance);

  delay(1000);  // 1 saniye bekle
}