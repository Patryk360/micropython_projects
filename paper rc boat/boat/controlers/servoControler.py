from machine import Pin, PWM
setDegree = 0

def setServoDegree(degree):
    global setDegree
    setDegree = degree

def getServoDegree():
    return setDegree