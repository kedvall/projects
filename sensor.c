// This library is for R30X Fingerprint Sensors
// It was written for the R301, but should for work any R30X sensor

//Fingerprint Sensor related functions
uint8_t gen_img(void)
{
	packet_addr = form_packet(CMD_PKT, 0x03, F_GEN_IMG, 0x05);
	send_packet(packet_addr);
	read_ack();
}


// Utility commands
uint32_t form_packet(uint8_t packet_id, uint16_t packet_len, uint8_t packet_data, uint16_t checksum)
{
	int i;
	packet_t packet;
	packet.header = HEADER;
	packet.addr = ADDR;
	packet.packet_id = packet_id;
	packet.packet_len = packet_len;
	packet.packet_data = packet_data;
	packet.checksum = checksum;

	return &packet;
}

uint8_t send_packet(uint32_t* packet_addr)
{
	uint8_t bytes_sent;
	bytes_sent = Serial.write(*packet_addr, PACKET_SIZE);

	if (bytes_sent != 96)
		return -1
	return 0;
}

int8_t reack_ack()
{
	int i = 0;
	uint8_t ack_packet[12];

	while (Serial.available() > 0)
		ack_packet[i++] = Serial.read();

	if (ack_packet[0] != 0xEF && ack_packet[1] != 0x01)
		return -1;

	return ack_packet[9];
}
