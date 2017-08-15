import usb.core
import usb.util


class PyUSB:
    """
    This class provides basic functions to access
    a USB HID device using pyusb to write an endpoint
    """

    def __init__(self):
        self.dev = usb.core.find(idVendor=0x2886)

        # get active config
        config = self.dev.get_active_configuration()

        # iterate on all interfaces:
        #    - if we found a HID interface
        for interface in config:
            if interface.bInterfaceClass == 0x03:
                interface_number = interface.bInterfaceNumber
                break

        try:
            if self.dev.is_kernel_driver_active(interface_number):
                self.dev.detach_kernel_driver(interface_number)
        except Exception as e:
            print(e)

        ep_in, ep_out = None, None
        for ep in interface:
            if ep.bEndpointAddress & 0x80:
                ep_in = ep
            else:
                ep_out = ep

        self.ep_in = ep_in
        self.ep_out = ep_out
        self.interface_number = interface_number

    def write(self, data):
        """
        write data on the OUT endpoint associated to the HID interface
        """

        # report_size = 64
        # if self.ep_out:
        #     report_size = self.ep_out.wMaxPacketSize
        #
        # for _ in range(report_size - len(data)):
        #    data.append(0)

        if not self.ep_out:
            bmRequestType = 0x21              # Host to device request of type Class of Recipient Interface
            bmRequest = 0x09              # Set_REPORT (HID class-specific request for transferring data over EP0)
            wValue = 0x200             # Issuing an OUT report
            wIndex = self.interface_number  # SeeedStudio ReSpeaker interface number for HID
            self.dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, data)

        self.ep_out.write(data)


    def read(self):
        return self.ep_in.read(self.ep_in.wMaxPacketSize, -1)


    def close(self):
        """
        close the interface
        """
        usb.util.dispose_resources(self.dev)



if __name__ == '__main__':
    import signal
    import time

    is_quit = False
    def handler(signum, frame):
        global is_quit
        is_quit = True
        print 'quit'

    signal.signal(signal.SIGINT, handler)

    hid = PyUSB()

    data = None
    while not is_quit:
        new_data =  hid.read()
        if len(new_data) == 64 and data != new_data:
            data = new_data
            #print [int(c) for c in data]
            vad = data[4]
            direction = int(data[5]) + (int(data[6]) << 8)
            print 'vad: {}, direction: {}'.format(vad, direction)