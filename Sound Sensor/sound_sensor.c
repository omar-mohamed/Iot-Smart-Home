#include <stdio.h>
#include <unistd.h>
#include "mraa.h"
#include "mraa/aio.h"
#include <Python.h>


#define ANALOG_PIN 0
#define DIGITAL_PIN 3


const char* get_sensor_reading()
{
    mraa_aio_context adc;
    int value;
    int result;
    mraa_gpio_context gpio;

    adc = mraa_aio_init(ANALOG_PIN);
	
	if (adc == NULL) {
        printf( "[-] Initialisation of analog pin %d"\
                "failed. Is this pin exist on your platform?\n",
                ANALOG_PIN);
        return "-1";
    }
//    printf("[+] Pin %d is initialised\n", LED_DIGITAL_PIN);
	
    gpio = mraa_gpio_init(DIGITAL_PIN);
	
	if (gpio == NULL) {
        printf( "[-] Initialisation of digital pin %d"\
                "failed. Is this pin exist on your platform?\n",
                DIGITAL_PIN);
        return "-1";
    }


    result = mraa_gpio_dir(gpio, MRAA_GPIO_IN);
	 
	if (result != MRAA_SUCCESS) {
        mraa_result_print(result);
        printf("[+] Pin %d is not initialised correctly\n", DIGITAL_PIN);
		return "-1";
    }

    int counter=0;
    while (1)
        {

            value = mraa_aio_read(adc);
//            printf( "Pin A%d received %d - \n", ANALOG_PIN, value);
            value = mraa_gpio_read(gpio);

            if (value==1) {
                printf("changing state.");
                sleep(1);
                return "1";
            }
        }
}


