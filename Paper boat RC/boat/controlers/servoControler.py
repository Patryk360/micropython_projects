from machine import Pin, PWM
setDegree = 0

servo = PWM(Pin(9))
servo.freq(50)

def setServoDegree(degree):
    global setDegree
    setDegree = degree
    
    servoMinPWM = 3277
    servoMaxPWM = 6136#6554 - (19*22)
    
    duty = int((degree / 180) * (servoMaxPWM - servoMinPWM) + servoMinPWM)
    
    #duty = 4916-(19*10)

    
    servo.duty_u16(duty)

def getServoDegree():
    return setDegree