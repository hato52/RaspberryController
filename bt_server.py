import RPi.GPIO as GPIO
import time
from bluetooth import *
import ir_operate

PNO = 4
id = ""

def action(code):
    if code in {"PUSH", "PULL", "UP", "DOWN", "RIGHT", "LEFT"}:
        for i in range(5):
            GPIO.output(PNO, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(PNO, GPIO.LOW)
            time.sleep(0.1)
            
    elif code == "b'ADD_SIGNAL'":
        global id
        id = ir_operate.capture_signal()
        if id == None:
            print("send failed")
            client_sock.send("IR_FAILED")
            #send failed
        else:
            print("send id")
            client_sock.send(id)
            #send id
            
    elif code == "b'COMPLETE'":
        global id
        print("save signal")
        ir_operate.save_signal(id)
        
    else:
        #send signal
        code = code[2:-1]
        print(code)
        ir_operate.send_signal(code)


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
        # execute action when data received
        code = client_sock.recv(1024)
        if len(code) == 0: break
        print("received: %s" % str(code))
        action(str(code))
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
GPIO.cleanup()
print("all done")
