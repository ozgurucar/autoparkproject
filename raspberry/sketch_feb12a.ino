#define BLED_PIN 13
#define YLED_PIN 12
#define RLED_PIN 8
#define TRIG_PIN 9
#define ECHO_PIN 10
int ledstate = -1;

void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(YLED_PIN, OUTPUT);
    pinMode(RLED_PIN, OUTPUT);
    pinMode(BLED_PIN, OUTPUT);
    
   
}

void loop() {
    // Ultrasonic sensor distance measurement
    long duration;
    float distance;

    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    duration = pulseIn(ECHO_PIN, HIGH);
    distance = duration * 0.034 / 2;

    Serial.println(distance);  // Send distance to Python
    delay(500);  // Wait for data transmission

    if (Serial.available() > 0) {  // Check if data is received from Python
        char command = Serial.read();  // Read the command
        if (command == '1') {  // Turn on LED if command is '1'
            ledstate = 1;
        } else if(command == '2'){
            ledstate = 2;  // Turn off LED
        } else if(command == '3'){
            ledstate = 3;  // Turn off LED
        }
        
    }

    // Control the LED based on the state
    if (ledstate == 1) {
        digitalWrite(BLED_PIN, LOW);
        digitalWrite(YLED_PIN, HIGH);
        digitalWrite(RLED_PIN, LOW);
    } else if(ledstate == 2){
        digitalWrite(BLED_PIN, LOW);
        digitalWrite(RLED_PIN, HIGH);
        digitalWrite(YLED_PIN, LOW);
    }
    else if(ledstate == 3){
        digitalWrite(BLED_PIN, HIGH);
        digitalWrite(RLED_PIN, HIGH);
        digitalWrite(YLED_PIN, LOW);
    } else {
      digitalWrite(BLED_PIN, LOW);
      digitalWrite(YLED_PIN, LOW);
      digitalWrite(RLED_PIN, LOW);
    }
}
