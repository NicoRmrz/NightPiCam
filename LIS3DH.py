#!/usr/bin/env python
"""LIS3DH, module for use with a LIS3DH accelerometer

created Mar 27, 2017 OM
work in progress - Dec 15, 2018 OM"""

"""
Copyright 2018 Owain Martin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import time, spidev, sys, smbus

class Accelerometer:

    def __init__(self, mode, i2cAddress = 0x0, spiPort = 0, spiCS = 0):

        self.mode = mode
        self.scale = 2
        self.odr = 50
        self.temperatureOffset = 0        

        if self.mode == 'spi':
            self.spi=spidev.SpiDev()
            self.spi.open(spiPort,spiCS)
            self.spi.max_speed_hz = 4000000
        else:  #i2C
            self.bus = smbus.SMBus(3)
            self.addr = i2cAddress

    def single_access_read(self, reg=0x00):
        """single_access_read, function to read a single data register
        of the LIS3DH"""

        rwBit = 0b1  # read/write bit set to read
        msBit = 0b1  # multiple read/write address increment select bit set to auto increment

        if self.mode == 'spi':
            dataTransfer=self.spi.xfer2([(rwBit<<7)+(msBit<<6)+reg,0])

            # for testing
            #print(hex(reg), hex(dataTransfer[1]),bin(dataTransfer[1]))
            
            return dataTransfer[1]
        
        else: #i2c
            dataTransfer=self.bus.read_byte_data(self.addr,reg)
            return dataTransfer
       

    def single_access_write(self, reg=0x00, regValue=0x0):
        """single_access_write, function to write a single data register
        of the LIS3DH"""

        rwBit = 0b0  # read/write bit set to write
        msBit = 0b1  # multiple read/write address increment select bit set to auto increment

        if self.mode == 'spi':
            dataTransfer=self.spi.xfer2([(rwBit<<7)+(msBit<<6)+reg,regValue])
            # for testing
            #print(bin((rwBit<<7)+(msBit<<6)+reg),hex(reg), hex(regValue), hex(dataTransfer[1]))
            
        else: #i2c
            self.bus.write_byte_data(self.addr, reg, regValue)    

        return

    def twos_complement_conversion(self, msb, lsb):
        """twos_complement_conversion, function to change the 10 bit value
        split across 2 bytes from 2s complement to normal binary/decimal. Also
        the left justification of the 10 bits is removed.

        msb = most significant byte
        lsb = least significant byte"""

        signBit= (msb & 0b10000000)>>7
        msb = msb & 0x7F  # strip off sign bit
        #print('signBit',signBit)

        if signBit == 1:  # negative number        
            x = (msb<<8) + lsb
            x = x^0x7FFF
            x = -(x + 1)
        else: # positive number        
            x = (msb<<8) + lsb

        x = x>>6  # remove left justification of data    

        return x

    def adc_reading(self, channel):
        """adc_reading, function to read one of the accelerometer's onboard
        adc channels"""

        channel = channel - 1

        channelAddress = [(0x08, 0x09), (0x0A, 0x0B), (0x0C, 0x0D)]
        
        adcL = self.single_access_read(channelAddress[channel][0])
        adcH = self.single_access_read(channelAddress[channel][1])        

        adcTotal = self.twos_complement_conversion(adcH, adcL)
        
        return adcTotal

    def axis_enable(self, x='on',y='on',z='on'):
        """axis_enable, function to enable/disable the x, y and z axis"""

        xBit = 0b1   # default value - 'on'
        yBit = 0b1   # default value - 'on'
        zBit = 0b1   # default value - 'on'

        CTRL_REG1 = self.single_access_read(0x20)

        if x == 'off':
            xBit = 0b0

        if y == 'off':
            yBit = 0b0

        if z == 'off':
            zBit = 0b0

        CTRL_REG1 = CTRL_REG1 & 0b11111000
        CTRL_REG1 = CTRL_REG1 | ((zBit<<2) + (yBit<<1) + xBit)

        #print (bin(CTRL_REG1)) # for testing

        self.single_access_write(0x20, CTRL_REG1)

        return 

    def disable_temperature(self, adcOn='on'):
        """disable_temperature, function to disable the on board temperature
        sensor. This sets bit 6 and optionally bit 7 of TEMP_CFG_REG (0x1F)"""       

        TEMP_CFG_REG = self.single_access_read(0x1F)

        adcBit = 0b1  # default value

        if adcOn == 'off':
            adcBit = 0b0

        TEMP_CFG_REG = TEMP_CFG_REG & 0b00111111
        TEMP_CFG_REG = TEMP_CFG_REG | (adcBit<<7)

        #print (bin(TEMP_CFG_REG)) # for testing

        self.single_access_write(0x1F, TEMP_CFG_REG)

        return

    def enable_temperature(self):
        """enable_temperature, function to enable the on board temperature
        sensor. This sets bits 6&7 of TEMP_CFG_REG (0x1F)"""

        self.single_access_write(0x1F, 0xC0) # enable adc's and enable temp sensor

        return

    def interrupt_high_low(self, level='high'):
        """interrupt_high_low, function to set the interrupt pins to either
        active high or active low"""

        CTRL_REG6 = self.single_access_read(0x25)

        if level == 'low':
            highlowBit = 0b1
        else:
            highlowBit = 0b0

        CTRL_REG6 = CTRL_REG6 & 0b11111101
        CTRL_REG6 = CTRL_REG6 | (highlowBit<<1)

        #print (bin(CTRL_REG6)) # for testing

        self.single_access_write(0x25, CTRL_REG6)

        return

    def get_aux_status(self, show=False):
        """get_aux_status, function to return the contents of the
        aux status register (0x07)"""
        
        auxStatus = self.single_access_read(0x07)

        if show == True:
            print('Aux Status (0x07) '+str(bin(auxStatus)))

        return auxStatus

    def get_clickInt_status(self, show=False):
        """get_clickInt_status, function to return the contents of the
        click interrupt status register (0x39)"""
        
        clickInterruptStatus = self.single_access_read(0x39)

        if show == True:
            print('Click Interrupt Status (0x39) '+str(bin(clickInterruptStatus)))

        return clickInterruptStatus

    def get_fifo_status(self, show=False):
        """get_fifo_status, function to return the contents of the
        fifo register (0x2F)"""
        
        fifoStatus = self.single_access_read(0x2F)

        if show == True:
            print('FIFO Status (0x2F) '+str(bin(fifoStatus)))

        return fifoStatus
      

    def get_int1_status(self, show=False):
        """get_int1_status, function to return the contents of the
        interrupt1 status register (0x31)"""
        
        interrupt1Status = self.single_access_read(0x31)

        if show == True:
            print('Interrupt Status (0x31) '+str(bin(interrupt1Status)))

        return interrupt1Status

    def get_status(self, show=False):
        """get_status, function to return the contents of the
        status register (0x27)"""
        
        status = self.single_access_read(0x27)

        if show == True:
            print('Status (0x27) '+str(bin(status)))

        return status

    def get_temperature(self):
        """get_temperature, function to read the accelerometer's onboard
        temperature sensor""" 
        
        tempH = self.single_access_read(0x0D)
        tempL = self.single_access_read(0x0C)

        tempTotal = self.twos_complement_conversion(tempH, tempL)
        tempTotal = tempTotal + self.temperatureOffset

        return tempTotal

    def latch_interrupt(self, latch='on'):
        """latch_interrupt, function to turn the latch feature on interrupt1
        on or off"""

        CTRL_REG5 = self.single_access_read(0x24)

        if latch == 'off':
            latchBit = 0b0
        else:
            latchBit = 0b1

        CTRL_REG5 = CTRL_REG5 & 0b11110111
        CTRL_REG5 = CTRL_REG5 | (latchBit<<3)

        #print (bin(CTRL_REG5)) # for testing

        self.single_access_write(0x24, CTRL_REG5)

        return

    def set_4D(self, enable='on'):
        """set_4D, function to turn 4D detection on or off. This sets
        bit 3 of CTRL_REG5 (0x24)"""

        CTRL_REG5 = self.single_access_read(0x24)

        if enable == 'off':
            enableBit = 0b0
        else:
            enableBit = 0b1

        CTRL_REG5 = CTRL_REG5 & 0b11111011
        CTRL_REG5 = CTRL_REG5 | (enableBit<<2)

        #print (bin(CTRL_REG5)) # for testing

        self.single_access_write(0x24, CTRL_REG5)

        return

    def set_adcOn(self, adcOn='off'):
        """set_adcOn, function to enable/disable the aux 10 bit adc
        converter feature.  This sets bit 7 of TEMP_CFG_REG (0x1F)"""

        TEMP_CFG_REG = self.single_access_read(0x1F)

        adcBit = 0b0  # default value

        if adcOn == 'on':
            adcBit = 0b1

        TEMP_CFG_REG = TEMP_CFG_REG & 0b01111111
        TEMP_CFG_REG = TEMP_CFG_REG | (adcBit<<7)

        #print (bin(TEMP_CFG_REG)) # for testing

        self.single_access_write(0x1F, TEMP_CFG_REG)

        return

    def set_BDU(self, bdu='off'):
        """set_BDU, function to enable/disable the block data update
        feature.  This sets bit 7 of CTRL_REG4 (0x23)"""

        CTRL_REG4 = self.single_access_read(0x23)

        bduBit = 0b0  # default value

        if bdu == 'on':
            bduBit = 0b1

        CTRL_REG4 = CTRL_REG4 & 0b01111111
        CTRL_REG4 = CTRL_REG4 | (bduBit<<7)

        #print (bin(CTRL_REG4)) # for testing

        self.single_access_write(0x23, CTRL_REG4)

        return

    def set_click_config(self, zd=0, zs=1, yd=0, ys=0, xd=0, xs=0):
        """set_click_config, function to set the CLICK_CFG regisiter
        (0x38) options"""

        CLICK_CFG = ((zd<<5) + (zs<<4) +(yd<<3) + (ys<<2) + (xd<<1)
                     + xs)

        #print(hex(CLICK_CFG),bin(CLICK_CFG))  # for testing

        self.single_access_write(0x38, CLICK_CFG)

        return

    def set_click_threshold(self, threshold):
        """set_click_threshold, function to set the click threshold (mg).
        This sets CLICK_THS (0x3A)"""

        threshold = abs(threshold)
        thresholdBits = 0b0      

        if self.scale == 2:
            scaleOffset = 4
        elif self.scale == 4:
            scaleOffset = 5
        elif self.scale == 8:
            scaleOffset = 6
        else: # self.scale == 16
            scaleOffset = 7

        for i in range (6,-1,-1):           

            if threshold >= 2**(i+scaleOffset):
                thresholdBits = thresholdBits | (1<<i)
                threshold = threshold - 2**(i+scaleOffset)

        #print(hex(thresholdBits),bin(thresholdBits)) # for testing

        self.single_access_write(0x3A, thresholdBits)

        return

    def set_click_timelimit(self, duration):
        """set_click_timelimit, function to set the click time limit
        duration (ms). This sets TIME_LIMIT (0x3B)"""

        duration = abs(duration)

        if duration > (float(127000)/float(self.odr)):
            durationBits = 0b01111111

        else:
            durationBits = int((float(duration) / float(1000)) * self.odr)
            durationBits = durationBits & 0b01111111

        #print(bin(durationBits))  # for testing

        self.single_access_write(0x3B, durationBits)

        return

    def set_click_timelatency(self, duration):
        """set_click_timelatency, function to set the click time latency
        duration (ms). This sets TIME_LATENCY (0x3C)"""

        duration = abs(duration)

        if duration > (float(255000)/float(self.odr)):
            durationBits = 0b11111111

        else:
            durationBits = int((float(duration) / float(1000)) * self.odr)
            durationBits = durationBits & 0b11111111

        #print(bin(durationBits))  # for testing

        self.single_access_write(0x3C, durationBits)

        return

    def set_click_timewindow(self, duration):
        """set_click_timewindow, function to set the click time window
        duration (ms). This sets TIME_WINDOW (0x3D)"""

        duration = abs(duration)

        if duration > (float(255000)/float(self.odr)):
            durationBits = 0b11111111

        else:
            durationBits = int((float(duration) / float(1000)) * self.odr)
            durationBits = durationBits & 0b11111111

        #print(bin(durationBits))  # for testing

        self.single_access_write(0x3D, durationBits)

        return

    def set_fifo_mode(self, mode='bypass'):
        """set_fifo_mode, function to set the fifo mode of the accelerometer,
        valid value for mode are; off, bypass, fifo, stream and streamfifo.
        This sets bit 6 of CTRL_REG5 (0x24) and bits 6 & 7 of FIFO_CTRL_REG
        (0x2E)"""

        CTRL_REG5 = self.single_access_read(0x24)
        FIFO_CTRL_REG = self.single_access_read(0x2E)

        enableBit = 0b1 # default value: enable
        modeBits = 0b00 # default value: bypass

        if mode == 'off':
            enableBit = 0b0
        elif mode == 'fifo':
            modeBits = 0b01
        elif mode == 'stream':
            modeBits = 0b10
        elif mode == 'streamfifo':
            modeBits = 0b11 

        CTRL_REG5 = CTRL_REG5 & 0b10111111
        CTRL_REG5 = CTRL_REG5 | (enableBit<<6)
        self.single_access_write(0x24, CTRL_REG5)

        FIFO_CTRL_REG = FIFO_CTRL_REG & 0b00111111
        FIFO_CTRL_REG = FIFO_CTRL_REG | (modeBits<<6)
        self.single_access_write(0x2E, FIFO_CTRL_REG)

        #print(hex(CTRL_REG5),bin(CTRL_REG5))  # for testing
        #print(hex(FIFO_CTRL_REG),bin(FIFO_CTRL_REG))  # for testing

        return

    def set_fifo_threshold(self, threshold):
        """set_fifo_threshold, function to the fifo threshold level.
        This sets bits 0-4 of FIFO_CTRL_REG (0x2E)"""

        FIFO_CTRL_REG = self.single_access_read(0x2E)

        threshold = int(abs(threshold))

        if threshold > 31:
            threshold = 31

        FIFO_CTRL_REG = FIFO_CTRL_REG & 0b11100000
        FIFO_CTRL_REG = FIFO_CTRL_REG | threshold
        self.single_access_write(0x2E, FIFO_CTRL_REG)

        #print(hex(FIFO_CTRL_REG),bin(FIFO_CTRL_REG))  # for testing

        return

    def set_highpass_filter(self, mode, freq, FDS, hpClick, hpIS2, hpIS1):
        """set_highpass_filter, function to set the various high pass filter
        options.  This sets CTRL_REG2 (0x21)

        mode - normal, reference, normalreset, autoreset
        freq - see table 8 of the LIS3DH app note
        FDS (filtered data selection) bypass - on or off """

        if mode == 'normalreset':
            modeBits = 0b0
        elif mode == 'reference':
            modeBits = 0b1
        elif mode == 'autoreset':
            modeBits = 0b11
        else: # mode = 'normal'
            modeBits = 0b10

        freq = int(abs(freq))

        if freq > 0b11:
            freqBits = 0b11
        else:
            freqBits = freq

        CTRL_REG2 = ((modeBits<<6) + (freqBits<<4) + (FDS<<3) + (hpClick<<2)
                     + (hpIS2<<1) +hpIS1)

        #print(bin(CTRL_REG2)) # for testing

        self.single_access_write(0x21, CTRL_REG2)

        return        

    def set_int1_config(self, aoi=1, d6=0, zh=0, zl=0, yh=0, yl=0, xh=0, xl=0):
        """set_int1_config, function to set the INT1_CFG regisiter (0x30) options"""

        INT1_CFG = ((aoi<<7) + (d6<<6) + (zh<<5) + (zl<<4) +(yh<<3) +
                (yl<<2) + (xh<<1) + xl)

        #print(hex(INT1_CFG),bin(INT1_CFG))  # for testing

        self.single_access_write(0x30, INT1_CFG)

        return

    def set_int1_duration(self, duration):
        """set_int1_duration, function to set the minimum interrupt 1 duration (ms).
        This sets INT1_DURATION(0x33)"""

        duration = abs(duration)

        if duration > (float(127000)/float(self.odr)):
            durationBits = 0b01111111

        else:
            durationBits = int((float(duration) / float(1000)) * self.odr)
            durationBits = durationBits & 0b01111111

        #print(bin(durationBits))  # for testing

        self.single_access_write(0x33, durationBits)

        return        

    def set_int1_pin(self, click=0,aoi1=0, aoi2=0, drdy1=0, drdy2=0, wtm=0, overrun=0):
        """set_int1, function to which interrupt signals get pushed to
        the int1 pin. This sets CTRL_REG3 (0x22)"""

        CTRL_REG3 = ((click<<7) + (aoi1<<6) + (aoi2<<5) + (drdy1<<4) +(drdy2<<3) +
                (wtm<<2) + (overrun<<1))

        #print (bin(CTRL_REG3)) # for testing

        self.single_access_write(0x22, CTRL_REG3)

        return
    
    def set_int1_threshold(self, threshold):
        """set_int1_threshold, function to set the interrupt1 threshold (mg).
        This sets INT1_THS (0x32)"""

        threshold = abs(threshold)
        thresholdBits = 0b0      

        if self.scale == 2:
            scaleOffset = 4
        elif self.scale == 4:
            scaleOffset = 5
        elif self.scale == 8:
            scaleOffset = 6
        else: # self.scale == 16
            scaleOffset = 7

        for i in range (6,-1,-1):

            if threshold >= 2**(i+scaleOffset):
                thresholdBits = thresholdBits | (1<<i)
                threshold = threshold - 2**(i+scaleOffset)

        #print(hex(thresholdBits),bin(thresholdBits)) # for testing

        self.single_access_write(0x32, thresholdBits)

        return
        
       

    def set_ODR(self, odr=50, powerMode='normal'):
        """set_ODR, function to set the output data rate (ODR) and the power
        mode (normal, low, or off). This sets bits 3-7 of CTRL_REG1 (0x20)"""

        CTRL_REG1 = self.single_access_read(0x20)

        odrBits = 0b0100  # default value 50Hz
        self.odr = 50     # default value 50Hz
        lowPowerBit = 0b0 # default value 'normal' power mode        

        odrOptions = [(1,0b0001),(10,0b0010),(25,0b0011),(50,0b0100),
                      (100,0b0101),(200,0b0110),(400,0b0111),(1600,0b1000),
                      (1250,0b1001),(5000,0b1001)]

        for dataRate in odrOptions:
            if dataRate[0] == odr:
                odrBits = dataRate[1]
                self.odr = dataRate[0]

        if powerMode == 'off':
            odrBits = 0b0000

        elif powerMode == 'low':
            lowPowerBit = 0b1

        CTRL_REG1 = CTRL_REG1 & 0b00000111
        CTRL_REG1 = CTRL_REG1 | ((odrBits<<4) + (lowPowerBit<<3))

        #print (bin(CTRL_REG1)) # for testing

        self.single_access_write(0x20, CTRL_REG1)

        return

    def set_resolution(self, res='low'):
        """set_resolution, function to set the accelerometer resolution
        to either high or low.  This sets bit 3 of CTRL_REG4 (0x23)"""

        CTRL_REG4 = self.single_access_read(0x23)

        resBit = 0b0  # default value: low

        if res == 'high':
            resBit = 0b1

        CTRL_REG4 = CTRL_REG4 & 0b11110111
        CTRL_REG4 = CTRL_REG4 | (resBit<<3)

        #print (bin(CTRL_REG4)) # for testing

        self.single_access_write(0x23, CTRL_REG4)

        return

    def set_scale(self, scale=2):
        """set_scale, function to set the scale used by the
        accelerometer; +-2g, 4g, 8g, 16g"""

        CTRL_REG4 = self.single_access_read(0x23)

        scaleBits = 0b00  # default value
        self.scale = 2

        if scale == 4:
            scaleBits = 0b01
            self.scale = 4
        elif scale == 8:
            scaleBits = 0b10
            self.scale = 8
        elif scale == 16:
            scaleBits = 0b11
            self.scale = 16

        CTRL_REG4 = CTRL_REG4 & 0b11001111
        CTRL_REG4 = CTRL_REG4 | (scaleBits<<4)

        #print (bin(CTRL_REG4)) # for testing

        self.single_access_write(0x23, CTRL_REG4)

        return

    def set_temperature_offset(self, offset):
        """set_temperature_offset, function to set the temperature
        offset value"""

        self.temperatureOffset = offset

        return

    def x_axis_reading(self):
        """x_axis_reading, function to read the x axis accelerometer value"""

        # output in 2s complement
        xH = self.single_access_read(0x29)
        xL = self.single_access_read(0x28)

        xTotal = self.twos_complement_conversion(xH, xL)

        #print (bin(xH),bin(xL),bin(xTotal), xTotal)
        
        return xTotal

    def y_axis_reading(self):
        """y_axis_reading, function to read the y axis accelerometer value"""

        # output in 2s complement
        yH = self.single_access_read(0x2B)
        yL = self.single_access_read(0x2A)

        yTotal = self.twos_complement_conversion(yH, yL)

        #print (bin(yH),bin(yL),bin(yTotal), yTotal)
        
        return yTotal

    def z_axis_reading(self):
        """z_axis_reading, function to read the z axis accelerometer value"""

        # output in 2s complement
        zH = self.single_access_read(0x2D)
        zL = self.single_access_read(0x2C)

        zTotal = self.twos_complement_conversion(zH, zL)

        #print (bin(zH),bin(zL),bin(zTotal), zTotal)
        
        return zTotal

    def __del__(self):
        """__del__, cleanup i2c or SPI connections"""

        self.set_ODR(odr=50, powerMode='off') # put the accel in power down mode

        if self.mode == 'spi':    
            self.spi.close()
        else:  #i2C    
            self.bus.close()



   
    
    
    
