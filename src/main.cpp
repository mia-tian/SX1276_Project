#include <Arduino.h>
#include <SPI.h>

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
/**
 * reads the input as a string
 * input comes in as: "code register value"
 **/
void loop() {

  while (!Serial.available());
  String input_string = Serial.readString();

  Serial.print(input_string);

  if(input_string.substring(0,2) == "wr"){
    
    char input[input_string.length()];
    input_string.toCharArray(input, input_string.length());
    char* code = strtok(input, " ");
    char* reg_str = strtok(NULL," ");
    char* val_str = strtok(NULL, " ");

    int reg_int = String(reg_str).toInt();
    int val_int = String(val_str).toInt();
    byte reg = reg_int;
    byte val = val_int;

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


/**
 * reads the input as bytes using struct packing
 * input comes in as 12 bytes: b'code\x00\x00\x00\register\x00\x00\x00\value\x00\x00\x00
 **/
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
//   }

//   byte reg = buf[4];
//   Serial.print(reg);
//   Serial.print(" ");
//   byte val = buf[8];
//   Serial.print(val);
//   Serial.print(" end of loop | ");
  
//  }