#include <PinChangeInt.h>
#include <TimerOne.h>

#define PIN1 3 // энкодер тянущего signal C
#define PIN2 4 // брайдер 1 signal A 
#define PIN3 5 // брайдер 2 signal B
#define PIN4 2 // сброс счетчика

int count;
int b1_time_new;
int b1_time_last;
int b1_rpm;
int b2_time_new;
int b2_time_last;
int b2_rpm;
int push_time_new;
int push_time_last;
int push_rpm;
int encoder_100; //счетчик импульсов энкодера. 200 импульсов - 1 оборот 
float count_len; //подсчет длины бухты
byte inByte;

//массивы для сохрания данных для вычисления средней скорости вращения
volatile int b1_rpm_array[5] = {0,0,0,0,0};
volatile int b2_rpm_array[5] = {0,0,0,0,0};
volatile int push_rpm_array[5] = {0,0,0,0,0};

uint8_t latest_interrupted_pin;
uint8_t interrupt_count[20]={0}; // 20 possible arduino pins
void quicfunc() {
  latest_interrupted_pin=PCintPort::arduinoPin;
  interrupt_count[latest_interrupted_pin]++;
};

// Скорость вращения тянущего
void pin1func() {
  encoder_100 = encoder_100 + 1;
  if (encoder_100 >= 100)
    { 
    push_time_new=(millis()-push_time_last);
    push_time_last=millis();
    push_rpm = push_time_new / 10;
    encoder_100 = 0; 
    count_len = count_len + 0.376;
    }
  }
// Скорость вращения первого барабана брайдера
void pin2func() {
  b1_time_new=(millis()-b1_time_last);
  b1_time_last=millis();
//  b1_rpm=b1_time_new;

    b1_rpm_array[0] = b1_rpm_array[1];
    b1_rpm_array[1] = b1_rpm_array[2];
    b1_rpm_array[2] = b1_rpm_array[3];
    b1_rpm_array[3] = b1_rpm_array[4];
    b1_rpm_array[4] = b1_time_new;    
    //Вычисление среднего значения
    b1_rpm = (b1_rpm_array[0] + b1_rpm_array[1] + b1_rpm_array[2] + b1_rpm_array[3] + b1_rpm_array[4]) / 5;
}
// Скорость вращения второго барабана брайдера
void pin3func() {
  b2_time_new=(millis()-b2_time_last);
  b2_time_last=millis();
 // b2_rpm=b2_time_new;
  
    b2_rpm_array[0] = b2_rpm_array[1];
    b2_rpm_array[1] = b2_rpm_array[2];
    b2_rpm_array[2] = b2_rpm_array[3];
    b2_rpm_array[3] = b2_rpm_array[4];
    b2_rpm_array[4] = b2_time_new;    
    //Вычисление среднего значения
    b2_rpm = (b2_rpm_array[0] + b2_rpm_array[1] + b2_rpm_array[2] + b2_rpm_array[3] + b2_rpm_array[4]) / 5;
}

// Сброс счетчика 
void pin4func() {
    count_len = 0;
}

void setup() {
  pinMode(PIN1, INPUT); digitalWrite(PIN1, HIGH);
  PCintPort::attachInterrupt(PIN1, &pin1func, FALLING);  // при изменеии сигнала "0" вызов функции &pin1func
  pinMode(PIN2, INPUT); digitalWrite(PIN2, HIGH);
  PCintPort::attachInterrupt(PIN2, &pin2func, FALLING);
  pinMode(PIN3, INPUT); digitalWrite(PIN3, HIGH);
  PCintPort::attachInterrupt(PIN3, &pin3func, FALLING);
  pinMode(PIN4, INPUT); digitalWrite(PIN4, HIGH);
  PCintPort::attachInterrupt(PIN4, &pin4func, CHANGE);
  
  
  Serial.begin(9600, SERIAL_8E2);
  
}


uint8_t i;

void timerIsr()
{
    // timer
    Serial.print ("c");
    Serial.println(push_rpm * 0.2);
    Serial.print ("a");
    Serial.println(b1_rpm);
    Serial.print ("b");
    Serial.println(b2_rpm);
    Serial.print ("d");
    Serial.println(count_len);
}

void loop() {
  if (Serial.available()) {//Если пришел запрос от компьютера
      inByte = Serial.read();
      if (inByte == 115) {
        Serial.print ("c");
        Serial.println(push_rpm * 0.2);
        Serial.print ("a");
        Serial.println(b1_rpm);
        Serial.print ("b");
        Serial.println(b2_rpm);
        Serial.print ("d");
        Serial.println(count_len);
      }}
  }
