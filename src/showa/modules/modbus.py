# from showa.lib import logs
from showa.modules import config
# import config
from datetime import datetime
import serial
from time import sleep


class Error(Exception):
    """Base class for other exceptions"""
    pass


class Empyt_reply_error(Error):
    """Raised when b'' is detected."""
    pass


def __calculateCRC(data, numberOfBytes, startByte):
    crc = 0xFFFF
    for x in range(0, numberOfBytes):
        crc = crc ^ data[x]
        for _ in range(0, 8):
            if (crc & 0x0001) != 0:
                crc = crc >> 1
                crc = crc ^ 0xA001
            else:
                crc = crc >> 1
    return crc


def ser_obj(line: int):
    '''Serial object creation function

    create Serial for URL from line number

    Arguments:
        line {int} -- line number

    Returns:
        Serial object --
    '''
    # 'socket://128.53.66.36:5046'
    port_dict = {
                 201: '36', 202: '37', 203: '38',
                 204: '39', 205: '40', 206: '41',
                 207: '42', 208: '43', 209: '44',
                 210: '45', 211: '46'
                 }
    port = port_dict[line]
    _url_ = f'socket://128.53.66.{port}:5044'
    # print(_url_)
    return serial.serial_for_url(
        url=_url_,
        baudrate=19200,
        do_not_open=True,
        bytesize=8,
        parity=serial.PARITY_EVEN,
        stopbits=1, timeout=0.6)


def get_command(__unitIdentifier: int, starting_add: str, ser,
                function_code=3, quantity=1) -> bytearray:
    '''Create modbus command function

    Construct modbus serial commands using station number
    (default function code 3 for reading registers and
    data quantity 1)

    Arguments:
        __unitIdentifier {int} -- pump number
        starting_add {str} -- hex string
        # starting_address = 0x26

    Keyword Arguments:
        function_code {number} -- read register (default: {3})
        quantity {number} -- data 1 byte (default: {1})
    '''
    starting_address = int(starting_add, 16)
    starting_address_lsb = starting_address & 0xFF
    starting_address_msb = (starting_address & 0xFF00) >> 8
    quantity_lsb = quantity & 0xFF
    quantity_msb = (quantity & 0xFF00) >> 8
    data = bytearray([
                      __unitIdentifier, function_code,
                     starting_address_msb, starting_address_lsb,
                     quantity_msb, quantity_lsb, 0, 0
                     ])
    crc = __calculateCRC(data, len(data) - 2, 0)
    crcLSB = crc & 0xFF
    crcMSB = (crc & 0xFF00) >> 8
    data[6] = crcLSB
    data[7] = crcMSB
    # print(data.hex())
    # b'\x05\x03\x00\x26\x00\x01\x64\x45',
    try:
        ser.write(data)
        sleep(0.12)
        ans = ser.read(7)
        print(ans)
        if ans != b'':
            anscrc = __calculateCRC(ans, len(ans) - 2, 0)
            crcLSB = anscrc & 0xFF
            crcMSB = (anscrc & 0xFF00) >> 8
            if (crcLSB != ans[len(ans) - 2]) & (crcMSB != ans[len(ans) - 1]):
                # raise Exceptions.CRCCheckFailedException("CRC check failed")
                print("Error!")
            # print(ans)
            return ans
    except Exception as e:
        print(f'error at get_command {e}')


def decode(slave_reply: bytearray, quantity=1):
    '''Decode funtion

    convert hex reply from slave to integer or float

    Arguments:
        slave_reply {bytearray} -- output from get command function

    Keyword Arguments:
        quantity {number} -- data quantity (default: {1})

    Returns:
        int/float -- decoded result
    '''

    if slave_reply:
        for i in range(0, quantity):
            final_result = (slave_reply[i * 2 + 3] << 8) + slave_reply[i * 2 + 4]
        return final_result


def check_drive_status(pump: int, ser) -> str:
    '''Pump status function

    Checking the register 48 for pump status
    each byte represents the status of the pump

    Arguments:
        pump {int} -- [description]

    Returns:
        int/float -- decoded result
    '''
    register = '4B'
    hex_bytes = get_command(pump, register, ser)
    # print(hex_bytes)
    # reply_length = len(hex_bytes)
    # print(reply_length)
    if not hex_bytes:
        raise Empyt_reply_error("No response from inverter!")
    elif len(hex_bytes) == 7:
        new_bytes = hex_bytes[4:-2]
        hex_value = new_bytes.hex()
        int_value = int(hex_value, base=16)
        # # Convert integer to a binary value
        binary_value = str(bin(int_value))[2:].zfill(8)
        # print(binary_value[-1:])
        if binary_value[-3:] == '001':
            return 'forward'
        elif binary_value[-3:] == '100':
            return 'reverse'
        elif binary_value[-3:] == '010':
            return 'stop'
        else:
            return 'Error!'


def get_data(line: int, pump: str, ser) -> tuple:
    '''Prepare pump data for database upload

    create serial payload
    recieve and decode reply from slave
    averaging results from 15 times of slave replies
    datetime, cryo compressor number, chamber number
    and pump status are initiated berfore data appending.

    Arguments:
        line {int} -- line number
        pump {str} -- chamber number

    Returns:
        tuple -- ('22-07-2022 17:27:00', 207, 'CRC2',
                  'P5', 'forward', 60.0, 9.23, 202.51, 276.5, 0.02)
    '''
    CRC = config.CRC
    register_dict = config.register_dict
    sample_cycles = config.sample_cycles
    status = check_drive_status(pump, ser)
    # print(status)
    if line == 211:
        boo = 0
    else:
        boo = 1
    crc_number = CRC[boo][pump]
    # crc_number = "CRC4"
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mean_list = [date_time, line, crc_number, f'P{pump}', status]
    # if status == 'stop':
    #     mean_list.append(0, 0, 0, 0, 0)
    for register, description in register_dict.items():
        data_list = []
        for i in range(sample_cycles):
            data = decode(get_command(pump, register, ser))
            # print(data)
            if data:
                data_list.append(data*description[0])
        mean_data = sum(data_list) / len(data_list)
        mean_list.append(round(mean_data, 2))
    return tuple(mean_list)


if __name__ == "__main__":
    import itertools
    # # address_list = list(range(4, 9))
    # # for i in range(4, 9):
    # #     for j in register_list:
    # #         print(i, j)
    # # for i, j in itertools.product(range(4, 9), register_list):
    # #     commands = get_command(i, j)
    # #     print(commands)
    # # commands = [get_command(4, i) for i in register_list]
    # # print(commands)
    # commands_list = [get_command(i, j) for i, j in itertools.product(range(4, 9), register_list)]
    # print(commands_list)
    line = 207
    ser = ser_obj(line)
    ser.open()
    for readback in range(5):
        ser.readline()
    ser.reset_input_buffer()
    for pump in [4, 5]:
        result = get_data(line, pump, ser)
        print(result)
