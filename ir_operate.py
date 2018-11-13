from irmagician import IrMagician
import sys
import uuid
import sqlite3
import json
    
def capture_signal():
    mag = IrMagician()
        
    # capture IR signal
    while True:
        print("push remote controller button")
        print("...")
        r = mag.ir_capture()
        if ("Time Out" in r) == True or r == "":
            print("failed")
            return None
            continue  
        print("captured!")
        print(r)
        break

    # create ID
    id = uuid.uuid4().hex
    print(id)
        
    return id
    
def save_signal(id):
    mag = IrMagician()
    
    #get signal size
    ir_size_s = mag.command("I,1\r\n", 1.0)
    ir_size = int(ir_size_s, 16)
    #mag.log("ir_size=" + str(ir_size))

    #get postscaler
    postscale_str = mag.command("I,6\r\n")
    postscale = int(postscale_str)
    #mag.log("postscale=" +  postscale_str)

    #read signal
    values = []
    for n in range(ir_size):
        bank = n // 64
        pos = n % 64
        if (pos == 0):
            mag.write("b,%d\r\n" % bank)
                
        mag.write("d,%d\r\n" % pos)
        xs = mag.read(3)
        v = int(xs, 16)
        values.append(v)
            
    json_data = {
        'format':'raw', 'freq':38, 'data':values,
        'postscale':postscale}
    
    data = json.dumps(json_data)
        
    # save signal
    connection = sqlite3.connect("/home/pi/PythonProjects/RaspberryController/signal.db")
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO signals VALUES (?,?)', (id, data))
    except sqlite3.Error as e:
        print("DB failed")
        print(e)
        return False
        
    connection.commit()
    connection.close()
    print("DB success")
    return True

def send_signal(id):
    # find signal
    connection = sqlite3.connect("/home/pi/PythonProjects/RaspberryController/signal.db")
    cursor = connection.cursor()
    
    cursor.execute('SELECT data FROM signals WHERE id = ?', (id,))
    #print(cursor.fetchone())
    # send signal
    mag = IrMagician()
    tmp = str(cursor.fetchone())
    tmp = tmp[2:-3]
    print(tmp)
    if tmp == None:
        print("no such action")
        
    json_data = json.loads(tmp)
    
    ir_size = len(json_data['data'])
    values = json_data['data']
    
    # lead ir size
    mag.command("n,%d\r\n" % ir_size, 0.1)
    # lead postScale
    postscale = json_data['postscale']
    mag.command("k,%d\r\n" % postscale, 0.1)
    # lead data
    for n in range(ir_size):
        bank = n // 64
        pos = n % 64
        if (pos == 0):
            mag.write("b,%d\r\n" % bank)
        mag.write("w,%d,%d\n\r" % (pos, values[n]))
       
    # send data
    mag.command("p\r\n")
        
    print("send data!")
    connection.close()
    
##if __name__ == "__main__":
##    send_signal("a32e3ef8921e42fe833ef756043ddc3e")
