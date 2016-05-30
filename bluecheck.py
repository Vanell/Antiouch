# /usr/bin/python

import bluepy.btle # import bluetooth low-energy
import RPi.GPIO as GPIO

b = 10 # min value
a = 90 # distance impact
m = 100 # max value

GPIOpin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)

# from received signal strength indicator to 0->100
def calibrssi(rssi):
    rssi = -1*rssi
    rssi = rssi-b
    rssi = rssi*m/a
    rssi = m-rssi
    if rssi>m:
        rssi=m
    if rssi<10:
        rssi=10
    return rssi

def find_dist():	
	# scan for low energy bluetooth device

	sc = bluepy.btle.Scanner()
	scanned = sc.scan(timeout=2)

	# for each bluetooth le device do
	for dev in scanned:
    		name = dev.getValueText(9) # check the text name
    		if name:
        		if 'Bean' in name: # if Bean in the name
            			rssi = int(dev.rssi) #get the rssi
            			rssi = calibrssi(rssi) #calib the value
            			print rssi
        			return rssi
	    			# ICI RSSI varie entre 10 et 100
            			# (pour avoir un min a 10 des detection)
            			# et un max a 100 des qu'on est assez pres
            			# il faut utiliser GPIO.output pour faire varier l'output
#print type(rssi)

p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
        value = find_dist()
	if isinstance(value,float) or isinstance(value,int):
		p.ChangeDutyCycle(value)
	else :
		p.ChangeDutyCycle(0)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
