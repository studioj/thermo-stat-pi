#include"TFT_eSPI.h"
TFT_eSPI tft;

#include <Wire.h>

#include "SparkFun_SCD30_Arduino_Library.h" //Click here to get the library: http://librarymanager/All#SparkFun_SCD30
SCD30 airSensor;
bool connected_to_wifi = false;

#include "rpcWiFi.h"

const char* ssid = "yourNetworkName";
const char* password =  "yourNetworkPassword";

void setup() {
    tft.begin();
    tft.setRotation(1);

    tft.fillScreen(TFT_GREEN);
    tft.setTextColor(TFT_BLACK);
    tft.setTextSize(4);
    tft.drawString("Booting", 50, 100);
    Wire.begin();
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();

    Serial.println("Connecting to WiFi..");
    WiFi.begin(ssid, password);
    int time_print = 0;
    for( int i = 0; i<=5;i++) {
        if (WiFi.status() != WL_CONNECTED){
            delay(500);
            tft.fillScreen(TFT_GREEN);
            tft.setTextColor(TFT_BLACK);
            tft.setTextSize(4);
            tft.drawString("Connecting to", 30, 80);
            tft.drawString("Wifi " + String(time_print), 60, 130);
        }
        else {
            connected_to_wifi = true;
        }
    }
    tft.fillScreen(TFT_GREEN);
    tft.setTextColor(TFT_BLACK);
    tft.setTextSize(4);
    tft.drawString("Connected to", 30, 80);
    tft.drawString("Wifi", 60, 130);
    tft.drawString(String(WiFi.localIP()), 60, 180);
    if (airSensor.begin() == false)
    {
        tft.fillScreen(TFT_RED);
        tft.drawString("Cant connect", 20, 80);
        tft.drawString(" to sensor", 30, 130);
        tft.setTextSize(3);
        tft.drawString("please get help!", 25, 180);
    }
    else {
        if (airSensor.dataAvailable()) {
          int cotwo = doMeasurements(3,2000);
          drawScreen(cotwo);
        }
    }
}

void loop() {
    int sleeptime = 2500;
    int loops = 3;

    int measured_value = doMeasurements(loops, sleeptime);
    drawScreen(measured_value);
    if (measured_value > 1000) {
        sleeptime = 1000;
    }
    else {
        sleeptime = 10000;
    loops = 6;
    }
}

void drawScreen(int measured_value){
    int screencolor = TFT_GREEN;
    if (measured_value > 900) {
        screencolor = TFT_ORANGE;
        if (measured_value > 1200){
            screencolor = TFT_RED;
        }
    }
    tft.setTextColor(TFT_BLACK);
    tft.setTextSize(10);
    tft.fillScreen(screencolor);
    tft.drawString(String(measured_value), 102, 60);
    tft.setTextSize(4);
    tft.drawString("ppm co2", 85, 190);
    tft.setTextSize(1);
    if (connected_to_wifi){
        tft.drawString(String(WiFi.localIP()), 0, 220);
    }

}

int doMeasurements(int loops, int sleeptime){
    int sum = 0;
    int measurements = 0;
    for( int i = 0; i<=loops;i++) {
        int cotwo = 0;
        delay(sleeptime);
        while(!airSensor.dataAvailable()) {
            delay(500);
        }
            cotwo = airSensor.getCO2();
            measurements++;
        sum += cotwo;
        if (cotwo > 1000) {
            sleeptime = 2200;
        }
    }
    return sum/measurements;
}
