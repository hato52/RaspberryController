import RPi.GPIO as GPIO
import time
from bluetooth import *

PNO = 4

# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO, GPIO.OUT)

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805F9B34FB"

advertise_service(server_sock, "SampleServer",
                  service_id = uuid,
                  service_classes = [uuid, SERIAL_PORT_CLASS],
                  profiles = [SERIAL_PORT_PROFILE],
#                  protocols = [OBEX_UUID]
                  )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data)
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