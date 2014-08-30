/*
mh-twi.c  :  I2C (TWI) Communication functions for Atmega32 on MicroHOPE
SDA on PC4 ---> 27 (pin-number)
SCL on PC5 ---> 28 (pin-number)
** SDA - Serial Data Line
** SCA - Serial Clock Line
Author  :  Arun Jayan, GNU USERS NETWORK (GUN)
Email ID:  <arunjayan32gmail.com>,<arun.jayan.j@ieee.org>
Licence :  GNU General Public License  version 3 or above
Date :  5-Feb-2014
*/

#include <avr/io.h>
#define fcpu 16000000L   		// run cpu at 16Mhz
/*
 * I2C_init() is to initiate I2C communication 
 * we gave fscl as argument (ie., scl frequency)
 * example :
 * 			if scl if 400khz then TWBR(Bit rate register) should be 12 or 0xoc
 * 			SCL Freq is find using Equation :
 * 									 SCL Freq = CPU Freq/(16+2(TWBR).Prescalar Value)
 * 			SCL Freq = fscl
 * 			CPU Freq = fcpu
 * 		So from the above equation we can find corresponding TWBR value for specific SCL Freq
 * 		TWBR = ((fcpu/fscl)-16)/2
 * 		in above example fscl = 400khz and fcpu = 16Mhz 
 *  	so TWBR = ((16/.4)-16)/2 = (40-16)/2 = 24/2 = 12(or 0x0C)
 * 		if fscl is 100 khz TWBR will be 72
 * */
void I2C_init(uint8_t fscl)
{
	TWSR = 0;	//set prescalar to zero		
	TWBR = ((fcpu/fscl)-16)/12;	//set SCL frequency in TWI Bit Register
	TWCR = (1<<TWEN);	//enable TWI ; TWCR - TWI Controll Register
}
void I2C_start()
{
	TWCR = (1<<TWINT)|(1<<TWSTA)|(1<<TWEN);
/*TWINT,TWSTA, and TWEN bits of the control register is enabled. These bits enable the TWI interrupt,     
 the start-condition, and the whole TWI module */
	while  ((TWCR & (1<<TWINT)) == 0);
}
//sends stop signal 
void I2C_stop()
{
	TWCR = (1<<TWINT)|(1<<TWSTO)|(1<<TWEN);
}
void I2C_Write(uint8_t data)
{
	TWDR = data; 	
	/*
	 * It writes data byte to TWDR which is shifted to SDA line .
	 * */
	TWCR = (1<<TWINT)|(1<<TWEN);
	while  ((TWCR & (1<<TWINT)) == 0);
}
