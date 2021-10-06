
#include <MCP3304.h>
#include <SPI.h>

MCP3304 adc(SS);  //creat an instance with pin 10 as CS

int baud_rate = 9600;
int reading_1;
int reading_2;
float voltage_1;
float voltage_2;
String analyte_1_name = "PEA ";
String analyte_2_name = "mRNA ";

void setup() {

  Serial.begin(baud_rate);
  
}

void loop() {
 
  reading_1 = adc.readAdc(0,1);    //read data from CH0 in SGL mode
  reading_2 = adc.readAdc(1,1);    //read data from CH1 in SGL mode

  voltage_1 = reading_1 / 4095.0 * 5.0;    //convert reading into a voltage from 0 to 5V
  voltage_2 = reading_2 / 4095.0 * 5.0;

  Serial.println(analyte_1_name + (String)(voltage_1));
  Serial.println(analyte_2_name + (String)(voltage_2));
  
  
  delay(100);    //delay for 1s so you dont get to much lines in the serial monitor
}