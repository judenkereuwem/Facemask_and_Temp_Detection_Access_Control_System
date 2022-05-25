# Facemask_and_Temp_Detection_Access_Control_System

Project Features:
This system detect human faces and checks their temperature, if the person is putting 
on a health mask and their temperature is normal (not too high), they will be asked to 
wash their hands then the solenoid lock will open, granting them access to the facility.
If their temperature is high, and/or they don't have their mask on, then the system will 
deny them access to the facility.

Harware Components:
- Raspberry pi 4 (Model B: 2GB RAM)
- SD CARD (16 GB)
- Webcam or Pi Ccamera
- Mlx90614 temperature Sensor
- IR obstacle avoidance sensor
- Relay module x 2
- 20x4 LCD with I2C module
- Selonoid lock
- Water pump
- Buzzer

Software:
- Raspberry Pi OS (Buster)
- Python3 programming language
- OpenCV for image processing
- Teachable machines for training our model
- TensorFlow 2.3.0
- cvzone 1.3.3



How the system works:

Step 1
-Move fore-head closer to the temperature sensor to check body temperature:
if the body temperature is higher than recommended, the system will deny access 
to the user, while displaying the infomations on an LCD scrren.

Step 2
-The camera on the system will then monitor your face for mask:
if you do not have your mask on but your temperature is of recommended
value, the system will notify you to put on mask while still denying
access. An LED will light up when mask is detected and remain off if no mask
is detected. When LED is on (mask on), focus on the camera with taht position
for some seconds to verify the mask detection till the LCD displays "Mask: Yes" 
(this helps to avoid glitch while processing mask detection)

Step 3
-If your temp. is as recommended, and LCD displays "Mask: Yes", the system will 
notify you to wash your hands. If you place your hands under the tap, you'll
trigeer the IR sensor which will keep the tap and buzzer on for set time (say 5 sec) 
then turn off the tap.

Step 4
-After washing your hands, the system will grant access by unlocking a solenoid 
lock for set time (e.g 5 sec) then restart the  system to monitor new users.
