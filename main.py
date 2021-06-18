import time
import serial
import hid_listen
import display
import threading
from message import MessageHandler
from ui import UI
from env import get_env


def arduino_run(ser, mh):
    while True:
        msg = ser.read_until()[:-1]
        print(b"Handling Arduino message: %s" % msg)
        mh.handle_msg(msg)

def hid_run(mh):
    for msg in hid_listen.get_inputs():
        print(b"Handling HID message: %s" % msg)
        mh.handle_msg(msg)


def main():
    with serial.Serial('/dev/ttyACM0', 119200, timeout=5) as ser:
        env = get_env()
        ui = UI(ser, env)
        mh = MessageHandler(env, ui)

        # Shake hands
        while True:
            display.send_command(ser, b"PING")
            if (is_ready := ser.read_until()) != b"PONG\n":
                print(is_ready)
                print("Serial not ready. Retrying.")
            else:
                print("Serial ready!")
                break

        t_arduino = threading.Thread(target=arduino_run, args=(ser,mh), daemon=True)
        t_hid = threading.Thread(target=hid_run, args=(mh,), daemon=True)
        t_arduino.start()
        t_hid.start()
        t_arduino.join()
        t_hid.join()
    ser.close()


if __name__ == '__main__':
    main()


