import serial
import time
import struct
import numpy
import gmplot
from ISStreamer.Streamer import Streamer
import pynmea2

ser_LoRa = serial.Serial ("COM5")			# UART port.
ser_LoRa.baudrate = 9600                    		# Set baud rate to 9,600.
ser_LoRa.timeout = 15                            	# Read timeout of 15 seconds.

ser_gps = serial.Serial("COM7")
ser_gps.baudrate = 4800
ser_gps.timeout = 1
#ser_gps.open()

gmap = gmplot.GoogleMapPlotter(39.858394, -83.103535, 16)	#39.858394, -83.103535
latitudes_LoRa = [39.858394]
longitudes_LoRa = [-83.103535]
latitudes_gps =  [39.858394]
longitudes_gps = [-83.103535]
my_bucket_key = 'InitialStateBucketKey'
my_access_key = 'InitialStateAccessKey'
api_endpoint = 'https://groker.initialstate.com/api/events?accessKey=InitialStateAccessKey&bucketKey=InitialStateBucketKey'
streamer = Streamer(bucket_name="LoRa Hat Stream", bucket_key=my_bucket_key, access_key=my_access_key)
streamer.log("My Messages", "Stream Starting")

while True:
	data_LoRa = ser_LoRa.readline().rstrip()
	if data_LoRa.startswith('Got message'):
		message = data_LoRa.split('|')
		if message[0].endswith('KE8KUJ'):
			del message[0]
			for seg in message:
				els = seg.split('=')
				key = els[0]
				value = els[1]
				print ("Key = %s | Value = %s") % (key, value)
				if key == "LAT":
					latitudes_LoRa.append(float(value))
				elif key == "LON":
					longitudes_LoRa.append(float(value))
				elif key != "DTM" and key != "GPS":
					streamer.log(key,int(value)) 
	elif data_LoRa.startswith('RSSI:'):
		message = data_LoRa.split(':')
		key = "RSS"
		value = message[1]
		streamer.log(key,int(value))
		print("Key = %s | Value = %s") % (key, value)
	
	data_gps = ser_gps.readline()
	if data_gps[0:6] == '$GPGGA':
		try:
			msg = pynmea2.parse(data_gps)
			lat = msg.latitude
			lon = msg.longitude	
			latitudes_gps.append(float(lat))
			longitudes_gps.append(float(lon))
		except:
			continue		
	gmap.plot(latitudes_gps, longitudes_gps, 'red', edge_width=5)
	gmap.plot(latitudes_LoRa, longitudes_LoRa, 'cornflowerblue', edge_width=5)
	gmap.draw("mymap.html")
