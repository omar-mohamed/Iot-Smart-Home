#include <stdio.h>
#include <unistd.h>
#include "mraa.h"
#include "mraa/aio.h"
#include <Python.h>
#define ANALOG 0
#define THRESHOLD 500

const char* return_string()
{
        mraa_aio_context abc;
        uint16_t val;
        abc = mraa_aio_init(ANALOG);
        if (abc == NULL)
        {
                printf("pin %d not initiated\n", ANALOG);
                return "-1";
        }
        while(1)
        {
                sleep(1);
                val = mraa_aio_read(abc);
                printf("Pin A%d received %hu ", ANALOG, val);

                if (val > THRESHOLD)
                {
                        printf("GPIO 1\n");
                        return "1";
                }
                else
                {
                        printf("GPIO 0\n");
                        return "0";
                }
        }
}
