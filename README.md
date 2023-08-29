# People-Counter
This single python script will enable you to count inbound and outbound people in real time.
This script also provides functionality to blink RED and GREEN LED lights based on number of people entered and number of people left the room.
In order to use the LED functionality, it is recommended to deploy the script via Raspberry Pi.

So you need the following apparatus:
1. A Raspberry Pi
2. LED lights(Red, Green)
3. Web camera
4. HDMI cables
5. A Monitor or Any kind of suitable display

# Settings:
The settings are very straight forward, connect the LED lights to Raspberry Pi according to the type of lights you will be using. 
Then connect both web-cam and monitor to Raspberry pi accordingly. You can use the USB port on Raspberry Pi for web-cam and HDMI port for monitor.
Once the set up are done, then simply run the python script *counter.py* (do not forget to install OpenCV v3).
The script will generate a window by showing the live videos in monitor which includes the texts of *number of people entered, number of people exit, available places*
This will enable you to observe the results of people counter script. 

You can follow the connected LED lights, where the number of red light means: Number of occupied places in the room
and number of green light means: Number of available places in the room.
