import RPi.GPIO as GPIO
LF=18
LB=23
RF=24
RB=25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LF, GPIO.OUT)
GPIO.setup(LB, GPIO.OUT)
GPIO.setup(RF, GPIO.OUT)
GPIO.setup(RB, GPIO.OUT)
GPIO.output(LF , 0)
GPIO.output(RF , 0)
GPIO.output(LB , 0)
GPIO.output(RB , 0)
print("Motor setup done")

from datetime import datetime
sig = 17
codes = [0x300ff18e7, 0x300ff10ef, 0x300ff4ab5, 0x300ff5aa5, 0x300ff38c7]
names = ["Forward","Left","Reverse","Right","Ok"]
GPIO.setup(sig, GPIO.IN)

def getBinary():
    num1s = 0
    binary = 1
    command = []
    prev = 0
    val = GPIO.input(sig)
    
    while val:
        val = GPIO.input(sig)
        
    startTime = datetime.now()
    
    while True:
        if prev != val:
            now = datetime.now()
            pulseTime = now - startTime
            startTime = now
            command.append((prev,pulseTime.microseconds))
            
        if val:
            num1s += 1
        else:
            num1s = 0
        if num1s > 10000:
            break
            
        prev = val
        val = GPIO.input(sig)
        
    for(typ, tme) in command:
        if typ == 1:
            if tme > 1000:
                binary = binary*10 + 1
            else:
                binary *= 10
        
    if len(str(binary)) > 34:
        binary = int(str(binary)[:34])    
    return binary

def convertHex(binval):
    tmpB2 = int(str(binval),2)
    return hex(tmpB2)

while True:
    inData = convertHex(getBinary())
    for code in range(len(codes)):
        if hex(codes[code]) == inData:
            key = names[code]
            print(key)
            if(key=="Left"):
                print("moving left")
                GPIO.output(LF , 0)
                GPIO.output(LB , 0)
                GPIO.output(RF , 1)
                GPIO.output(RB , 0)
                
            elif(key=="Right"):
                print("moving right")
                GPIO.output(LF , 1)
                GPIO.output(LB , 0)
                GPIO.output(RF , 0)
                GPIO.output(RB , 0)

            elif(key=="Forward"):
                print("moving forward")
                GPIO.output(LF , 1)
                GPIO.output(LB , 0)
                GPIO.output(RF , 1)
                GPIO.output(LB , 0)

            elif(key=="Reverse"):
                print("moving rev")
                GPIO.output(LF , 0)
                GPIO.output(LB , 1)
                GPIO.output(RF , 0)
                GPIO.output(RB , 1)
    
            elif(key=="Ok"):
                GPIO.output(LF , 0)
                GPIO.output(LB , 0)
                GPIO.output(RF , 0)
                GPIO.output(RB , 0)
                print("Stop")
                
            elif(input() == 'q'):
                exit()

exit()
