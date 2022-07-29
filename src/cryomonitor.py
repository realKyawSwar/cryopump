#!/usr/bin/env python3
from showa.lib.database import Postgres
from showa.modules import modbus, config
from showa.lib import logs
# from time import sleep


def upload_data(data: tuple) -> None:
    '''Upload modbus data

    Arguments:
        data {tuple} -- [description]
    '''
    try:
        myPg = None
        myPg = Postgres("128.53.1.71/5432", "spt_db", "spt_admin",
                        "sptadmin")
        myPg.connect()
        print("Connection succeeded for cryopump..")
        strSQL = f"INSERT INTO eqt_data_monitor.cryopump values {data}"
        myPg.execute(strSQL)
        myPg.commit()
    except Exception as err:
        logs.logError(f"Upload Error :{str(err)}",
                      includeErrorLine=True)
    finally:
        if myPg is not None:
            myPg.close()


def greetings(ser) -> None:
    """Catch greetings from console server"""

    ser.open()
    for readback in range(5):
        ser.readline()
    ser.reset_input_buffer()


if __name__ == '__main__':
    logs.initLogger(logLevel=logs.LEVEL_DEBUG)
    in_ope = config.in_ope
    # print(in_ope)
    for line, chambers_ in in_ope.items():
        ser = modbus.ser_obj(line)
        greetings(ser)
        status = modbus.check_drive_status(chambers_[0], ser)
        # print(status)
        if status != 'stop':
            for pump in chambers_:
                try:
                    print(pump)
                    result = modbus.get_data(line, pump, ser)
                    print(result)
                    upload_data(result)
                except Exception as err:
                    logs.logError(f"Line {line} Chamber {pump}: {str(err)}",
                                  includeErrorLine=True)
                    print(err)
        elif status == 'stop':
            logs.logInfo(f"Line {line} is stopped.")
            print(f"Line {line} is stopped.")
        else:
            logs.logError(f"L{line} error encountered with {status}",
                          includeErrorLine=False)
            print(f"L{line} error encountered with {status}")
    logs.closeLogger()
