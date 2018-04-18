#include <stdio.h>                                
#include "mraa.h"                                 
#include <Python.h>                               
#define ANALOG_PIN 0                              
#define DIGITAL_PIN 7                             
#define THRESHOLD 500                             
                                                  
const char* return_string(){                      
                                                   
    mraa_aio_context sensor;                       
    mraa_gpio_context led;                         
    uint16_t value;                                
    mraa_result_t result;                          
                                                   
    sensor = mraa_aio_init(ANALOG_PIN);            
    if(sensor == NULL){                            
      printf("Cannot init pin %d \n",ANALOG_PIN);  
      return "close";                              
    }                                              
                                                   
   led = mraa_gpio_init(DIGITAL_PIN);              
   if(led == NULL){                                
      printf("Cannot init pin %d \n",DIGITAL_PIN); 
      return "close";                              
   }                                               
                                                   
 printf("Pin %d is initialized \n",DIGITAL_PIN);   
 result = mraa_gpio_dir(led,MRAA_GPIO_OUT);        
 while(1){                                         
   value = mraa_aio_read(sensor);                  
   printf("Pin A%d received %d ",ANALOG_PIN,value);
                                
   if(value < THRESHOLD){       
      // mraa_gpio_write(led,0);     
        return "0";             
   }                            
   else{                        
       //  mraa_gpio_write(led,1);                                          
        return "1";                                
  }                                                
                                                   
  sleep(1);                                        
                                                                                                     
 }                                                 
                                                                                                    
}          

