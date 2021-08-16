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

void loop() {

  while (!Serial.available());
  String input_string = Serial.readString();

  if(input_string.substring(0,2) == "wr"){
    
    char input[input_string.length()];
    input_string.toCharArray(input, input_string.length());
    char* code = strtok(input, " ");
    char* reg_str = strtok(NULL," ");
    char* val_str = strtok(NULL, " ");

    int reg = String(reg_str).toInt();
    int val = String(val_str).toInt();

    Serial.print("|");
    Serial.print(code);
    Serial.print("|");
    Serial.print(reg);
    Serial.print("|");
    Serial.print(val);
    Serial.print("|");
  }
  else{
    Serial.print(input_string);
  }
  
}

// void loop(){

//   byte packet_length = 0x00;
//   const int buffer_size = 12;
//   byte buf[buffer_size];

//   while (!Serial.available());
  
//   packet_length = Serial.readBytes(buf, buffer_size);
//   for (int i = 0; i < packet_length; i++) {
//     for(int j = 7 ; j >= 0 ; j--){
//       Serial.print(bitRead(buf[i], j));
      
//     }
//     Serial.print(" ");
//     //Serial.print(char(buf[i]));
//   }
//   // char code[2] = (char[]) buf[0];
//   // Serial.print(code);
//   // Serial.print(" ");
//   int reg = (int) buf[4];
//   Serial.print(reg);
//   Serial.print(" ");
//   int val = (int) buf[8];
//   Serial.print(val);
//   Serial.print(" end of loop | ");
//   // String incoming = Serial.readString();
//   // Serial.print(incoming, BIN);
//   // byte incoming_byte[1];
//   // Serial.readBytes(incoming_byte, 1);
//   // Serial.print(incoming_byte);
  
// }