from irmagician import IrMagician
import sys
import uuid
import sqlite3
    
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
        
    # save signal
    connection = sqlite3.connect("signal.db")
    cursor = connection.cursor()
    try:
        c.execute("INSERT INTO signals VALUES (?,?)", id, json_data)
    except sqlite3.Error as e:
        return False
        
    return True

def send_signal(id):
    # find signal
    connection = sqlite3.connect("signal.db")
    cursor = connection.cursor()
    
    c.execute("SELECT code FROM signals WHERE id = ?", id)
    
    # send signal
    mag = IrMagician()
    json_data = json.dumps(cursor.fetchone())
    
    ir_size = len(json_data['data'])
    values = json_data['data']
    
    # send ir size
    self.command("n,%d\r\n" % ir_size, 0.1)
    # send postScale
    postscale = json_data['postscale']
    self.command("k,%d\r\n" % postscale, 0.1)
    # send data
    for n in range(ir_size):
        bank = n // 64
        pos = n % 64
        if (pos == 0):
            self.write("b,%d\r\n" % bank)
        self.write("w,%d,%d\n\r" % (pos, values[n]))
    
if __name__ == "__main__":
    learn_signal()