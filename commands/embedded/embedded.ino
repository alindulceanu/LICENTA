#include <Servo.h>
//#include <HCSR04.h>

//HCSR04 hc(44, 45);

Servo myservo;

const int velocity = 2;
const int forward = 43;
const int backward = 42;
const int direction = 3;

void setup() {
  pinMode(velocity, OUTPUT);
  pinMode(forward, OUTPUT);
  pinMode(backward, OUTPUT);
  pinMode(direction, OUTPUT);  
    
  myservo.attach(direction);
  Serial.begin(115200);
  Serial.println("Hello!");
}

double calculateDistance(){
  
}

void move(String com, int val = 0){
  if (com == "dc"){
    if (val < 0){
      Serial.println("backward!");
      digitalWrite(forward, 0);
      digitalWrite(backward, 1);
    }

    else if (val > 0){
      Serial.println("forward!");
      digitalWrite(forward, 1);
      digitalWrite(backward, 0);
    }
    if (val != 0){
      val = map(abs(val), 0, 30, 20, 50);      
    }
    
    if (val >= 50){
      val = 50;
    }
    analogWrite(velocity, val);
  }

  else if (com == "srv"){
    val = map(val, -50, 50, 57, 123);

    if (val < 57)
      val = 57;
    
    else if (val > 123)
      val = 125;

    myservo.write(val);
  }

  else{
    Serial.println("Wrong command!");
  }

}


void loop() {
  while (Serial.available() == 0){
    //Serial.println(hc.dist());
    //delay(60);
  }

  String com = Serial.readStringUntil('\n');
  String motor = "";
  int value;

  int delimiter = com.indexOf("/");

  if (delimiter != -1){
    motor = com.substring(0, delimiter);
    value = com.substring(delimiter + 1, com.length()).toInt();
  }

  else{
    Serial.println("Wrong command!");
  }

  move(motor, value);

}
