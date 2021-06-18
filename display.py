def send_command(ser, cmd):
    print("Sending command: " + cmd.decode('utf-8'))
    ser.write(b"C:" + cmd + b"\n")

def send_data(ser, data, clear=False):
    if clear:
        send_command(ser, b"CLEAR")

    print("Sending data: " + data.decode('utf-8'))
    ser.write(data + b"\n")

def send_header(ser, data, clear=False):
    if clear:
        send_command(ser, b"CLEAR")

    print("Sending header data: " + data.decode('utf-8'))
    ser.write(b"D0:" + data + b"\n")

def send_content(ser, data, clear=False):
    if clear:
        send_command(ser, b"CLEAR")

    print("Sending content data: " + data.decode('utf-8'))
    ser.write(b"D1:" + data + b"\n")
