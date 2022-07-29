import serial
from time import sleep
import crc16
# from functools import reduce
# from operator import xor
# import json
# import itertools
# from datetime import date
# # from lib.database import Postgres
# from modules.lib import logs
# from pathlib import Path


# with open(configPath+'config.json') as config_file:
# def ser_obj():
#     return serial.Serial('COM7', baudrate=9600, bytesize=7,
#                          parity=serial.PARITY_EVEN, stopbits=2, timeout=0.5)


def ser_obj(line: int):
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


if __name__ == "__main__":
    import itertools
    line = 211
    # register_list = ['23', '24', '25', '26',
    #                  '27', '28', '31', '32', 'AC',
    #                  'AD']
    register_list = ['24', '3F']
    register_dict = {'23': 'freq_ref',
                     '24': 'output_freq',
                     '25': 'output_Vref',
                     '26': 'output_I',
                     '27': 'output_W',
                     '28': 'T_ref',
                     '31': 'Vdc',
                     '32': 'T_monitor',
                     'AC': 'motor_speed_rpm',
                     'AD': 'motor_speed_percent',
                     '3F': 'output_freq'}
    commands = [crc16.get_command(7, i) for i in register_list]
    # commands_list = [crc16.get_command(i, j) for i, j in itertools.product(range(4, 9), register_list)]
    ser = ser_obj(line)
    ser.open()
    for i in range(4):
        ser.readline()
    ser.reset_input_buffer()
    for i in commands:
        print(i.hex())
        ser.write(i)
        sleep(0.3)
        ans = ser.read(7)
        print(ans.hex())
    ser.close()
