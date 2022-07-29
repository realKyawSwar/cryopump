from abc import ABCMeta, abstractmethod
import pandas as pd
import cx_Oracle
import psycopg2
import pypyodbc
import re


class GenericSQL(object):
    '''
    [summary]
        - A Generic Database Connection Class

    [description]
        - To Simplify The Ease To Code For Connection And Code Execution

    Property:
        server              : Server Information
        database            : Database Name To Connect To
        username            : The UID Of The Connection
        password            : The Password Of The Connection
        connection_string   : The Connection String
    '''
    __metaclass__ = ABCMeta

    def __init__(self, server=None, database=None,
                 username=None, password=None):
        '''
        [summary]
            - Initialize The Database Class With Values

        Keyword Arguments:
            server {string} -- Server To Connect To     (default: {None})
            database {string} -- Database To Connect To (default: {None})
            username {string} -- Username To Connect As (default: {None})
            password {string} -- Password For Username  (default: {None})
        '''
        if (server is None or database is None or
           username is None or password is None):
            self.print_init_message()
            raise TypeError('Not Enough Arguments')
        else:
            self.server = server
            self.database = database
            self.username = username
            self.password = password
            self.connection_string = ''
            self.connection_object = None
            self.cursor_object = None

    @property
    def server(self):
        '''
        [summary]
            - A Property Getter Function To Get The Server Value

        Returns:
            str -- Server Value
        '''
        # Return The Server Value
        return self.__server

    @server.setter
    def server(self, server):
        '''
        [summary]
            - A Property Setter Function To Set The Server Value

        Arguments:
            server {str} -- The Server Value
        '''
        # Check For The Object Type
        if type(server) == str:
            self.__server = server
        else:
            raise TypeError("'server' parameter only accept str")

    @property
    def database(self):
        '''
        [summary]
            - A Property Getter Function To Get The Database Value

        Returns:
            str -- Database Value
        '''
        # Return The Database Value
        return self.__database

    @database.setter
    def database(self, database):
        '''
        [summary]
            - A Property Setter Function To Set The Database Value

        Arguments:
            server {str} -- The Database Value
        '''
        # Check For The Object Type
        if type(database) == str:
            self.__database = database
        else:
            raise TypeError("'database' parameter only accept str")

    @property
    def username(self):
        '''
        [summary]
            - A Property Getter Function To Get The Username Value

        Returns:
            str -- Username Value
        '''
        # Return The Username Value
        return self.__username

    @username.setter
    def username(self, username):
        '''
        [summary]
            - A Property Setter Function To Set The Username Value

        Arguments:
            username {str} -- The Username Value
        '''
        # Check For The Object Type
        if type(username) == str:
            self.__username = username
        else:
            raise TypeError("'username' parameter only accept str")

    @property
    def password(self):
        '''
        [summary]
            - A Property Getter Function To Get The Password Value

        Returns:
            str -- Password Value
        '''
        # Return The Password Value
        return self.__password

    @password.setter
    def password(self, password):
        '''
        [summary]
            - A Property Setter Function To Set The Password Value

        Arguments:
            password {str} -- The Password Value
        '''
        # Check For The Object Type
        if type(password) == str:
            self.__password = password
        else:
            raise TypeError("'password' parameter only accept str")

    @property
    def connection_string(self):
        '''
        [summary]
            - A Property Getter Function To Get The Connection String Value

        Returns:
            str -- Connection String Value
        '''
        # Return The Connection String Value
        return self.__connection_string

    @connection_string.setter
    def connection_string(self, connection_string):
        '''
        [summary]
            - A Property Setter Function To Set The Connection String Value

        Arguments:
            connection_string {str} -- The Connection String Value
        '''
        # Check For The Object Type
        if type(connection_string) == str:
            self.__connection_string = connection_string
        else:
            raise TypeError("'connection_string' parameter only accept str")

    @property
    def connection_object(self):
        '''
        [summary]
            - A Property Getter Function To Get The Connection Object Value

        Returns:
            str -- Connection Object Value
        '''
        # Return The Connection Object Value
        return self.__connection_object

    @connection_object.setter
    def connection_object(self, connection_object):
        '''
        [summary]
            - A Property Setter Function To Set The Connection Object Value

        Arguments:
            connection_object {str} -- The Connection Object Value
        '''
        # Check For The Object Type
        objTypeList = [
                        str,
                        type(None),
                        psycopg2.extensions.connection,
                        pypyodbc.Connection,
                        cx_Oracle.Connection
                      ]
        if any(objType is type(connection_object) for objType in objTypeList):
            self.__connection_object = connection_object
        else:
            raise TypeError(
                (
                    "'connection_object' parameter only accept str, "
                    "psycopg2's connection, cx_Oracle's connection and "
                    "pypyodbc's connection. {}".format(type(connection_object))
                )
            )

    @property
    def cursor_object(self):
        '''
        [summary]
            - A Property Getter Function To Get The Cursor Object Value

        Returns:
            str -- Cursor Object Value
        '''
        # Return The Cursor Object Value
        return self.__cursor_object

    @cursor_object.setter
    def cursor_object(self, cursor_object):
        '''
        [summary]
            - A Property Setter Function To Set The Cursor Object Value

        Arguments:
            cursor_object {str} -- The Cursor Object Value
        '''
        # Check For The Object Type
        curObjList = [
                        type(None),
                        psycopg2.extensions.cursor,
                        cx_Oracle.Cursor,
                        pypyodbc.Cursor
                     ]
        if any(objType is type(cursor_object) for objType in curObjList):
            self.__cursor_object = cursor_object
        else:
            raise TypeError(
                (
                    "'cursor_object' parameter only accept psycopg2's cursor, "
                    "cx_Oracle's cursor and pypyodbc's cursor. "
                    "Given Object: {}".format(
                        type(cursor_object)
                    )
                )
            )

    @abstractmethod
    def print_init_message(self):
        '''
        [summary]
            - Function To Print Information On How To
                Initialize When Error Occurs.

        '''
        pass

    @abstractmethod
    def __generate_connection_string(self):
        '''
        [summary]
            - Function To Generate Out The Connection String
        '''
        pass

    @abstractmethod
    def __get_connection_format(self):
        '''
        [summary]
            - A Function To Get The Database Connection String Format

        Returns:
            str -- The Database Connection String Format
        '''
        pass

    @abstractmethod
    def __get_driver_type(self):
        '''
        [summary]
            - A Function To Return The Driver Type For The Connection String
        '''
        pass

    @abstractmethod
    def __is_complete_info(self):
        '''
        [summary]
            - Check If Data Inserted During Initialize Is Correct

        Returns:
            bool -- [Status On Data Inialize Correctly]
        '''
        pass

    @abstractmethod
    def __cursor_connection_check(self):
        '''
        [summary]
            - A Function To Check For Database Cursor And Connection
        '''
        pass

    @abstractmethod
    def connect(self):
        '''
        [summary]
            - Function To Create Connection To Database
        '''
        pass

    def close(self):
        '''
        [summary]
            - Function To Close Connection To Database
        '''
        try:
            if self.cursor_object is not None:
                self.cursor_object.close()

            if self.connection_object is not None:
                self.connection_object.close()
        except Exception as e:
            raise e

    def commit(self):
        '''
        [summary]
            - A Function To Commit The Transaction On The Database
        '''
        try:
            if self.connection_object is not None:
                self.connection_object.commit()
        except Exception as e:
            raise e

    def rollback(self):
        '''
        [summary]
            - A Function To Rollback The Transaction On The Database
        '''
        try:
            if self.connection_object is not None:
                self.connection_object.rollback()
        except Exception as e:
            raise e

    def set_cursor_obj(self):
        '''
        [summary]
            - A Function To Open Cursor Object
        '''
        if self.cursor_object is None:
            self.cursor_object = self.connection_object.cursor()

    @abstractmethod
    def execute(self, sql, value=None):
        '''
        [summary]
            - Function To Execute Query Such As Insert/Update/Delete/Create
            - Followed by A Commit/Rollback Depends On The Status

        Arguments:
            sql {str} -- Query String That Need To Be Execute
            value {tuple} -- Values Wrap In Tuple

        Returns:
            list -- list of result
        '''
        pass

    @abstractmethod
    def query(self, sql, value=None, returnAsDataFrame=True):
        '''
        [summary]
            - Function To Execute Query Only For Select Statement
            - Return Value As A Pandas Data Frame

        Arguments:
            sql {str} -- Query String That Need To Be Execute

        Returns:
            list of dataframe -- Result Return From Query
        '''
        pass

    def result_to_dataframe(self, resultValue, columnNamePos=0):
        '''
        [summary]
            - A Function To Convert Result Returned By
                Execute/Query Function To DataFrame Type

        Arguments:
            resultValue {dictionary} -- Result Returned

        Returns:
            [type] -- [description]
        '''
        columnValue = []

        for colInfo in resultValue["column"]:
            if type(colInfo) in [tuple, list]:
                columnValue.append(colInfo[columnNamePos].strip())
            else:
                columnValue.append(colInfo.strip())

        if not columnValue:
            columnValue = None

        dataValue = self.__removespace(resultValue["value"])
        df = pd.DataFrame(dataValue, columns=columnValue)
        return df

    def __removespace(self, a):
        '''
        [summary]
            - Function to remove space in json value

        Arguments:
            a {str/list/row/set} -- the value to strip

        Returns:
            str/list/row/set -- value after being strip of the spaces
        '''
        if type(a) is str:
            return a.strip()
        elif type(a).__name__ == "list":
            return [self.__removespace(x) for x in a]
        elif type(a).__name__ == "Row":
            return [self.__removespace(x) for x in a]
        elif type(a) is set:
            return {self.__removespace(x) for x in a}
        else:
            return a


