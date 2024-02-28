/*
 * spi_cmx994.h
 *
 *  Created on: Nov 19, 2023
 *      Author: Asus
 */

#ifndef SPI_CMX994_H_
#define SPI_CMX994_H_

#include <stdint.h> 										/// Include to get precision types (ex. uint8_t)
#include "stm32l4xx_hal.h"									/// Include to get acces to HAL_handleTypeDef variables

#define MAX_NUM_REGISTERS							14		/// Number of write/read only registers in CMX994AQ4

extern uint8_t REGISTER_VALUES[MAX_NUM_REGISTERS]; 			/// Buffer to store readed value's from all CMX994AQ4 registers


/*
 * WRITE ONLY REGISTERS
 */

#define GENERAL_RESET_REGISTER_W  					0x10 	/// A command to this register resets the device and clears all bits of all registers.

#define GENERAL_CONTROL_REGISTER_W  				0x11 	/// This register controls general features such as powersave
#define RX_CONTROL_REGISTER_W  						0x12	/// This register controls general features of the receiver such as Powersave
#define RX_OFFSET_REGISTER_W						0x13   	/// I/Q DC offset correction; see section 6.2.1 for further details. The step size can be doubled using the Rx Control Register ($12), b2; see section 7.3.1.
#define LNA_IM_CONTROL_REGISTER_W					0x14 	/// This register controls features of the receiver that support intermodulation optimisation.
#define OPTIONS_CONTROL_REGISTER_W					0x15	/// This register controls options features added in the CMX994A.
#define RX_GAIN_REGISTER_W							0x16	/// This register controls receiver gain control.
#define EXTENDED_RX_OFFSET_REGISTER_W				0x17	/// the bits in registers $13 and $17 control the same hardware functions with the most recent write to $17 or $13 being applicable at any given time

#define PLL_M_DIVIDER_REGISTER_1_W					0x20	/// These registers set the M divider value for the PLL (Feedback Divider). The divider is updated synchronously
#define PLL_M_DIVIDER_REGISTER_2_W					0x21	/// when register $22 is written so registers $20 and $21 should be written before $22.
#define PLL_M_DIVIDER_REGISTER_3_W					0x22

#define PLL_R_DIVIDER_REGISTER_1_W					0x23 	/// These registers set the R divider value for the PLL (Reference Divider). The PLL dividers are updated
#define PLL_R_DIVIDER_REGISTER_2_W					0x24	/// synchronously when $24 is written. Note: $23 should be written first then $24.

#define VCO_CONTROL_REGISTER_W						0x25 	/// This register controls the operation of the VCO and LO input.


/*
 * READ ONLY REGISTERS
 */

#define GENERAL_CONTROL_REGISTER_R					0xE1  	/// This read-only register mirrors the value in register $11
#define RX_CONTROL_REGISTER_R  						0xE2	///	This read-only register mirrors the value in register $12
#define RX_OFFSET_REGISTER_R						0xE3   	/// This read-only register mirrors the value in register $13
#define LNA_IM_CONTROL_REGISTER_R					0xE4	/// This read-only register mirrors the value in register $14
#define OPTIONS_CONTROL_REGISTER_R					0xE5	/// This read only register mirrors the value in register $15
#define RX_GAIN_REGISTER_R							0xE6 	///	This read only register mirrors the value in register $16
#define EXTENDED_RX_OFFSET_REGISTER_R				0xE7	/// This read-only register mirrors the value in register $17

#define PLL_M_DIVIDER_REGISTER_1_R					0xD0	/// This read-only register mirrors the value in register $20
#define PLL_M_DIVIDER_REGISTER_2_R					0xD1	/// This read-only register mirrors the value in register $21
#define PLL_M_DIVIDER_REGISTER_3_R					0xD2	/// This read-only register mirrors the value in register $22

#define PLL_R_DIVIDER_REGISTER_1_R					0xD3 	/// This read-only register mirrors the value in register $23
#define PLL_R_DIVIDER_REGISTER_2_R					0xD4 	/// This read-only register mirrors the value in register $24

#define VCO_CONTROL_REGISTER_R						0xD5 	/// This read-only register mirrors the value in register $12


/**
 *
 * @param
 *
 * @return void
 */
void reset_registers(SPI_HandleTypeDef* hspi);


/**
 *
 * @param
 * @param
 * @param
 *
 * @return void
 */
void write_to_register(SPI_HandleTypeDef* hspi,uint8_t register_address, uint8_t data);




/**
 *
 * @param
 * @param
 * @param
 *
 * @return void
 */
void write_to_register_16(SPI_HandleTypeDef* hspi,uint8_t register_address, uint16_t register_value);


/**
 *
 * @param
 * @param
 * @param
 *
 * @return void
 */
void read_from_register(SPI_HandleTypeDef* hspi,uint8_t register_address,uint8_t *register_buffer);


/**
 *
 * @param
 * @param
 * @param
 *
 * @return void
 */
void read_from_register_16(SPI_HandleTypeDef* hspi,uint8_t register_address, uint8_t *register_buffer_1,uint8_t *register_buffer_2);
/**
 *
 * @param
 *
 * @return void
 */
void REGISTER_ALL_Init(SPI_HandleTypeDef* hspi);



/**
 *
 * @param
 * @param
 *
 * @return void
 */
void REGISTER_ALL_Read(SPI_HandleTypeDef* hspi,uint8_t *REGISTER_VALUES);




#endif /* SPI_CMX994_H_ */
