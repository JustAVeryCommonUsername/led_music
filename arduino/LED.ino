#define RED D4
#define GREEN D2
#define BLUE D3

int r = 0, g = 0, b = 0;

void setup() {
  Serial.begin(115200);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
}

void loop() {
  if (Serial.available() >= 3) {
    r = Serial.read();
    g = Serial.read();
    b = Serial.read();

    analogWrite(RED, r);
    analogWrite(GREEN, g);
    analogWrite(BLUE, b);
  }
}