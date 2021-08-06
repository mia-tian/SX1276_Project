#include <Arduino.h>

struct Serial_Info{
  char txrx[2]{};
  int packet{};
  int reg{};
  int value{};
};

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
}

// void loop() {

//   while (!Serial.available());
//   String x = Serial.readString();
//   if(x.substring(0,2) == "wr")
//   {
//     String reg_string = x.substring(2, 6);
//     int reg = std::stoi(reg_string, 0, 16);
//     std::cout<<"reg: "<<reg<<std::endl;

//     String value_string = x.substring(6,13);
//     int value = std::stoi(value_string, 0, 2);
//     std::cout<<"value: "<<value<<std::endl;
//   }
//   else{
//     Serial.print(x);
//   }
// }

void loop(){
  while (!Serial.available());
  byte incoming_byte[1];
  Serial.readBytes(incoming_byte, 1);
  Serial_Info serial_info = incoming_byte[0];
  Serial.print(serial_info.reg);
  Serial.print(serial_info.value);
  
}