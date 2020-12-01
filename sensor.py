import serial


def serial_connection(port, baundrate, timeout=None):
    ser = serial.Serial(
        port=port,
        baudrate=baundrate,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=timeout)
    return ser