class MsSQL(GenericSQL):
    """
    [summary]
        - A Class Built For Microsoft SQL Server Connection

    Extends:
        GenericSQL
    """
    def __init__(self, server=None, database=None,
                 username=None, password=None):
        '''
        [summary]
            - Initialize The Database Class With Values

        Keyword Arguments:
            server {string} -- Server To Connect To     (default: {None})
            database {string} -- Database To Connect To (default: {None})
            username {string} -- Username To Connect As (default: {None})
            password {string} -- Password For Username  (default: {None})
        '''
        super().__init__(server, database, username, password)

    def print_init_message(self):
        '''
        [summary]
            - Function To Print Information On How To
                Initialize When Error Occurs.

        '''
        print('-'*85)
        print("#"*15, "Initialization Error For Microsoft SQL Server", "#"*15)
        print(
                (
                    "Missing 4 Required Arguments: "
                    "'server', "
                    "'database', "
                    "'userId', "
                    "'password'"
                )
             )
        print("Server \t\t: The Server Name/Location You Want To Connect To")
        print("Database \t: The Database You Want To Connect To")
        print("Username \t: The User ID That You Want To Connect As")
        print("Password \t: The Password For User ID Provided")
        print("-"*20, "Example For Connection", "-"*20)
        print(r"myMSQL = MsSQL('1.2.3.4\Server', 'Database', 'user', 'pwd')")
        print('-'*85)

    def __generate_connection_string(self):
        '''
        [summary]
            - Function To Generate Out The Connection String
        '''
        if self.__is_complete_info():
            self.connection_string = re.sub(
                                                r'[\s+]',
                                                '',
                                                self.__get_connection_format()
                                           ).format(
                                                    self.__get_driver_type(),
                                                    self.server,
                                                    self.database,
                                                    self.username,
                                                    self.password
                                                   )
        else:
            raise ValueError('Please Check Your Connection Details.')

    def __get_connection_format(self):
        '''
        [summary]
            - A Function To Get The Database Connection String Format

        Returns:
            str -- The Database Connection String Format
        '''
        conn_str_format = '''
                                DRIVER      = {{{}}};
                                SERVER      = {};
                                DATABASE    = {};
                                UID         = {};
                                PWD         = {};
                            '''
        return conn_str_format

    def __get_driver_type(self):
        '''
        [summary]
            - A Function To Return The Driver Type For The Connection String
        '''
        return "SQL Server"

    def __is_complete_info(self):
        '''
        [summary]
            - Check If Data Inserted During Initialize Is Correct

        Returns:
            bool -- Status On Data Inialize Correctly
        '''
        if (str(self.server).strip() is None or
           str(self.database).strip() is None or
           str(self.username).strip() is None or
           str(self.password).strip() is None):
            return False
        else:
            return True

    def __cursor_connection_check(self):
        '''
        [summary]
            - A Function To Check For Database Cursor And Connection
        '''
        # To Clear Cursor Object
        if self.cursor_object is not None:
            self.cursor_object.close()
            self.cursor_object = None

        # Check If Cursor Object Is Valid
        if self.cursor_object is None:
            # Check If Connection Object Is None
            if self.connection_object is None:
                # If None, Do A Connection
                self.connect()

            self.set_cursor_obj()

    def connect(self):
        '''
        [summary]
            - A Function To Do Connection
        '''
        try:
            # Check If Connection String Is Empty
            if self.connection_string == '':
                # If Empty, Generate Connection String
                # - Different Child Class Different String
                self.__generate_connection_string()

            self.connection_object = pypyodbc.connect(self.connection_string)
        except Exception as e:
            raise e

    def execute(self, sql, value=None):
        '''
        [summary]
            - Function To Execute Query Such As Insert/Update/Delete/Create

        Arguments:
            sql {str} -- Query String That Need To Be Execute
            value {tuple} -- Values Wrap In Tuple

        Returns:
            list -- list of result
        '''
        if value is not None:
            if type(value) is not tuple:
                raise ValueError(
                    (
                        "Given 'value' value is not type tuple or None."
                    )
                )

        try:
            self.__cursor_connection_check()
            resultList = []
            self.cursor_object.execute(sql, value)
            rowCount = self.cursor_object.rowcount

            if rowCount == -1:
                columns = self.cursor_object.description
                records = self.cursor_object.fetchall()
                tempDict = {"column": columns, "value": records}
                resultList.append(tempDict)
            else:
                resultList.append(rowCount)

            # advance to next result set
            while (self.cursor_object.nextset()):
                rowCount = self.cursor_object.rowcount
                if rowCount == -1:
                    columns = self.cursor_object.description
                    records = self.cursor_object.fetchall()
                    tempDict = {"column": columns, "value": records}
                    resultList.append(tempDict)
                else:
                    resultList.append(rowCount)

            return resultList
        except Exception as e:
            raise e

    def query(self, sql, value=None, returnAsDataFrame=True):
        '''
        [summary]
            - Function To Execute Query Only For Select Statement
            - Return Value As A Pandas Data Frame

        Arguments:
            sql {str} -- Query String That Need To Be Execute

        Returns:
            list of dataframe -- Result Return From Query
        '''
        if value is not None:
            if type(value) is not tuple:
                raise ValueError(
                    (
                        "Given 'value' value is not type tuple or None."
                    )
                )

        # Check If Connection Object Is None
        if self.connection_object is None:
            # If None, Do A Connection
            self.connect()

        try:
            self.__cursor_connection_check()

            if returnAsDataFrame:
                result = pd.io.sql.read_sql(
                                                sql,
                                                con=self.connection_object,
                                                params=value
                                           )
            else:
                self.cursor_object.execute(sql, value)
                columns = [desc[0] for desc in self.cursor_object.description]
                records = self.cursor_object.fetchall()
                result = {"column": columns, "value": records}

            return result
        except Exception as e:
            raise e


