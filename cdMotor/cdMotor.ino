int wait = 10;
int p1 = 3;
int p2 = 4;
int p3 = 5;

unsigned long discoTime = 20; // in seconds
int count = (discoTime * 1000) / (6 * wait);

void setup() {
  pinMode(p1, OUTPUT);
  pinMode(p2, OUTPUT);
  pinMode(p3, OUTPUT);
  
  Serial.begin(9600);
  
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

// the loop routine runs over and over again forever:
void loop() {
  if(Serial.available() && Serial.parseInt() > 0) {
    digitalWrite(13, HIGH);
    for(int i = 0; i < count; i++) {
      digitalWrite(p1, 1);
      digitalWrite(p2, 1);
      digitalWrite(p3, 0);
      delay(wait);
      digitalWrite(p1, 1);
      digitalWrite(p2, 0);
      digitalWrite(p3, 0);
      delay(wait);
      digitalWrite(p1, 1);
      digitalWrite(p2, 0);
      digitalWrite(p3, 1);
      delay(wait);
      digitalWrite(p1, 0);
      digitalWrite(p2, 0);
      digitalWrite(p3, 1);
      delay(wait);
      digitalWrite(p1, 0);
      digitalWrite(p2, 1);
      digitalWrite(p3, 1);
      delay(wait);
      digitalWrite(p1, 0);
      digitalWrite(p2, 1);
      digitalWrite(p3, 0);
      delay(wait);
    }
    digitalWrite(p1, 0);
    digitalWrite(p2, 0);
    digitalWrite(p3, 0);
    digitalWrite(13, LOW);
  }
}
