#include <stdio.h>
#include <stdlib.h>
#include <libserialport.h>



void main() {
    int err;
    struct sp_port** my_ports;

    err = sp_list_ports(&my_ports);

}