class Oracle(GenericSQL):
    """
    [summary]
        - A Class Built For Oracle Connection

    [description]
        There Is Two Type Of Connection String For Oracle Database Connection
        1)  Is By TNS
            - Driver={Oracle in OraClient11g_home1};
                     DBQ=myTnsServiceName;
                     Uid=myUsername;
                     Pwd=myPassword;
        2)  Is By Hostname:Port/SID
            - Driver={Oracle in OraClient11g_home1};
                     DBQ=myserver.mydomain.com:1521/mySid;
                     Uid=myUsername;
                     Pwd=myPassword;

    Extends:
        GenericSQL
    """
    def __init__(self, server=None, database=None,
                 username=None, password=None):
        '''
        [summary]
            - Initialize The Database Class With Values

        Keyword Arguments:
            server {string} -- Server To Connect To     (default: {None})
            database {string} -- Database To Connect To (default: {None})
            username {string} -- Username To Connect As (default: {None})
            password {string} -- Password For Username  (default: {None})
        '''
        self.TYPE_CURSOR = cx_Oracle.CURSOR
        super().__init__(server, database, username, password)

    def print_init_message(self):
        '''
        [summary]
            - Function To Print Information On How To
                Initialize When Error Occurs.

        '''
        print('-'*76)
        print("#"*17, "Initialization Error For Oracle Database", "#"*17)
        print(
                (
                    "Missing 4 Required Arguments: "
                    "'server', "
                    "'database', "
                    "'userId', "
                    "'password'"
                )
             )
        print(
                (
                    "Server \t\t: The Server Location Example - "
                    "Host IP Address:Port/SID"
                )
             )
        print("Database \t: The Database World In Your TNS File")
        print("Username \t: The User ID That You Want To Connect As")
        print("Password \t: The Password For User ID Provided")
        print(
                "*"*8,
                "Do Note You Can Provide Either Server Or Database Argument",
                "*"*8
             )
        print("-"*15, "Example For Connection Using Server", "-"*16)
        print("myOrcl = Oracle('1.2.3.4:1234/sid', '', 'user', 'pwd')")
        print("-"*15, "Example For Connection Using Database", "-"*15)
        print("myOrcl = Oracle('', 'databaseWorld', 'user', 'pwd')")
        print('-'*76)

    def __generate_connection_string(self):
        '''
        [summary]
            - Function To Generate Out The Connection String
        '''
        if self.__is_complete_info():
            tempDBQ = ''

            if str(self.server).strip() != '':
                try:
                    ip, portsid = str(self.server).split(':')
                    port, sid = portsid.split('/')
                except ValueError:
                    raise ValueError('Please Check Your Connection Details.')
                except Exception as e:
                    raise e
                else:
                    tempDBQ = cx_Oracle.makedsn(ip, port, sid)

                    if tempDBQ == '':
                        raise ValueError(
                            (
                                'Please Check Your Connection Details.'
                            )
                        )
            else:
                tempDBQ = self.database

            self.connection_string = tempDBQ
        else:
            raise ValueError('Please Check Your Connection Details.')

    def __get_connection_format(self):
        '''
        [summary]
            - A Function To Get The Database Connection String Format
            - cx_Oracle Does Not Need Format

        Returns:
            str -- The Database Connection String Format
        '''
        pass

    def __get_driver_type(self):
        '''
        [summary]
            - A Function To Return The Driver Type For The Connection String
        '''
        pass

    def __is_complete_info(self):
        '''
        [summary]
            - Check If Data Inserted During Initialize Is Correct

        Returns:
            bool -- Status On Data Inialize Correctly
        '''
        if (
            (
                str(self.server).strip() is None or
                str(self.database).strip() is None
            ) or
            str(self.username).strip() is None or
            str(self.password).strip() is None
           ):
            return False
        else:
            return True

    def __cursor_connection_check(self):
        '''
        [summary]
            - A Function To Check For Database Cursor And Connection
        '''
        # To Clear Cursor Object
        if self.cursor_object is not None:
            self.cursor_object.close()
            self.cursor_object = None

        # Check If Cursor Object Is Valid
        if self.cursor_object is None:
            # Check If Connection Object Is None
            if self.connection_object is None:
                # If None, Do A Connection
                self.connect()

            self.set_cursor_obj()

    def connect(self):
        '''
        [summary]
            - A Function To Do Connection
        '''
        try:
            # Check If Connection String Is Empty
            if self.connection_string == '':
                # If Empty, Generate Connection String
                # - Different Child Class Different String
                self.__generate_connection_string()

            self.connection_object = cx_Oracle.connect(
                                        self.username,
                                        self.password,
                                        self.connection_string
                                        )
        except Exception as e:
            raise e

    def execute(self, sql, value=None):
        '''
        [summary]
            - Function To Execute Query Such As Insert/Update/Delete/Create

        Arguments:
            sql {str} -- Query String That Need To Be Execute
            value {tuple} -- Values Wrap In Tuple

        Returns:
            list -- list of result
        '''
        if value is not None:
            if type(value) is not tuple:
                raise ValueError(
                    (
                        "Given 'value' value is not type tuple or None."
                    )
                )

        try:
            self.__cursor_connection_check()

            # To Check If There Begin And End In Statement
            findResult = re.findall(r"BEGIN(?:(?!BEGIN).|\t|\s|\n)*END", sql)
            if len(findResult) > 0:
                raise ValueError(
                    (
                        "Please Do Not Open Another "
                        "Transaction In The SQL Query"
                    )
                )

            if value is None:
                self.cursor_object.execute(sql)
            else:
                self.cursor_object.execute(sql, value)

            rowCount = self.cursor_object.rowcount
            if rowCount == 0:
                if self.cursor_object.description is None:
                    result = rowCount
                else:
                    curDesc = self.cursor_object.description
                    columns = [desc[0] for desc in curDesc]
                    records = self.cursor_object.fetchall()
                    result = {"column": columns, "value": records}
            else:
                result = rowCount

            return result
        except Exception as e:
            raise e

    def query(self, sql, value=None, returnAsDataFrame=True):
        '''
        [summary]
            - Function To Execute Query Only For Select Statement
            - Return Value As A Pandas Data Frame

        Arguments:
            sql {str} -- Query String That Need To Be Execute

        Returns:
            list of dataframe -- Result Return From Query
        '''
        if value is not None:
            if type(value) is not tuple:
                raise ValueError(
                    (
                        "Given 'value' value is not type tuple or None."
                    )
                )

        try:
            self.__cursor_connection_check()
            result = None

            if returnAsDataFrame:
                result = pd.io.sql.read_sql(
                                            sql,
                                            con=self.connection_object,
                                            params=value
                                           )
            else:
                if value is None:
                    self.cursor_object.execute(sql)
                else:
                    self.cursor_object.execute(sql, value)

                columns = [desc[0] for desc in self.cursor_object.description]
                records = self.cursor_object.fetchall()
                result = {"column": columns, "value": records}

            return result
        except Exception as e:
            raise e

    def call_func(self, function_name, output_type, parameter_value):
        '''
        [summary]
            - A Function To Call The Oracle Function

        Arguments:
            function_name {str} -- The Function Name To Call
            output_type {type} -- The Function Return Value Type
            parameter_value {tuple} -- Function Parameter Value Wrap In A Tuple

        Returns:
            dependent on the output_type -- The result value return
                                            by the function
        '''
        # Check if output_type is a type format
        if not type(output_type) is type:
            raise ValueError("'output_type' given is not a type")

        # Check if parameter_value given is in tuple format
        if not type(parameter_value) is tuple:
            raise ValueError("'parameter_value' given is not a tuple")

        try:
            self.__cursor_connection_check()
            result = None

            # Call The cx_Oracle callproc method
            returnValue = self.cursor_object.callfunc(
                                                        function_name,
                                                        output_type,
                                                        tuple(parameter_value)
                                                     )

            if type(returnValue) == self.TYPE_CURSOR:
                cursorOutput = returnValue.getvalue()
                columns = [desc[0] for desc in cursorOutput.description]
                records = cursorOutput.fetchall()
                result = {"column": columns, "value": records}
            else:
                result = returnValue

            return result
        except Exception as e:
            raise e

    def call_proc(self, procedure_name, parameter_value):
        '''
        [summary]
            - Function That Will Call The Oracle Procedure

        Arguments:
            procedure_name {str} -- The Procedure Name To Call
            parameter_value {tuple} -- Procedure Parameter Value In The
                                        Form Of (InputValue, OutputType)
                                        e.g ('ValueOne', 2, str, Oracle.Cursor)

        Returns:
            output parameter value -- list of different value of the
                                        out parameter of the procedure.
        '''
        # Check if parameter_value given is in tuple format
        if not type(parameter_value) is tuple:
            raise ValueError("'parameter_value' given is not tuple")

        try:
            self.__cursor_connection_check()

            # Prepare The Parameter Value For Oracle Output
            paramValue = []
            paramType = []
            for parameter in parameter_value:
                if type(parameter) == type:
                    paramValue.append(self.cursor_object.var(parameter))
                    paramType.append("OUT")
                else:
                    paramValue.append(parameter)
                    paramType.append("IN")

            # Call The cx_Oracle callproc method
            self.cursor_object.callproc(procedure_name, tuple(paramValue))

            # Retrieve All Output Parameter Value
            outputList = []
            for paramVal, paramType in zip(paramValue, paramType):
                if paramType == "OUT":
                    if type(paramVal) == self.TYPE_CURSOR:
                        cursorOutput = paramVal.getvalue()
                        curDesc = cursorOutput.description
                        columns = [desc[0] for desc in curDesc]
                        records = cursorOutput.fetchall()
                        tempDict = {"column": columns, "value": records}
                        outputList.append(tempDict)
                    else:
                        outputList.append(paramVal.getvalue())

            return outputList
        except Exception as e:
            raise e

    def enable_dbms_output(self):
        '''
        [summary]
            - A Function To Enable DBMS_OUTPUT
        '''
        try:
            self.__cursor_connection_check()
            procName = 'DBMS_OUTPUT.ENABLE'
            param = (None, )
            outputVal = self.call_proc(procName, param)
            return outputVal
        except Exception as e:
            raise e

    def disable_dbms_output(self):
        '''
        [summary]
            - A Function To Disable DBMS_OUTPUT
        '''
        try:
            self.__cursor_connection_check()
            procName = 'DBMS_OUTPUT.DISABLE'
            param = (None, )
            outputVal = self.call_proc(procName, param)
            return outputVal
        except Exception as e:
            raise e

    def get_dbms_output(self):
        '''
        [summary]
            - A Function To Get DBMS_OUTPUT Line
        '''
        try:
            self.__cursor_connection_check()

            procName = 'DBMS_OUTPUT.GET_LINE'
            param = (str, int)  # lineValue, Status Value

            resultList = []
            while True:
                output = self.call_proc(procName, param)
                if output[1] != 0:
                    break
                else:
                    resultList.append(
                        {
                            'status_value': output[1],
                            'line_message': output[0]
                        }
                    )

            return resultList
        except Exception as e:
            raise e


