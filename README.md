# Raspberry Pi Alarm System with a Keypad


GUI in Pygame to arm or disarm an alarm system on a Raspberry Pi. If armed, the system detects the state change of sensors connected to the RPi. The user has a some time to enter the right combination and disarm the alarm otherwise it goes off. The GUI also displays time and weather by pulling data from the Internet: OpenWeatherMap API. 


|<img width="398" alt="image" src="https://user-images.githubusercontent.com/116329812/206021331-317d61b1-97cd-4f1e-b2e8-7427e4326a1f.png">     |  <img width="401" alt="image" src="https://user-images.githubusercontent.com/116329812/206021484-efe76305-9f41-4946-9a33-5698b942bb42.png">   |
|-----|-----|
|  <img width="400" alt="image" src="https://user-images.githubusercontent.com/116329812/206021657-d931a4e9-bd65-4fd4-acda-9f594e98c1a8.png">   |<img width="398" alt="image" src="https://user-images.githubusercontent.com/116329812/206021743-aa63f056-b5e8-4a22-8292-b595a27fc815.png">     |


- Run on Linux/Ubuntu


Module: 
pygame
pyowm
math
requests
datetime
time
smtplib
RPISim
RPi.GPIO
