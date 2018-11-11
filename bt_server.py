import RPi.GPIO as GPIO
import time
from bluetooth import *
import ir_operate

PNO = 4
id = ""

# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO, GPIO.OUT)

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805F9B34FB"

advertise_service(server_sock, "BluetoothServer",
                  service_id = uuid,
                  service_classes = [uuid, SERIAL_PORT_CLASS],
                  profiles = [SERIAL_PORT_PROFILE],
                  )

print("Waiting for connection on RFCOMM channel %d" % port)

GPIO.output(PNO, GPIO.HIGH)
time.sleep(1.0)
GPIO.output(PNO, GPIO.LOW)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        code = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % code)
        GPIO.output(PNO, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(PNO, GPIO.LOW)
        time.sleep(0.3)
except IOError:
    pass

    print("disconnected")

    client_sock.close()
    server_sock.close()
    GPIO.cleanup()
    print("all done")

def action(code):
    if code in {"PUSH", "PULL", "UP", "DOWN", "RIGHT", "LEFT"}:
        for i in range(5):
            GPIO.output(PNO, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(PNO, GPIO.LOW)
            time.sleep(0.1)
    elif code == "ADD_SIGNAL":
        id = ir_operate.learn_signal()
        if id == None:
            print("send failed")
            #send failed
        else:
            print("send id")
            #send id
            
    elif code == "COMPLETE":
        ir_operate.save_signal(id)
    else:
        #send signal
        ir_operate.send_signal(code)
        print("send signal")
