import serial
import time

arduino_port = 'COM3'  
baud_rate = 9600  

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)

def lightOn():
  ser.write(b'o') 

def LightOff():
  ser.write(b'f') 

if __name__ == '__main__':
  try:
    while True: 
      try:
        user_input = input("Enter 'on' to turn the relay ON, 'off' to turn the relay OFF, or 'q' to quit: ").strip().lower()
        if user_input == 'q':
          break
        elif user_input == 'on':
          ser.write(b'o') 
          print("Relay turned ON.")
        elif user_input == 'off':
          ser.write(b'f') 
          print("Relay turned OFF.")
        else:
          print("Invalid input. Please enter 'on', 'off', or 'q'.")
      except serial.SerialTimeoutException:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)
      except KeyboardInterrupt:
        pass
  finally:
    ser.close()
    print("Serial connection closed.")
  ...
# while True:
#   lightOn()
#   time.sleep(2)
#   LightOff()
#   time.sleep(2)