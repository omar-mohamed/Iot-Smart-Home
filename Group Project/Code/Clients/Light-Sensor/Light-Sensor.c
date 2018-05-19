#include<stdio.h>

#include "mraa/aio.h"
#include<string>
#include <sstream>
#include<cstring>
using namespace std;
#define DigitalPin1 0
#define DigitalPin2 6
#define PhotoResistorPin 0

#define TSH 100
#define TSH2 200
extern "C"
const char* getLightSensorVal(){
mraa_aio_context PhotoResistor = mraa_aio_init(PhotoResistorPin);
mraa_result_t Result;
int SensorVal;
if(PhotoResistor==NULL)
{
printf("Sensor not Initialized");
return 0;
}

SensorVal = mraa_aio_read(PhotoResistor);
stringstream ss ;
ss<<SensorVal;
return ss.str().c_str();

}
int runSensor(){
mraa_gpio_context DPin1 = mraa_gpio_init(DigitalPin1);
mraa_gpio_context DPin2 = mraa_gpio_init(DigitalPin2);

mraa_aio_context PhotoResistor = mraa_aio_init(PhotoResistorPin);
mraa_result_t Result;
int SensorVal;
printf("run");
if(DPin1==NULL)
{ printf("Digital Pin Not Initialized .\n");
return 0;
if(DPin2==NULL)
{ printf("Digital Pin 2 Not Initialized .\n");
return 0;
}

}
if(PhotoResistor==NULL)
{
printf("Sensor not Initialized");
return 0;
}


Result = mraa_gpio_dir(DPin1,MRAA_GPIO_OUT);
if(Result != MRAA_SUCCESS){
printf("error pin1");
return 2;
}

Result = mraa_gpio_dir(DPin2,MRAA_GPIO_OUT);

if(Result != MRAA_SUCCESS){
printf("error pin 2");
return 2;
}

while(1){
SensorVal = mraa_aio_read(PhotoResistor);
printf("PhotoResistor Read %d\n",SensorVal);
fflush(stdout);
if(SensorVal >TSH2){
    mraa_gpio_write(DPin1,1);
    mraa_gpio_write(DPin2,1);

}
else if(SensorVal > TSH)
    {
     mraa_gpio_write(DPin1,1);
    mraa_gpio_write(DPin2,0);

    }
  else
    {
    mraa_gpio_write(DPin1,0);
    mraa_gpio_write(DPin2,0);

    }

sleep(1);
}

return 0;
}
