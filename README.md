# LoRa-GPS-Project
Specific application for high altitude ballooning.

---------------------------------------------

Sender is composed of:
Raspberry Pi 2 Model B --> https://www.raspberrypi.org/products/raspberry-pi-2-model-b/
RPi is connected via USB to an Arduino Uno --> https://store.arduino.cc/usa/arduino-uno-rev3
The RPi has a Sense HAT atop it --> https://www.raspberrypi.org/products/sense-hat/
For taking pix of the mission, the RPi also has a NoIR camera connected --> https://www.raspberrypi.org/products/pi-noir-camera-v2/
For determining GPS coords and sending GPS and Sense HAT data, the Arduino has a Dragino LoRa/GPS Shield --> http://wiki.dragino.com/index.php?title=Lora/GPS_Shield

Before the Arduino code will compile and upload to the Uno, the RadioHead project (http://www.airspayce.com/mikem/arduino/RadioHead/) and the TinyGPS project (http://arduiniana.org/libraries/tinygps/) need to be installed.

Before the Python program will run on the RPi, Sense-Hat will need to be installed --> https://www.raspberrypi.org/documentation/hardware/sense-hat/.

TIPS
----
- I have commented out the Python code that snaps a pic on a regular timer. Remove the comments to enable this feature. For testing I could display the snapped pic on the LED matrix. This should remain commented out, since it's not required. The various stats all scroll by on the LED matrix display anyway.

- In order to have the Uno's USB communication with the RPri and LoRa/GPS communication all functioning, you will need to jumper the GPS to the Uno. See the Dragino Wiki page listed above for the specifics.

- A large USB smartphone power brick can replace a standard wall power adapter for RPi portability (e.g. - High Altitude Ballooning).
 
- A 4 x AA battery pack with a barrel adapter can supplement USB power for the Uno so that it has a backup power source.

- http://predict.habhub.org/ is a great website for predicting HAB landing location based on the supplied flight plan details.

- https://www.highaltitudescience.com/pages/balloon-performance-calculator is another great tool for determining the required HAB supplies, based on the supplied details.

---------------------------------------------

Receiver is composed of:
Any standard Windows 7 and above laptop with at least two available USB ports.
An Arduino Uno --> https://store.arduino.cc/usa/arduino-uno-rev3
Sitting atop the Uno is a LoRa Shield --> http://wiki.dragino.com/index.php?title=Lora_Shield.
For determining GPS coords the Windows laptop has a GlobalSat USB Dongle --> http://www.globalsat.com.tw/s/2/product-199954/GPS-Receiver-ND-105C.html.

Before the Arduino code will compile and upload to the Uno, the RadioHead project (http://www.airspayce.com/mikem/arduino/RadioHead/) needs to be installed.

Before the Python program will run on the RPi, numpy, gmplot, ISStreamer, and pynmea2 will all need to be pip-installed.

TIPS
----
- The Python program plots both sender and receiver GPS coords to a Google Map in real-time. Internet access is required to completely display the content. When in a chase car that's well outside of cellular coverage, feeding these coords into a full-fledged GPS smartphone app will help.

- The Python program also posts real-time sender stats into InitialState --> https://app.initialstate.com/#/. Again, this IOT link is based on the presumption that the laptop has consistent Internet access. Regardless of that, both the sender and receiver store the sender data (e.g. - time-stamped Long, Lat, Temp, Hum, Alt, etc.).

- Since 915 MHz LoRa transmission requires line of sight, HAB transmissions should surpass terrestrial distances. The former has been tested at 15-20 miles, whereas the latter is usually limited to maybe 1-2 miles. 

- This LoRa frequency doesn't require an FCC transmission license (i.e. - Ham Radio class licensing). It's open to use for anyone.

- Any HAB payloads less than 5 pounds don't require FAA permits. But 30 minutes prior to HAB launch, you will need to contact the closest FAA field office in order to provide them specifics (e.g. - the Long/Lat launch point, the estimated Long/Lat landing point, the estimated flight time, a brief description of the HAB's characteristics and weight, etc.).

- If you have an amateur radio license, then you could connect the laptop to a mobile transceiver and rebroadcast the telemmetry via APRS. This is outside the scope of this project, but feel free to extend it!




