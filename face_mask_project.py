import cvzone
import cv2
import numpy as np
import time

from smbus2 import SMBus
from mlx90614 import MLX90614
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

from gpiozero import Button, LED
button = Button(12)
led = LED(24)
IRpin = 23
buzzer = 25

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pumpRelay = 8
lockRelay = 7

GPIO.setup(pumpRelay, GPIO.OUT)
GPIO.setup(lockRelay, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(IRpin, GPIO.IN)

from RPLCD import*
from time import sleep
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0X27)


lcd.cursor_pos = (0, 0)
lcd.write_string("Temp: ")
lcd.cursor_pos = (1, 0)
lcd.write_string("Mask: ")
lcd.cursor_pos = (2, 0)
lcd.write_string("Notice: ")
lcd.cursor_pos = (3, 0)
lcd.write_string("Access: ")

cap = cv2.VideoCapture(0)
myClassifier = cvzone.Classifier('MyModel/keras_model.h5','MyModel/labels.txt')
fpsReader = cvzone.FPS()

maskStatus = ""
access = ""
notice = ""

counter = 0

while True:

    body_temp = int(sensor.get_object_1())

    lcd.cursor_pos = (0, 6)
    lcd.write_string(str(body_temp))
    lcd.cursor_pos = (0, 9)
    lcd.write_string("C")
    time.sleep(0.2)

    _, img = cap.read()
    predictions, index = myClassifier.getPrediction(img, scale=1)
    fps = fpsReader.update()
    #print(index)

    if index == 0:
        counter += 1
    else:
        counter = 0
    print(counter)

    if counter >= 15:
        maskStatus = "Yes"
        print(maskStatus)
        lcd.cursor_pos = (1, 6)
        lcd.write_string(str(maskStatus))
    elif counter < 20 and maskStatus != "Yes":
        maskStatus = "No"
        print(maskStatus)
        lcd.cursor_pos = (1, 6)
        lcd.write_string(str(maskStatus))

    if maskStatus == "No " and body_temp <= 33:
        notice = "Put on Mask "
        lcd.cursor_pos = (2, 8)
        lcd.write_string(str(notice))
        access "Denied "
        lcd.cursor_pos = (3, 8)
        lcd.write_string(str(access))

    elif body_temp > 33:
        notice = "High temp     "
        lcd.cursor_pos = (2, 8)
        lcd.write_string(str(notice))
        access "Denied "
        lcd.cursor_pos = (3, 8)
        lcd.write_string(str(access))

    elif maskStatus == "Yes" and body_temp <= 33:
        notice = "Wash Hands    "
        lcd.cursor_pos = (2, 8)
        lcd.write_string(str(notice))
        access "                "
        lcd.cursor_pos = (3, 8)
        lcd.write_string(str(access))
        
        if (button.is_pressed):
        #if GPIO.output(IRpin):
            start = time.time()
            finish = start + 5
            while time.time() < finish:
                GPIO.output(pumpRelay, GPIO.HIGH)
                norice = "Pump on      "
                lcd.cursor_pos = (2, 8)
                lcd.write_string(str(notice))
                if time.time() > finish:
                    GPIO.output(pumpRelay, GPIO.LOW)
                    norice = "Pump off      "
                    lcd.cursor_pos = (2, 8)
                    lcd.write_string(str(notice))

                    start = time.time()
                    finish = start + 5
                    while time.time() < finish:
                        GPIO.output(lockRelay, GPIO.HIGH)
                        norice = "Granted      "
                        lcd.cursor_pos = (3, 8)
                        lcd.write_string(str(notice))
                        GPIO.output(buzzer, True)
                        if time.time() > finish:
                            GPIO.output(buzzer, False)
                            maskStatus = "No "
                            break
                        else:
                            continue
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break

    cv2.imshow("Image", img)
    cv2.waitKey(1)
