//Include required lib so Arduino can talk with the Lora Shield
#include <SPI.h>
#include <RH_RF95.h>
#include <SoftwareSerial.h>
#include <stdlib.h>

// Singleton instance of the radio driver
RH_RF95 rf95;
int led = 4;
int reset_lora = 9;
String dataString = "";

void setup() 
{
  pinMode(led, OUTPUT); 
  pinMode(reset_lora, OUTPUT);    
  
  // Initialize the USB-Serial connection.
  Serial.begin(9600);
  
  // reset lora module first. to make sure it will works properly
  digitalWrite(reset_lora, LOW);   
  delay(1000);
  digitalWrite(reset_lora, HIGH); 
  
    if (!rf95.init())
    {
      Serial.println("RF initialitzation failed.");  
      // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
      // Need to change to 868.0Mhz in RH_RF95.cpp 
    }
    else
    {
      Serial.println("RF initialized.");
      //bool mdmCfg = rf95.setModemConfig(RH_RF95::Bw125Cr48Sf4096);
      //bool mdmFreq = rf95.setFrequency(915.0);
      rf95.setFrequency(868.0);
      rf95.setTxPower(13);
      /*if (mdmCfg == false || mdmFreq == false)
      {
        Serial.println("RF not configured.");
      }
      else
      {
        Serial.println("RF configured.");
      }*/
    }
  
}

void loop()
{
  dataString="";
  if (rf95.available())
  {
    Serial.println("Get new RF message");
    // Should be a message for us now   
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    if (rf95.recv(buf, &len))
    {
      digitalWrite(led, HIGH);
      //RH_RF95::printBuffer("request: ", buf, len);
      Serial.print("Got message: ");
      Serial.println((char*)buf);
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);

      // Send a reply to client as ACK
      /*uint8_t data[] = "200 OK";
      rf95.send(data, sizeof(data));
      rf95.waitPacketSent();
      Serial.println("Sent a reply");*/
    }
  }
}
