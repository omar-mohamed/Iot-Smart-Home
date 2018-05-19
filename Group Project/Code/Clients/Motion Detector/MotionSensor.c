#include <stdio.h>
#include <unistd.h>
#include "mraa/gpio.h"
#include <Python.h>
#define DIGITAL_IN 4
#define DIGITAL_OUT 7

const char* return_string()
{
	mraa_gpio_context gpio_out, gpio_in;
	uint16_t val;
	mraa_result_t led_result, PIR_result;
	gpio_in = mraa_gpio_init(DIGITAL_IN);
	gpio_out = mraa_gpio_init(DIGITAL_OUT);

	if (gpio_in == NULL)
	{
		printf("pin %d not initiated\n", DIGITAL_IN);
		return "-1";
	}
	if (gpio_out == NULL)
	{
		printf("pin %d not initiated\n", DIGITAL_OUT);
		return "-1";
	}
	
	PIR_result = mraa_gpio_dir(gpio_in, MRAA_GPIO_IN);
	led_result = mraa_gpio_dir(gpio_out, MRAA_GPIO_OUT);
	
	if (PIR_result != MRAA_SUCCESS) {
		mraa_result_print(PIR_result);
		printf("Pin %d is not initialised correctly\n", DIGITAL_IN);
		return "-1";
	}
	if (led_result != MRAA_SUCCESS) {
		mraa_result_print(led_result);
		printf("Pin %d is not initialised correctly\n", DIGITAL_OUT);
		return "-1";
	}
	
	while(1)
	{
		val = mraa_gpio_read(gpio_in);
		
		printf("Pin D%d received %hu \n", DIGITAL_IN, val);

		if (val == 1)
		{
			printf("GPIO1 1\n");
			return "1";
		}
		else
		{
			printf("GPIO1 0\n");
			return "0";
		}
		sleep(1);
	}
}