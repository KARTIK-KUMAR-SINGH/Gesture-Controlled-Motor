#define bs 10

void setup(){
  Serial.begin(9600);
  pinMode(bs , OUTPUT);
}

void loop(){
  if(Serial.available()){
    int speed = Serial.parseInt();
    if(speed >= 0 && speed <= 255){
      analogWrite(bs , speed);
    }
  }
}