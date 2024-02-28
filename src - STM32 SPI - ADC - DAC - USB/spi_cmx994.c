/*
 * spi_cmx994.c
 *
 *  Created on: Nov 19, 2023
 *      Author: Asus
 */

#include "spi_cmx994.h"
#include "main.h"


uint8_t REGISTER_VALUES[MAX_NUM_REGISTERS];			 		/// Buffer to store readed value's from all CMX994AQ4 registers



void reset_registers(SPI_HandleTypeDef* hspi){
	/**
	 *
	 *
	 */

	uint8_t tx_data[1];
	tx_data[0] = GENERAL_RESET_REGISTER_W;

	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin, GPIO_PIN_RESET); /// CS pin low - start SPI transmission
	HAL_SPI_Transmit(hspi, tx_data, 1, HAL_MAX_DELAY);		/// Transmit data
	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin, GPIO_PIN_SET);   /// CS pin high - end SPI transmission

}

void write_to_register(SPI_HandleTypeDef* hspi,uint8_t register_address, uint8_t register_value){
	/**
	 *
	 *
	 */

	uint8_t tx_data[2];

	tx_data[0]=register_address;
	tx_data[1]=register_value;

	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin,GPIO_PIN_RESET); /// CS pin low - start SPI transmission
	HAL_SPI_Transmit(hspi, tx_data, 2, HAL_MAX_DELAY); 	   /// Transmit data
	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin, GPIO_PIN_SET);  /// CS pin high - end SPI transmission

}

void write_to_register_16(SPI_HandleTypeDef* hspi,uint8_t register_address, uint16_t register_value){
	/**
	 *
	 *
	 */

	uint8_t tx_data[3];

	tx_data[0]=register_address;
	tx_data[1] = (uint8_t)(register_value & 0xFF);        // Lower 8 bits
	tx_data[2] = (uint8_t)((register_value >> 8) & 0xFF); // Upper 8 bits

	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin,GPIO_PIN_RESET); /// CS pin low - start SPI transmission
	HAL_SPI_Transmit(hspi, tx_data, 3, HAL_MAX_DELAY); 	   /// Transmit data
	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin, GPIO_PIN_SET);  /// CS pin high - end SPI transmission

}



void read_from_register(SPI_HandleTypeDef* hspi,uint8_t register_address, uint8_t *register_buffer){
	/**
	 *
	 *
	 */


	uint8_t tx_data[2];
	uint8_t rx_data[2];

	tx_data[0] = register_address;
	tx_data[1]= 0x00;

	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin,GPIO_PIN_RESET); 		   /// CS pin low - start SPI transmission
	HAL_SPI_TransmitReceive(hspi,tx_data,rx_data,2,HAL_MAX_DELAY); /// Transmit and receive data
	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin, GPIO_PIN_SET);	 	   /// CS pin high - end SPI transmission

	*register_buffer=rx_data[1];

}

void read_from_register_16(SPI_HandleTypeDef* hspi,uint8_t register_address, uint8_t *register_buffer_1,uint8_t *register_buffer_2){
	/**
	 * This function initiates a read operation from the CMX994 device by providing the register
	 * address. It reads a 16-bit value from the specified register address and stores the two
 	 * bytes in the provided register_buffer_1 and register_buffer_2 pointers.
	 *
	 */


	uint8_t tx_data[2];
	uint8_t rx_data[3];

	tx_data[0] = register_address;
	tx_data[1]= 0x00;

	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin,GPIO_PIN_RESET); 		   /// CS pin low - start SPI transmission
	HAL_SPI_TransmitReceive(hspi,tx_data,rx_data,3,HAL_MAX_DELAY); /// Transmit and receive data
	HAL_GPIO_WritePin(CS_GPIO_Port,CS_Pin, GPIO_PIN_SET);	 	   /// CS pin high - end SPI transmission

	*register_buffer_1=rx_data[1];
	*register_buffer_2=rx_data[2];

}


