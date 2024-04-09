const int buzzerPin = 8; // Change this to the actual pin where your buzzer is connected
bool buzzerOn = false;   // Flag to track the state of the buzzer

void setup() {
  Serial.begin(9600);  // Set the baud rate to match the Python script
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the value sent from Python
    char receivedValue = Serial.read();

    if (receivedValue == '1') {
      // Turn on the buzzer only if it's not already on
      if (!buzzerOn) {
        digitalWrite(buzzerPin, HIGH);
        delay(1000);  // Buzzer on for 1 second
        digitalWrite(buzzerPin, LOW);
        buzzerOn = true;  // Set the flag to indicate the buzzer is on
      }
    } else {
      // Turn off the buzzer only if it's not already off
      if (buzzerOn) {
        digitalWrite(buzzerPin, LOW);
        buzzerOn = false;  // Set the flag to indicate the buzzer is off
      }
    }
  }

  
}
