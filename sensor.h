#ifndef SENSOR_H
#define SENSOR_H

// Header file for finger print sensor library
// Written for R301 Finger print sensor, should work for R30X sensors 
//#include <stdio.h>
//#include <stint.h>
#include "Arduino.h"

//Variables
uint32_t* packet_addr;

//Packet structure
typedef struct packet {
	uint16_t header;
	uint32_t addr;
	uint8_t packet_id;
	uint16_t packet_len;
	uint8_t packet_data;
	uint16_t checksum;
} packet_t;

// Command Defines
//System Commands
#define S_SET_SYS_PARAM 0x0E
#define S_READ_SYS_PARAM 0x0F
#define S_SET_PWD 0x12
#define S_VERIFY_PWD 0x13
#define S_SET_ADDR 0x15
#define S_PORT_CONTROL 0x17
#define S_TEMPLATE_NUM 0x1D

//Fingerprint Commands
#define F_GEN_IMG 0x01
#define F_IMG2TZ 0x02
#define F_MATCH 0x03
#define F_SEARCH 0x04
#define F_REG_MODEL 0x05
#define F_STORE 0x06
#define F_LOAD_CHAR 0x07
#define F_UP_CHAR 0x08
#define F_DOWN_CHAR 0x09
#define F_UP_IMG 0x0A
#define F_DOWN_IMG 0x0B
#define F_DELETE_CHAR 0x0C
#define F_EMPTY_LIB 0x0D
#define F_HIGH_SPEED_SEARCH 0x1B

//Other Commands
#define O_GET_RAND 0x14
#define O_WRITE_NOTEPAD 0x18
#define O_READ_NOTEPAD 0x19

// Acknowledgment Defines
#define ACK_COMMAND_EXECUTED 0x00
#define ACK_RECEIVE_ERROR 0x01
#define ACK_NO_FINGER 0x02
#define ACK_ENROLL_FAIL 0x03
#define ACK_CHAR_GEN_FAIL_DISORDER 0x06
#define ACK_CHAR_GEN_FAIL_SMALLFINGER 0x07
#define ACK_MATCH_FAIL 0x08
#define ACK_FINGER_FIND_FAIL 0x09
#define ACK_CHAR_COMBINE_FAIL 0x0A
#define ACK_PAGEID_OUTSIDE_RANGE 0x0B
#define ACK_INVALID_TEMPLATE 0x0C
#define ACK_TEMPLATE_UPLOAD_ERROR 0x0D
#define ACK_MODULE_DATAPACK_RECEIVE_ERROR 0x0E
#define ACK_IMAGE_UPLOAD_ERROR 0x0F
#define ACK_TEMPLATE_DELETE_FAIL 0x10
#define ACK_FINGER_LIBRARY_CLEAR_FAIL 0x11
#define ACK_WRONG_PASSWORD 0x13
#define ACK_IMAGE_GEN_FAIL_INVALID_PRIMARY_IMAGE 0x15
#define ACK_INVALID_HEADER 0xFF

//Constant defines 
#define HEADER 0xEF01
#define ADDR 0xFFFFFFFF
#define CMD_PKT 0x01
#define DATA_PKT 0x02
#define ACK_PKT 0x07
#define END_PKT 0x08
#define PACKET_SIZE 12 //Packet size in bytes

//Utility commands
uint32_t form_packet(uint8_t packet_id, uint16_t packet_len, uint8_t* data_ptr, uint16_t checksum);
uint8_t send_packet(uint32_t* packet_addr);
int8_t reack_ack();

//System command prototypes
uint8_t gen_img(void);

#endif