class Postgres(GenericSQL):
    """
    [summary]
        - A Class Built For PostgreSQL Database Connection

    Extends:
        GenericSQL
    """
    def __init__(self, server=None, database=None,
                 username=None, password=None):
        '''
        [summary]
            - Initialize The Database Class With Values

        Keyword Arguments:
            server {string} -- Server To Connect To     (default: {None})
            database {string} -- Database To Connect To (default: {None})
            username {string} -- Username To Connect As (default: {None})
            password {string} -- Password For Username  (default: {None})
        '''
        super().__init__(server, database, username, password)

    def print_init_message(self):
        '''
        [summary]
            - Function To Print Information On How To
                Initialize When Error Occurs.

        '''
        print('-'*77)
        print("#"*15, "Initialization Error For PostgreSQL Database", "#"*15)
        print(
                (
                    "Missing 4 Required Arguments: "
                    "'server', "
                    "'database', "
                    "'userId', "
                    "'password'"
                )
             )
        print("Server \t\t: Is The Host/Port You Want To Connect To")
        print("Database \t: Is The Database You Want To Connect To")
        print("Username \t: Is The User ID That You Want To Connect As")
        print("Password \t: Is The Password For User ID Provided")
        print("-"*20, "Example For Connection", "-"*20)
        print(
                (
                    "myPostgres = Postgres("
                    "'1.2.3.4/port', "
                    "'Database', "
                    "'user', "
                    "'pwd')"
                )
             )
        print('-'*77)

    def __generate_connection_string(self):
        '''
        [summary]
            - Function To Generate Out The Connection String
        '''
        if self.__is_complete_info():
            svrIP, svrPort = self.server.split("/")
            self.connection_string = self.__get_connection_format().format(
                                        svrIP,
                                        svrPort,
                                        self.database,
                                        self.username,
                                        self.password
                                     )
        else:
            raise ValueError('Please Check Your Connection Details.')

    def __get_connection_format(self):
        '''
        [summary]
            - A Function To Get The Database Connection String Format

        Returns:
            str -- The Database Connection String Format
        '''
        conn_str_format = '''
                            host        = '{}'
                            port        = '{}'
                            dbname      = '{}'
                            user        = '{}'
                            password    = '{}'
                          '''
        return conn_str_format

    def __get_driver_type(self):
        '''
        [summary]
            - A Function To Return The Driver Type For The Connection String
        '''
        return ""

    def __is_complete_info(self):
        '''
        [summary]
            - Check If Data Inserted During Initialize Is Correct

        Returns:
            bool -- Status On Data Inialize Correctly
        '''
        if (str(self.server).strip() is None or
           str(self.database).strip() is None or
           str(self.username).strip() is None or
           str(self.password).strip() is None):
            return False
        else:
            return True

    def __cursor_connection_check(self):
        '''
        [summary]
            - A Function To Check For Database Cursor And Connection
        '''
        # To Clear Cursor Object
        if self.cursor_object is not None:
            self.cursor_object.close()
            self.cursor_object = None

        # Check If Cursor Object Is Valid
        if self.cursor_object is None:
            # Check If Connection Object Is None
            if self.connection_object is None:
                # If None, Do A Connection
                self.connect()

            self.set_cursor_obj()

    def connect(self):
        '''
        [summary]
            - A Function To Create Connection To Database Using Psycopg2

        '''
        try:
            # Check If Connection String Is Empty
            if self.connection_string == '':
                # If Empty, Generate Connection String
                # - Different Child Class Different String
                self.__generate_connection_string()

            self.connection_object = psycopg2.connect(self.connection_string)
        except Exception as e:
            raise e

    def execute(self, sql, value=None):
        '''
        [summary]
            - Function To Execute Query Such As Insert/Update/Delete/Create

        Arguments:
            sql {str} -- Query String That Need To Be Execute
            value {tuple} -- Values Wrap In Tuple

        Returns:
            list -- list of result
        '''
        if value is not None:
            if type(value) is not tuple:
                raise ValueError(
                    (
                        "Given 'value' value is not type tuple or None."
                    )
                )

        try:
            self.__cursor_connection_check()
            self.cursor_object.execute(sql, value)

            statusResult = self.cursor_object.statusmessage.split(" ")

            if statusResult[0] == "SELECT":
                resultList = []
                resultSet = self.cursor_object.fetchall()
                resultDesc = self.cursor_object.description

                if len(resultDesc) > 1:
                    for result, description in zip(resultSet[0], resultDesc):
                        # Check If It Refcursor Type (1790)
                        if description[1] == 1790:
                            # 1 Col Value That Is A Refcursor Type
                            self.cursor_object.execute(
                                f'FETCH ALL IN "{result}"'
                            )
                            cursDesc = self.cursor_object.description
                            columns = [desc[0] for desc in cursDesc]
                            records = self.cursor_object.fetchall()
                            cursorDict = {
                                            "column": columns,
                                            "value": records
                                         }
                            tempDict = {
                                        "column": description,
                                        "value": cursorDict
                                       }
                            resultList.append(tempDict)
                        else:
                            # 1 Col Value That Is Not A Refcursor Type
                            tempDict = {"column": description, "value": result}
                            resultList.append(tempDict)
                else:
                    # Check If It Refcursor Type (1790)
                    if resultDesc[0][1] == 1790:
                        # 1 Row Value That Is A Refcursor Type
                        colList = []

                        for result in resultSet:
                            self.cursor_object.execute(
                                f'FETCH ALL IN "{ result[0] }"'
                            )
                            cursDesc = self.cursor_object.description
                            columns = [desc[0] for desc in cursDesc]
                            records = self.cursor_object.fetchall()
                            tempDict = {"column": columns, "value": records}
                            colList.append(tempDict)

                        resultList.append(colList)
                    else:
                        # 1 Row Value That Is Not Refcursor Type
                        tempDict = {
                                    "column": resultDesc[0],
                                    "value": resultSet[0]
                                   }
                        resultList.append(tempDict)
            elif statusResult[0] == "INSERT":
                returningInfo = None
                if "RETURNING" in sql.upper():
                    returningInfo = self.cursor_object.fetchall()

                resultList = {
                                "row_affected": statusResult[2],
                                "oid": statusResult[1],
                                "returning_info": returningInfo
                             }
            else:
                resultList = {"row_affected": statusResult[1]}

            return resultList
        except Exception as e:
            raise e

    def query(self, sql, value=None, returnAsDataFrame=True):
        '''
        [summary]
            - Function To Execute Query Only For Select Statement
            - Return Value As A Pandas Data Frame

        Arguments:
            sql {str} -- Query String That Need To Be Execute

        Returns:
            list of dataframe -- Result Return From Query
        '''
        if value is not None:
            if type(value) is not tuple:
                raise ValueError(
                    (
                        "Given 'value' value is not type tuple or None."
                    )
                )

        try:
            self.__cursor_connection_check()

            resultList = []
            if returnAsDataFrame:
                df = pd.io.sql.read_sql(
                                        sql,
                                        con=self.connection_object,
                                        params=value
                                       )
                resultList.append(df)
            else:
                self.cursor_object.execute(sql, value)
                self.cursor_object.execute(sql, value)
                columns = [desc[0] for desc in self.cursor_object.description]
                records = self.cursor_object.fetchall()
                tempDict = {"column": columns, "value": records}
                resultList.append(tempDict)

            return resultList
        except Exception as e:
            raise e

    def retrieve_cursor_info(self, value):
        '''
        [summary]
            - A Function To Retrieve All Data Base On
                Cursor Name From The Given Value

        Arguments:
            value {str} -- The String Value That Contains
                            Cursor Name Information

        Returns:
            list of dictionary -- {
                                    "column": CursorName,
                                    "value": {
                                                "column": (Cursor Column Info),
                                                "value": Cursor Records
                                             }
                                  }
        '''
        # Check If Value Is An Empty String
        if len(value) == 0 or value is None:
            return None

        # Regex Find All Cursor Name Using Pattern "<Cursor Name Here>"
        cursorNameList = re.findall(r'\"<.*?>\"', ''.join(value))
        if len(cursorNameList) == 0:
            return None

        # Initialize Information
        resultList = []
        self.__cursor_connection_check()

        # Loop Through Each Cursor Name
        for cursorName in cursorNameList:
            # Replace '"' In Cursor Name To ''
            cursorName = cursorName.replace('"', '')
            # Fetch Cursor Data And Store In Dictionary
            self.cursor_object.execute(f'FETCH ALL IN "{ cursorName }"')
            columns = [desc[0] for desc in self.cursor_object.description]
            records = self.cursor_object.fetchall()
            cursorDict = {"column": columns, "value": records}
            # Store Cursor Value Dictionary In
            # Another Dictionary With Column Information
            tempDict = {"column": cursorName, "value": cursorDict}
            # Append Result In List
            resultList.append(tempDict)

        # Return Result List
        return resultList
