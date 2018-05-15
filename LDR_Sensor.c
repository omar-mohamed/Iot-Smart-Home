#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "mraa.h"
#include "mraa/aio.h"
#include "mraa/gpio.h"

#define ANALOG_PIN 0
#define DIGITAL_PIN 7
#define MAX_VALUE 250

int
main(void)
{
    mraa_result_t status = MRAA_SUCCESS;
    mraa_gpio_context gpio_1, gpio_2;
    mraa_aio_context adc;
    int value;
    mraa_result_t result;
    mraa_gpio_context gpio;
    int val;
    mraa_init();
    

    adc = mraa_aio_init(ANALOG_PIN);
    if (adc == NULL) {
        printf("Cannot initiate pin number ( %d ) \n", ANALOG_PIN);
        return (1);
    }

    gpio_1 = mraa_gpio_init(DIGITAL_PIN);
    if (gpio_1 == NULL) {
        printf("Failed to initialize GPIO number ( %d ) \n", DIGITAL_PIN);
        mraa_deinit();
        return EXIT_FAILURE;
    }

    result = mraa_gpio_dir(gpio_1, MRAA_GPIO_OUT);
    if (result != MRAA_SUCCESS) {
        mraa_result_print(result);
    	printf("Pin %d is not initialised correctly\n", DIGITAL_PIN);
    } else {
    	printf("Pin %d is initialised as output\n", DIGITAL_PIN);
    }
    

    while (1) {
	value = mraa_aio_read(adc);
        printf("Analog Pin A%d received Light Resistance =  %hu and It's ",ANALOG_PIN, value);
            if (value > MAX_VALUE) {
                result = mraa_gpio_write(gpio_1, 1);
            	printf(" more than MAX %d\n",MAX_VALUE);
	    } else {
                result = mraa_gpio_write(gpio_1, 0);
            	printf("less than MAX %d\n",MAX_VALUE);
	    }
        sleep(1);
    }
    mraa_deinit();
    return EXIT_FAILURE;
}
