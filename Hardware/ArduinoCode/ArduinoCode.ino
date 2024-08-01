int relayPin = 7; // Pin where the relay is connected
int state = LOW;  // Initial state of the relay

void setup() {
  pinMode(relayPin, OUTPUT); // Set the relay pin as an output
  digitalWrite(relayPin, state); // Initialize the relay to the initial state
  Serial.begin(9600); // Start the serial communication at 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) { // Check if there is any data available on the serial port
    char command = Serial.read(); // Read the incoming data

    if (command == 't') { // If the command is 't', toggle the relay
      state = !state; // Toggle the state
      digitalWrite(relayPin, state); // Write the new state to the relay pin
    }
  }
}
