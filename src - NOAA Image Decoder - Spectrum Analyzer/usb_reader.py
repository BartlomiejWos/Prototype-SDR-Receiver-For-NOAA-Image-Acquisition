import usb.core
import usb.util
import threading
import time
import struct
import numpy as np


class USB_READER(threading.Thread):
    def __init__(self,IQ_queue):
        super(USB_READER, self).__init__()

        self.vid = 0x483                    # VID of USB device
        self.pid = 0x5740                   # PID of USB device
        self.endpoint_address = 0x81        # Endpoint address
        self.dev = None                     # Device descriptor
        self.running = False                # Flag to indicate if device was found
        self.buffer_size = 28000            # Buffer size in bytes
        self.adc_offset = 4096              #
        self.IQ_queue = IQ_queue            # Queue to store separate channel values


    def run(self):
        """

        :param

        :return:
        """
        self.dev = usb.core.find(idVendor=self.vid, idProduct=self.pid)   # Find device based on VID and PID

        if self.dev is not None:                #

            self.dev.set_configuration()        # Claim an interface on the device
            self.running = True                 # If true, start reading data

        while self.running:
            try:
                data = (self.dev.read(self.endpoint_address, self.buffer_size, timeout=100))   # Timeout in [ms]
                data = bytearray(data)
                samples = np.array(struct.unpack('h'*10000, data[:20000])) -8192
                self.IQ_queue.put(samples)                                                      # Put IQ channels into queue
                time.sleep(0.1)                                                                 # Sleep for 100 milliseconds (0.1 seconds)
            except usb.core.USBError as error:
                if error.errno == 110:          # Timeout error
                    pass
                else:
                    print("USB error:", error)  # print USB timeout error
                    self.running = False        # Stop reading data

    def stop(self):
        """

        :param

        :return:
        """
        self.running = False
        self.join()  # Wait for the thread to finish
        usb.util.dispose_resources(self.dev)




