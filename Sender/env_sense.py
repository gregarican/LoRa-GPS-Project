from sense_hat import SenseHat
import serial
import time
import os
from picamera import PiCamera
from picamera.array import PiRGBArray

sense = SenseHat()
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)
ti = time.time()
init_speed = 0

while True:
        tmp = sense.get_temperature()
        tmp = int(round(tmp))

        bar = sense.get_pressure()
        bar = int(round(bar))

        hum = sense.get_humidity()
        hum = int(round(hum))

        new_time = time.time()
        yaw, pit, rol = sense.get_accelerometer_raw().values()

        distance = abs((init_speed + 0.5 * yaw * ((ti - time.time()) * (ti - time.time())) * 3.2808))
        speed = distance / new_time
        init_speed = speed
        
        alt = ((1 - (bar / 1013.25) ** 0.190284) * 145366.45) * 0.3048
        alt = int(round(alt))
        
        orig_msg = "KE8KUJ|DTM=%s|TMP=%s|BAR=%s|HUM=%s|ALT=%s" % (time.strftime("%Y%m%d_%H%M%S"),tmp,bar,hum,alt)
        print time.strftime("%Y%m%d_%H%M%S") + "|Got Sense Hat data."
        try:        
                new_msg = ser.readline()
                print time.strftime("%Y%m%d_%H%M%S") + "|Read serial data from LoRa/GPS."
        except:
                # Do nothing, since serial port is in use.
                new_msg = ""
                print time.strftime("%Y%m%d_%H%M%S") + "|Failed to read serial data from LoRa/GPS."
                pass
                
        time.sleep(1)
        file = open("/home/pi/data_log.csv", "a")
        try:
                ser.write(orig_msg.encode('utf-8'))
                print time.strftime("%Y%m%d_%H%M%S") + "|Wrote serial data to LoRa/GPS."
        except:
                # Do nothing, since serial port is in use.
                print time.strftime("%Y%m%d_%H%M%S") + "|Failed to write serial data to LoRa/GPS."
                pass
                
        file.write(orig_msg+new_msg+"\n")
        file.flush()
        file.close()
        print time.strftime("%Y%m%d_%H%M%S") + "|Displaying gathered data - " + orig_msg.rstrip() + new_msg.rstrip()

        #with PiCamera() as camera:
        #        camera.resolution = (1024,768)
        #        camera.start_preview()
        #        time.sleep(2)
        #        current_timestamp = time.strftime("%Y%m%d_%H%M%S")
        #        camera.capture("ke8kuj-%s.jpg" % (current_timestamp))
        #        with PiRGBArray(camera, size = (8,8)) as stream:
        #                camera.capture(stream, format='rgb', resize = (8,8))
        #                image = stream.array

        #        pixels = [
        #                pixel
        #                for row in image
        #                for pixel in row
        #                ]

        #        sense.set_pixels(pixels)
        print time.strftime("%Y%m%d_%H%M%S") + "|Displaying data on Sense Hat."
        print "-----------------------------"
        sense.show_message(orig_msg+new_msg,scroll_speed=0.05)
        time.sleep(60)
        sense.clear()
        
