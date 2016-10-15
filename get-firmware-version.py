import sys
import time
import uuid
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import DeviceInformation

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()


def main(nuimo_uuid):
    print nuimo_uuid
    # Clear previously received data from the controller/adapter
    ble.clear_cached_data()

    # Connect to the default or first adapter and start scan
    adapter = ble.get_default_adapter()
    adapter.power_on()
    adapter.start_scan()

    # It needs bit of time to scan the devices. Some Peripherals advertise in different
    time.sleep(2)

    # Find all the ble devices with the name nuimo,this filtering part is done by Adafruit
    # devices -> interfaces/device/bluez-device, properties and method can be found there
    # id is MAC on Linux and on OSX uuid generated by OSX
    devices = ble.find_devices()

    for device in devices:
        print('Found device: {0}, id: {1}'.format(device.name, device.id))

        if device.id == uuid.UUID(nuimo_uuid):
            device.connect()
            DeviceInformation.discover(device)
            dis = DeviceInformation(device)
            print('Firmware Revision: {0}'.format(dis.fw_revision))
            device.disconnect()

    adapter.power_off()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter UUID of Nuimo")
        sys.exit()

    ble.initialize()
    ble.run_mainloop_with(main(sys.argv[1]))
