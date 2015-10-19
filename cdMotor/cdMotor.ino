unsigned long wait = 10;
unsigned long invLoopScale = 6UL * wait;
int p1 = 3;
int p2 = 4;
int p3 = 5;

unsigned long count = 0;

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
  if(Serial.available()) {
    unsigned long dTime = Serial.parseInt();
    if(dTime > 0) {
      count = dTime / invLoopScale * 1000UL;
    } else {
      return;
    }
    Serial.print(count);
    
    digitalWrite(13, HIGH);
    for(unsigned long l = 0; l < count; l++) {
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
