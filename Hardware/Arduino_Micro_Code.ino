// Photodiode code adapted from http://startrobotics.blogspot.com/2013/05/how-to-use-ir-led-and-photodiode-with-arduino.html
// Serial connection code adapted from https://thepoorengineer.com/en/arduino-python-plot/#python

// --Global constants--
int baud_rate = 38400;
long loopTime = 5000;    // Number of microseconds between readings
// The 'loopTime' value is arbitrary so we can change it, but it shouldn't be larger than 16383 for accuracy reasons

// Photodiodes are connected to the following digital pins:
int PEA_diode_pin = 2;

// Voltage levels are read from the following analog pins:
int PEA_voltage_pin = A0;


// --Global variables--
unsigned long timer = 0;


// --Main code--
void setup() {
  // Set photodiode pin modes to OUTPUT
  pinMode(PEA_diode_pin, OUTPUT);

  // Supply 5V to photodiodes
  digitalWrite(PEA_diode_pin, HIGH);

  Serial.begin(baud_rate);
  timer = micros(); // Set 'timer' to the number of microseconds since the Arduino board began running the program

  // If we need to wait for the software to finish setting up, insert a delay here
  
  // If a handshake is needed, insert it here:
  // Serial.write(-1);
}

void loop() {
  timeSync(loopTime);

  // Read voltage (range: 0V to 5V) and map it to an integer value (range: 0 to 1023)
  int PEA_voltage_reading = analogRead(PEA_voltage_pin);

  // We can probably just use Serial.write(PEA_voltage) to send it to the PC but this
  // requires more experimentation just in case we lose data when the values are too large/small
  sendToPC(&PEA_voltage_reading);

  // Print to serial monitor for debugging (remove later)
  Serial.println(PEA_voltage_reading);
}


// --Helper functions--
void timeSync(unsigned long deltaT) {
  unsigned long currTime = micros();
  long timeToDelay = deltaT - (currTime - timer);
  if (timeToDelay > 5000) {
    delay(timeToDelay / 1000);
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0) {
    delayMicroseconds(timeToDelay);
  }
  else {
    // timeToDelay is negative so we start immediately
  }
  timer = currTime + timeToDelay;
}

void sendToPC(int* data) {
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 2);
}