void REGISTER_ALL_Init(SPI_HandleTypeDef* hspi){
    /**
	 *This function sets the registers of the CMX994 device to predefined values to
	 * configure it for a specific operation. It includes configurations for General Control,
	 * RX Control, RX Offset, LNA IM Control, Options Control, RX Gain, Extended RX Offset,
	 * PLL M Divider, PLL R Divider, and VCO Control registers.
	 */

	reset_registers(hspi);											 	 /// Resets the device and clears all bits of all registers.

	write_to_register(hspi,GENERAL_CONTROL_REGISTER_W,		0x8A); /// 7-En Bias=1, 6-Freq2=0, 5-Freq1=0, 4-LP=0, 3-VCOEN=1, 2-PLLEN=0, 1-RXEN=1, 0-TXEN=0
	write_to_register(hspi,RX_CONTROL_REGISTER_W,			0b00010000); /// 7-Mix Pwr=0, 6-IQ Pwr=0, 5=LNA Pwr=0, 4-ACR FLt2=0, 3-ACR Flt1=1, 2-DC Range=0, 1-DIV2=0, 1-DIV1=0
	write_to_register(hspi,RX_OFFSET_REGISTER_W,			0b00000000); /// 7-QDC3=0, 6-QDC2=0, 5-QDC1=0, 4-QDC0=0, 3-IDC3=0, 2-IDC2=0, 1-IDC1=0, 0-IDC0=0
	write_to_register(hspi,LNA_IM_CONTROL_REGISTER_W,		0b00000000); /// 7-reserved=0, 6-reserved=0, 5-IM5=0, 4-IM4=0, 3-IM3=0, 2-IM2=0, 1-IM1=0, 0-IM0=0

	write_to_register(hspi,OPTIONS_CONTROL_REGISTER_W,		0b00000000); /// 7-IPX3=0, 6-reserved=0, 5-reserved=0, 4-reserved=0, 3-PDQ=0, 2-PDI=0, 1-PHCON=0, 0-PHOFF=0 MOŻNA DAĆ 1 i zobaczyć
	write_to_register(hspi,RX_GAIN_REGISTER_W,				0b00000000); /// 7-GS1=0, 6-GS0=0, 5-LNAG2=0, 4-LNAG1=0, 3-LNAZ0=0, 2-G2=0, 1-G1=0, 0-G0=0 // MOŻNA PODBIĆ GAINA i i zmienić Z0 , VGA wychodzi na MAX

	write_to_register_16(hspi,EXTENDED_RX_OFFSET_REGISTER_W,0b0000000000000000); /// No DC correction applied

	write_to_register(hspi,PLL_M_DIVIDER_REGISTER_1_W,		0b00000000); /// PLL unused
	write_to_register(hspi,PLL_M_DIVIDER_REGISTER_2_W,		0b00000000); /// PLL unused
	write_to_register(hspi,PLL_M_DIVIDER_REGISTER_3_W,		0b00000000); /// PLL unused

	write_to_register(hspi,PLL_R_DIVIDER_REGISTER_1_W,		0b00000000); /// PLL unused
	write_to_register(hspi,PLL_R_DIVIDER_REGISTER_2_W,		0b00000000); /// PLL unused

	write_to_register(hspi,VCO_CONTROL_REGISTER_W,			0b01110000); /// 7-FILT_CAL=0, 6-TXDIV1=1, 5-TXDIV0=1, 4-LO_INPUT_EN=1, 3=VCO_NR2=0, 2-VC0_NR1=0, 1-VCO_NR_En=0, 0-VCO_Buf_En=0


}


void REGISTER_ALL_Read(SPI_HandleTypeDef* hspi,uint8_t *REGISTER_VALUES){
	/**
	 *
	 *
	 */

	read_from_register(hspi,GENERAL_CONTROL_REGISTER_R,	   &REGISTER_VALUES[0]); 	///
	read_from_register(hspi,RX_CONTROL_REGISTER_R,		   &REGISTER_VALUES[1]); 	///
	read_from_register(hspi,RX_OFFSET_REGISTER_R,		   &REGISTER_VALUES[2]); 	///
	read_from_register(hspi,LNA_IM_CONTROL_REGISTER_R,	   &REGISTER_VALUES[3]); 	///

	read_from_register(hspi,OPTIONS_CONTROL_REGISTER_R,	   &REGISTER_VALUES[4]); 	///
	read_from_register(hspi,RX_GAIN_REGISTER_R,			   &REGISTER_VALUES[5]); 	///

	read_from_register_16(hspi,EXTENDED_RX_OFFSET_REGISTER_R, &REGISTER_VALUES[6],&REGISTER_VALUES[7]); ///

	read_from_register(hspi,PLL_M_DIVIDER_REGISTER_1_R,	   &REGISTER_VALUES[8]); 	///
	read_from_register(hspi,PLL_M_DIVIDER_REGISTER_2_R,	   &REGISTER_VALUES[9]); 	///
	read_from_register(hspi,PLL_M_DIVIDER_REGISTER_3_R,	   &REGISTER_VALUES[10]); 	/// 2 Only write ‘0’ to b4 and b2 of $22 (when read via $D2, these show the device type) B4=0 B2=1 (for CMX994A -return 4)

	read_from_register(hspi,PLL_R_DIVIDER_REGISTER_1_R,	   &REGISTER_VALUES[11]); 	///
	read_from_register(hspi,PLL_R_DIVIDER_REGISTER_2_R,	   &REGISTER_VALUES[12]); 	///

	read_from_register(hspi,VCO_CONTROL_REGISTER_R,		   &REGISTER_VALUES[13]); 	///

}




