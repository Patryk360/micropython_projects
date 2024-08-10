from machine import Pin, PWM
setDegree = 0

servo = PWM(Pin(9))
servo.freq(50)

def setServoDegree(degree):
    global setDegree
    setDegree = degree
    
    servoMinPWM = 3277 #1802
    servoMaxPWM = 6554 #7864
    
    duty = int((degree / 180) * (servoMaxPWM - servoMinPWM) + servoMinPWM)

    print(duty)
    
    servo.duty_u16(duty)

def getServoDegree():
    return setDegree