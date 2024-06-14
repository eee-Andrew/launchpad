const int buttonPin1 = 2;
const int buttonPin2 = 3;
const int buttonPin3 = 4;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(buttonPin1) == LOW) {
    Serial.println("BUTTON1_PRESSED");
    delay(500); // Debounce delay
  }
  if (digitalRead(buttonPin2) == LOW) {
    Serial.println("BUTTON2_PRESSED");
    delay(500); // Debounce delay
  }
  if (digitalRead(buttonPin3) == LOW) {
    Serial.println("BUTTON3_PRESSED");
    delay(500); // Debounce delay
  }
}
