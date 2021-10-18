#include <Arduino.h>
#include <SPI.h>

/*
Arduino script that controls a SX1276 SemTech RF-chip. Takes
commands from SX1276_Interface.py through serial port.
Currently has functionality to take in and decode commands
to write and read registers, and transmit and receive, but
can only write and read registers as of now. 

Every command has format "code message_1 message_2 ... \r"

TODO: integrate functionality to transmit and receive

Output:
prints |loop| each time the loop() function is called
prints entire command sent in through serial port
prints each significant part of command separated by |
prints function it is performing (read, transmit etc)
*/

const int NSS = 10;
byte packet_length = 0x00;
const int buffer_size = 128;
byte buf[buffer_size];

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(5);
}

void writeRegister(byte thisRegister, byte thisValue)
{

  //set wnr bit (A[7]) to 1 for write access
  bitWrite(thisRegister, 7, 1);

  //take the chip select low to select the device
  digitalWrite(NSS, LOW);

  SPI.transfer(thisRegister);
  SPI.transfer(thisValue);

  //take the chip select high to de-select:
  digitalWrite(NSS, HIGH);
}

unsigned int readRegister(byte thisRegister)
{

  unsigned int result = 0; //result to return

  //Serial.print(thisRegister, HEX);
  //Serial.print("\t");

  //set wnr bit (A[7]) to 0 for read access
  bitWrite(thisRegister, 7, 0);
  //Serial.print(thisRegister, BIN);

  //take the chip select low to select the device
  digitalWrite(NSS, LOW);

  //send the device register you want to read
  SPI.transfer(thisRegister);
  result = SPI.transfer(0x00);

  //take the chip select high to de-select
  digitalWrite(NSS, HIGH);

  return (result);
}

void decodeRR(String input_string)
{
  // split by space
  char input[input_string.length()];
  input_string.toCharArray(input, input_string.length());
  char *code = strtok(input, " ");
  char *reg_str = strtok(NULL, " ");

  // convert to bytes
  int reg_int = String(reg_str).toInt();
  byte reg = reg_int;

  Serial.print("|");
  Serial.print(code);
  Serial.print("|");
  Serial.print(reg);
  Serial.print("|\n");

  unsigned int val = 0;
  val = readRegister(reg);

  Serial.print("Register ");
  Serial.print(reg, HEX);
  Serial.print(" has value: ");
  Serial.print(val, BIN);
}

void decodeWR(String input_string)
{

  // split by space
  char input[input_string.length()];
  input_string.toCharArray(input, input_string.length());
  char *code = strtok(input, " ");
  char *reg_str = strtok(NULL, " ");
  char *val_str = strtok(NULL, " ");

  // convert to bytes
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
  Serial.print("|\n");

  Serial.print("Writing Register ");
  Serial.print(reg, HEX);
  Serial.print(" to value: ");
  Serial.print(val, BIN);

  writeRegister(reg, val);
}

void decodeTX(String input_string)
{
  // split by space
  char input[input_string.length()];
  input_string.toCharArray(input, input_string.length());
  char *code = strtok(input, " ");

  String packet = input_string.substring(3, input_string.length() - 1);

  Serial.print("|");
  Serial.print(code);
  Serial.print("|");
  Serial.print(packet);
  Serial.print("|\n");

  Serial.print("Transmitting: ");
  Serial.print(packet);

  //TODO: write and call transmit method
}

void decodeRX(String input_string)
{
  // split by space
  char input[input_string.length()];
  input_string.toCharArray(input, input_string.length());
  char *code = strtok(input, " ");

  Serial.print("|");
  Serial.print(code);
  Serial.print("|\n");

  Serial.print("Receiving ... ");

  //TODO: write and call receive method
}

/**
 * reads the input as a string
 * input comes in as: "code register value \r"
 **/
void loop()
{
  Serial.print("|loop| ");

  while (!Serial.available());
  String input_string = Serial.readStringUntil('\r');
  Serial.print(input_string);

  String code = input_string.substring(0, 2);

  // write register
  if (code == "wr")
  {
    decodeWR(input_string);
  }
  // read register
  else if (code == "rr")
  {
    decodeRR(input_string);
  }
  // transmit
  else if (code == "tx")
  {
    decodeTX(input_string);
  }
  // receive
  else if (code == "rx")
  {
    decodeRX(input_string);
  }
  else{
    Serial.print("Invalid Command");
  }

  Serial.print("\r");
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