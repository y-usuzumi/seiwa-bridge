import time
from io import BytesIO
import traceback
import consts
import hid as pyhid
import display


def sync_status(dev):
    dev.write(b"K:SYN\n")

def get_inputs():
    bio = BytesIO()
    while True:
        print("Probing:")
        yield b"S:DEVICE:PROBE"

        try:
            # Enumerate HID devices to find the one with designated usage page + usage
            devices = pyhid.enumerate(consts.VENDOR_ID, consts.PRODUCT_ID)
            dev_send_info = dev_recv_info = None
            dev_send = dev_recv = None
            for dev in devices:
                if (dev['usage_page'], dev['usage']) == (consts.USAGE_PAGE_SEND, consts.USAGE_SEND):
                    dev_send = dev
                elif (dev['usage_page'], dev['usage']) == (consts.USAGE_PAGE_RECEIVE, consts.USAGE_RECEIVE):
                    dev_recv = dev

            if dev_send is None or dev_recv is None:
                time.sleep(1)
                continue

            print("Opening sending dev (path: %s, usage page: %s, usage: %s)" % (dev_send['path'], dev_send['usage_page'], dev_send['usage']))
            dev_send = pyhid.Device(path=dev_send['path'])
            # dev_send = pyhid.Device(vid=dev_send['vendor_id'], pid=dev_send['product_id'])

            print("Opening receiving dev (path: %s, usage page: %s, usage: %s)" % (dev_recv['path'], dev_recv['usage_page'], dev_recv['usage']))
            dev_recv = pyhid.Device(path=dev_recv['path'])
            # dev_recv = pyhid.Device(vid=dev_recv['vendor_id'], pid=dev_recv['product_id'])
        except pyhid.HIDException as ex:
            print(ex)
            if dev_send is not None:
                dev_send.close()
            if dev_recv is not None:
                dev_recv.close()
            time.sleep(1)
            continue

        print("Device OK")
        yield b"S:DEVICE:OK"


        print("Syncing status from keyboard...")
        sync_status(dev_send)

        print("Listening:")

        bio = BytesIO()
        try:
            while True:
                s = dev_recv.read(64)
                for ch in s:
                    b = bytes([ch])
                    if b != b'\n' and b != b'\x00':
                        bio.write(b)
                    elif bio.getvalue():
                        yield bio.getvalue()
                        bio = BytesIO()
        except pyhid.HIDException as ex:
            traceback.print_exc()
        finally:
            dev_recv.close()
            dev_send.close()
