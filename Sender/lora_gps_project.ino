#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include <SPI.h>
#include <RH_RF95.h>
#include <stdlib.h>

RH_RF95 rf95;
TinyGPS gps;
SoftwareSerial ssGps(3, 4);
int led = 4;
int reset_lora = 9;

void setup() 
{
	// Reset the LoRA.
        pinMode(led, OUTPUT);
        pinMode(reset_lora, OUTPUT);
        digitalWrite(reset_lora, LOW);
        delay(1000);
        digitalWrite(reset_lora, HIGH);
        
        // Initialize the USB-Serial and GPS software serial connections.
        Serial.begin(9600);
        ssGps.begin(9600);
        
	if (!rf95.init())
        {
          //Serial.println("RF not initialized!");
        }
        rf95.setFrequency(915.0);
        rf95.setTxPower(13);
}

void loop()
{
      bool newData = false;  
      char rpi_sense[100]={"\0"};
      char gps_data[100]={"\0"};
      char aryLon[10]={"\0"};
      char aryLat[10]={"\0"};    
	
      // Every X seconds we parse GPS data and report some key values.
      for (unsigned long start = millis(); millis() - start < 60000;)
      {
        while (ssGps.available())
        {
          char c = ssGps.read();
          if (gps.encode(c))
          newData = true;
        }
      }
      
      // Get the GPS data.
      if (newData)
      {
        float flat, flon;
        unsigned long age;
        gps.f_get_position(&flat, &flon, &age);
        
        // Send the GPS data back to RPi over USB-Serial.
        Serial.print("|LAT=");
        Serial.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
        Serial.print("|LON=");
        Serial.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
        Serial.print("|SAT=");
        Serial.print(gps.satellites() == TinyGPS::GPS_INVALID_SATELLITES ? 0 : gps.satellites());
        Serial.print("|PRC=");
        Serial.println(gps.hdop() == TinyGPS::GPS_INVALID_HDOP ? 0 : gps.hdop());        
        
        strcpy(gps_data, "KE8KUJ|LAT=");
        dtostrf(flat, 10, 6, aryLat);
        strcat(gps_data, aryLat);
        strcat(gps_data, "|LON=");
        dtostrf(flon, 10, 6, aryLon);
        strcat(gps_data, aryLon);
            
        // Send GPS data to RF peer.
        rf95.send((uint8_t *)gps_data, sizeof(gps_data));
        rf95.waitPacketSent();             
        
        // Check the USB-Serial buffer for data from RPi.
        while (Serial.available())
        {
          String sr = Serial.readString();
          sr.toCharArray(rpi_sense, 100);
          
          // Send Hat data to RF peer.
          rf95.send((uint8_t *)rpi_sense, sizeof(rpi_sense));
          rf95.waitPacketSent();
        }        
      }
      else  // No GPS data available.
      {
        // Send GPS error back to RPi over USB-Serial.
        Serial.println("|GPS=Err");
        strcpy(gps_data, "KE8KUJ|GPS=Err");
        
        // Send GPS error to RF peer.
        rf95.send((uint8_t *)gps_data, sizeof(gps_data));
        rf95.waitPacketSent();
      }
}
