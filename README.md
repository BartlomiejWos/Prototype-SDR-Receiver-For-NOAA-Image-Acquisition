# Data acquisition from the NOAA meteoroligal satellite using DIY radio prototype based on the idea of Software Defined Radio (SDR) - Engineering Thesis Project   

## The purpose of this project was to design and fabricate a receiver, based on the idea of SDR, with appropriate software, to acquire weather images from NOAA's satellites (operating at 137 MHz).

This project is an example showing you how to create simple SDR receiver for narrowband applications. Parts of the project shows how do the following: 
* Create a radio front-end PCB using Direct Conversion Receiver (DCR) Integrated Circuit CMX994, MAX2607 (Local Oscillator - LO) and ADL5611 (LO amplifier).
* Analog-to-digital processing and interface handling using STM32.
* Creation of software application enabling the observation of the spectrum of received signals and signal processing to decode the received data into an image.
* All steps have been detailed in the engineering thesis in the Polish language.

## Complete Device:
![sdr](https://github.com/BartlomiejWos/Prototype-SDR-Receiver-For-NOAA-Image-Acquisition/assets/161388878/d6cecb45-81b8-405c-be6d-85b31180e8e5)

## Software written in python for spectral analysis and signal recording:
![gui](https://github.com/BartlomiejWos/Prototype-SDR-Receiver-For-NOAA-Image-Acquisition/assets/161388878/ca0806d9-ff2d-4afc-9d41-fdea74770b2c)

## NOAA image decoder:
![decoder](https://github.com/BartlomiejWos/Prototype-SDR-Receiver-For-NOAA-Image-Acquisition/assets/161388878/53a9c1eb-d77c-44a0-8751-ac79685338e6)

## PCB layout of radio front-end:
![layout](https://github.com/BartlomiejWos/Prototype-SDR-Receiver-For-NOAA-Image-Acquisition/assets/161388878/d8540fe4-c1b8-4f02-a3b0-5488f69d04fc)
