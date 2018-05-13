#include <stdio.h>
#include <mraa.h>

#define BUZZER_PIN 3
#define BUTTON_PIN 11
#define SENSOR_PIN 0

int main(){
	int sensor_data, button_status, buzzer_is_active = 0;
	FILE* data_file;
	
	data_file = fopen("fire_alarm_data.txt","w");
	fprintf(data_file,"0");
	fclose(data_file);
	
	mraa_gpio_context buzzer;
	mraa_gpio_context button;
	mraa_aio_context sensor;

	buzzer = mraa_gpio_init(BUZZER_PIN);
	button = mraa_gpio_init(BUTTON_PIN);
	sensor = mraa_aio_init(SENSOR_PIN);

	mraa_gpio_dir(buzzer,MRAA_GPIO_OUT);
	mraa_gpio_dir(button,MRAA_GPIO_IN); 

	if(!buzzer || !button || !sensor){
		printf("Error!\n");
		return 0;
	}

	while(1){
		if(!buzzer_is_active){
			sensor_data = mraa_aio_read(sensor);
			printf("Sensor: %d\n",sensor_data);
			if(sensor_data > 2){
				printf("The buzzer will start now! Press and hold the button to stop it!\n");
				buzzer_is_active = 1;
				mraa_gpio_write(buzzer,1);
				data_file = fopen("fire_alarm_data.txt","w");
				fprintf(data_file,"1");
				fclose(data_file);
			}
			else sleep(1);
		}
		else{
			button_status = mraa_gpio_read(button);
			printf("Button: %d\n",button_status);
			sleep(1);
			if(!button_status && !mraa_gpio_read(button)){
				buzzer_is_active = 0;
				mraa_gpio_write(buzzer,0);
				data_file = fopen("fire_alarm_data.txt","w");
				fprintf(data_file,"0");
				fclose(data_file);
			}
		}	
	}

	mraa_gpio_close(buzzer);
	mraa_gpio_close(button);
	mraa_aio_close(sensor);

	return 0;

}
