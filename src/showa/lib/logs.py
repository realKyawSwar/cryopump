import inspect
import logging
import errno
import os
import tempfile
import sys
from logging.handlers import TimedRotatingFileHandler
from logging import FileHandler

ERROR_INVALID_NAME = 123

LEVEL_NOT_SET = 0
LEVEL_DEBUG = 1
LEVEL_INFO = 2
LEVEL_WARNING = 3
LEVEL_ERROR = 4
LEVEL_CRITICAL = 5

TYPE_TIME = "TIME"
TYPE_FILE = "FILE"

allow_print = False
defaultMessageFormat = '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'


def how_to_use():
    '''
    [description]
        - Prints Out All The Information On How To Use The Logs Module
    '''
    print("-"*110)
    print("#"*40, " How To Use The logs Module ", "#"*40)
    print("~"*39, " Step 1 - Initializing Logger ", "~"*39)
    print("Initialize The Logger By Calling logs.initLogger()")
    print("It take 3 Optional Parameters: ")
    print(
        (
            "a) name, To Define The Logger Name. \n\t- If No Parameter Input, "
            "Will Use Main Script File Name Or DefaultLogger "
            "When Running Using Console"
        )
    )
    print(
        (
            "b) path, To Define The Save Path Of The Logs File. "
            "\n\t- Default Value Is At project_folder\\src\\showa\\logs"
        )
    )
    print(
        (
            "c) logLevel, To Define The Logging Level Of Application. "
            "\n\t- Default Value Is At Debug. \n\t- For More Info: "
            "https://docs.python.org/2/library/logging.html#logging-levels"
        )
    )
    print("~"*42, " Step 2 - Start Logging ", "~"*42)
    print(
        (
            "Start Logging By Calling logs.logCritical(msg), "
            "\n\t\t\t     .logDebug(msg), "
            "\n\t\t\t     .logInfo(msg), "
            "\n\t\t\t     .logWarning(msg) or "
            "\n\t\t\t     .logError(msg)"
        )
    )
    print("Where msg Is A Message String That You Want To Log In The File")
    print(
        (
            "For logCritical, logDebug, logInfo, logWarning Takes In "
            "2 Additional Parameters Where As logError Takes 3:"
        )
    )
    print(
        (
            "a) includeStackPos, Which Will Include The Caller Function Name "
            "In The Logging Logger Name. \n\t- Default Value Is False"
        )
    )
    print(
        (
            "b) skipStackCaller, Stack Traceback Level To "
            "Skip From Logs Module. "
            "\n\t- Default Value Is 2 "
            "\n\t- Example: "
            "\n\t\t- Flow To Log Module Is Main.FunctionOne -> logs.logInfo "
            "-> logs private function "
            "\n\t\t- Skip 2 Will Return Main.FunctionOne"
        )
    )
    print("!!!!! Only For logError !!!!!")
    print(
        (
            "c) includeErrorLine, Which Will Include Traceback "
            "Error Line Number In Log Message. \n\t- Default Value Is False"
        )
    )
    print("~"*39, " Step 3 - Closing Down Logger ", "~"*39)
    print(
        "An Important Step Before Ending Your Program Is To Close The Logger"
    )
    print("To Do So Is By Calling logs.closeLogger()")
    print("")
    print("~"*110)
    print("For More Information Regarding Function,")
    print("You Can Type help(function_name_here) For Function Description.")
    print("-"*110)


def check_print(*message):
    global allow_print
    if allow_print:
        print(*message)


def initLogger(name='-PARAM-AUTO-', path='..\\src\\showa\\logs',
               logLevel=LEVEL_INFO, fileName="LoggingInfo",
               messageFormat=defaultMessageFormat, logType=TYPE_TIME,
               logWhen="H", logInterval=1, logSuffix="%Y%m%d-%H.log",
               existRollover=False, allowPrint=False):
    '''
    [summary]
        - To Initialize Logger Based On Few Parameter
    [description]
        - Initialize Global Name To Store Logger Name
        - Setting Logger Formatter
        - And Time Rotating File Handler or File Handler
    Keyword Arguments:
        name {str} -- Logger Name (default: {'-PARAM-AUTO-'})
        path {str} -- Path To Store The Logging Files
                        (default: {'..\\src\\showa\\logs'})
        logLevel {int} -- Logging Level For Logging To Handle
                            (default: {LEVEL_INFO})
                        -- LEVEL_NOT_SET    - NOTSET   - 0
                        -- LEVEL_DEBUG      - DEBUG    - 1
                        -- LEVEL_INFO       - INFO     - 2
                        -- LEVEL_WARNING    - WARNING  - 3
                        -- LEVEL_ERROR      - ERROR    - 4
                        -- LEVEL_CRITICAL   - CRITICAL - 5
        fileName {str} -- The log file name (default: {"LoggingInfo"})
        messageFormat {str} -- The format to write the log data
                             (default: {defaultMessageFormat})
                        --'%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'
        logType {str} -- The Log Handler Type (default: {TYPE_TIME})
                        -- TYPE_TIME - TIME - Time Rotating File Handler
                        -- TYPE_FILE - FILE - File Handler
        logWhen {str} -- Time Interval Type (default: {"H"})
        logInterval {number} -- Time Interval Value (default: {1})
        logSuffix {str} -- Rollover File Suffix (default: {"%Y%m%d-%H.log"})
        existRollover {bool} -- To Do Rollover If File Exist (default: {False})
        allowPrint {bool} -- Allow print on command line (default: {False})
    '''
    global loggerName, allow_print
    allow_print = allowPrint

    if name == '-PARAM-AUTO-':
        loggerName = __getCallerFileName()
    else:
        loggerName = name

    logger = logging.getLogger(loggerName)
    formatter = logging.Formatter(messageFormat)

    if logLevel == LEVEL_NOT_SET:
        loggingLevel = logging.NOTSET
    elif logLevel == LEVEL_DEBUG:
        loggingLevel = logging.DEBUG
    elif logLevel == LEVEL_INFO:
        loggingLevel = logging.INFO
    elif logLevel == LEVEL_WARNING:
        loggingLevel = logging.WARNING
    elif logLevel == LEVEL_ERROR:
        loggingLevel = logging.ERROR
    elif logLevel == LEVEL_CRITICAL:
        loggingLevel = logging.CRITICAL

    mainFolder = os.path.dirname(sys.argv[0])
    if os.path.isabs(path):
        if not __is_path_exists_or_creatable(path):
            check_print("Log Path Given Is Not Valid - {}".format(str(path)))
            path = os.path.join(mainFolder, '..\\src\\showa\\logs')
    else:
        if not __is_path_exists_or_creatable(
                os.path.join(mainFolder, path)):
            check_print(
                        "Log Path Given Is Not Valid - {}".format(
                            str(os.path.abspath(path))
                        )
                       )
            path = os.path.join(mainFolder, '..\\src\\showa\\logs')
        else:
            path = os.path.join(mainFolder, path)

    if not os.path.exists(path):
        os.mkdir(path)

    logPath = os.path.join(os.path.abspath(path), fileName)
    check_print("Logging Will Be Written To This File: \n{}".format(logPath))

    logType = logType.upper()
    if logType == TYPE_TIME:
        handler = TimedRotatingFileHandler(
                                        logPath,
                                        logWhen,
                                        logInterval,
                                        delay=True
                                      )
        handler.suffix = logSuffix  # or anything else that strftime will allow

        if existRollover:
            if os.path.isfile(logPath):
                handler.doRollover()
    else:
        handler = FileHandler(logPath)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(loggingLevel)


def closeLogger():
    '''
    [summary]
        - To Close All Logging Handler
    '''
    logging.shutdown()


def logCritical(msg, includeStackPos=False, skipStackCaller=2):
    '''
    [summary]
        - To simplify user code to log critical information

    [description]
        - Check For Logger Exist
        - To Check If User Require Stack Position
        - Log Information Using Logging.

    Arguments:
        msg {string} -- [Message To Log]

    Keyword Arguments:
        includeStackPos {bool} -- [To Include Stack Position In Message Log]
                                    (default: {False})
        skipStackCaller {number} -- [Number Of Stack Position To Skip]
                                        (default: {2})
    '''
    chkStatus, chkRemark = __checkIfLoggerExist()
    if not chkStatus:
        check_print(chkRemark, "\n", msg)
    else:
        logger = logging.getLogger(
                                    __getLoggerName(
                                                    includeStackPos,
                                                    skipStackCaller + 1
                                                   )
                                  )
        logger.critical(msg)


def logDebug(msg, includeStackPos=False, skipStackCaller=2):
    '''
    [summary]
        - To simplify user code to log debug information

    [description]
        - Check For Logger Exist
        - To Check If User Require Stack Position
        - Log Information Using Logging.

    Arguments:
        msg {string} -- [Message To Log]

    Keyword Arguments:
        includeStackPos {bool} -- [To Include Stack Position In Message Log]
                                    (default: {False})
        skipStackCaller {number} -- [Number Of Stack Position To Skip]
                                    (default: {2})
    '''
    chkStatus, chkRemark = __checkIfLoggerExist()
    if not chkStatus:
        check_print(chkRemark, "\n", msg)
    else:
        logger = logging.getLogger(
                                    __getLoggerName(
                                                    includeStackPos,
                                                    skipStackCaller + 1
                                                   )
                                  )
        logger.debug(msg)


def logError(msg, includeStackPos=False, skipStackCaller=2,
             includeErrorLine=False, moduleNameIncludeClass=False):
    '''
    [summary]
        - To simplify user code to log error information

    [description]
        - Check For Logger Exist
        - To Check If User Require Stack Position
        - Log Information Using Logging.

    Arguments:
        msg {string} -- [Message To Log]

    Keyword Arguments:
        includeStackPos {bool} -- [To Include Stack Position In Message Log]
                                    (default: {False})
        skipStackCaller {number} -- [Number Of Stack Position To Skip]
                                        (default: {2})
    '''
    chkStatus, chkRemark = __checkIfLoggerExist()
    if not chkStatus:
        check_print(chkRemark, "\n", msg)
    else:
        errorLine = ''

        if includeErrorLine:
            modName, fnName, lineNo = __getErrorLocationInfo(
                                            moduleNameIncludeClass
                                      )
            errorLine = "Error @ [{}][{}][{}] ".format(modName, fnName, lineNo)

        msg = '{}{}'.format(errorLine, msg)
        logger = logging.getLogger(
                                    __getLoggerName(
                                                    includeStackPos,
                                                    skipStackCaller + 1
                                                   )
                                  )
        logger.error(msg)


def logInfo(msg, includeStackPos=False, skipStackCaller=2):
    '''
    [summary]
        - To simplify user code to log info information

    [description]
        - Check For Logger Exist
        - To Check If User Require Stack Position
        - Log Information Using Logging.

    Arguments:
        msg {string} -- [Message To Log]

    Keyword Arguments:
        includeStackPos {bool} -- [To Include Stack Position In Message Log]
                                    (default: {False})
        skipStackCaller {number} -- [Number Of Stack Position To Skip]
                                        (default: {2})
    '''
    chkStatus, chkRemark = __checkIfLoggerExist()
    if not chkStatus:
        check_print(chkRemark, "\n", msg)
    else:
        logger = logging.getLogger(
                                    __getLoggerName(
                                                    includeStackPos,
                                                    skipStackCaller + 1
                                                   )
                                  )
        logger.info(msg)


def logWarning(msg, includeStackPos=False, skipStackCaller=2):
    '''
    [summary]
        - To simplify user code to log warning information

    [description]
        - Check For Logger Exist
        - To Check If User Require Stack Position
        - Log Information Using Logging.

    Arguments:
        msg {string} -- [Message To Log]

    Keyword Arguments:
        includeStackPos {bool} -- [To Include Stack Position In Message Log]
                                    (default: {False})
        skipStackCaller {number} -- [Number Of Stack Position To Skip]
                                        (default: {2})
    '''
    chkStatus, chkRemark = __checkIfLoggerExist()
    if not chkStatus:
        check_print(chkRemark, "\n", msg)
    else:
        logger = logging.getLogger(
                                    __getLoggerName(
                                                    includeStackPos,
                                                    skipStackCaller + 1
                                                   )
                                  )
        logger.warning(msg)


def __checkIfLoggerExist(moduleNameIncludeClass=False):
    '''
    [summary]
        - To Check If Logging's Logger Has Already Been Created
    [description]
        - Check If Logging's Logger Already Been Created,
        - If Not Created,
            Will Create A New Logging Logger Base On MainFile Name

    Returns:
        bool -- [Status If Logger Existed],
        string -- [Message Of Status/Error Message Faced]

    '''
    if 'loggerName' in globals():
        return True, 'Logger Exist'
    else:
        try:
            loggerName = __getCallerFileName()
            initLogger(loggerName)

            return True, 'New Global Logger Has Been Created'
        except Exception:
            modName, fnName, lineNo = __getErrorLocationInfo(
                                        moduleNameIncludeClass
                                      )
            return (
                False,
                "[{}][{}][{}] Unable To Check For Logger Name".format(
                    modName,
                    fnName,
                    lineNo
                )
            )


def __getCallerName(skip=2):
    '''
    [summary]
        - Get a name of a caller in the format module.class.method
    [description]
        - `skip` specifies how many levels of stack to
            skip while getting caller
            name. skip=1 means "who calls me",
                  skip=2 "who calls my caller" etc.
    Returns:
        [string] -- An empty string is returned
                        if skipped levels exceed stack height
    '''
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)

    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':
        name.append(codename)
    del parentframe
    return ".".join(name)


def __getCallerFileName():
    '''
    [summary]
        - To Get Main Script File Name Without Its Path And Extension

    Returns:
        [string] -- [Main Script File Name/Root When Meet Error]
    '''
    fileName = "root"

    try:
        firstStack = inspect.stack()[-1]
        parentFrame = firstStack[0]
        module = inspect.getmodule(parentFrame)
        fileName = module.__file__
        del parentFrame

        if '\\' in fileName:
            fileName = fileName.split("\\")[-1]

        if '.' in fileName:
            fileName = fileName.split(".")[0]
    except Exception as e:
        check_print(
            (
                "Unable To Get Main Script File Name As Logger Name, "
                "\nError Faced: '{}'"
            ).format(
                        str(e)
                    )
        )

    return fileName


def __getLoggerName(includeStackPos, skipStackCaller):
    '''
    [summary]
        - Retrieve Logger Name With/Without Stack Information Of
            Function That Calls The Logger
    Arguments:
        includeStackPos {[bool]} -- True To Include, False To Exclude
        skipStackCaller {[type]} -- Stack Call Position To Skip
                                    From Current Logger Module

    Returns:
        [String] -- [Logger Name With/Without Stack Information]
    '''
    if includeStackPos:
        tempLoggerName = loggerName + '.'
        tempLoggerName += __getCallerName(skipStackCaller).replace(".", ">>")
    else:
        tempLoggerName = loggerName

    return tempLoggerName


def __getErrorLocationInfo(moduleNameIncludeClass=False):
    '''
    [summary]
        - Function Returning Module Name, Function Name And Line Number

    Returns:
        [type] -- [description]
        moduleName [string] -- Module Name Of Stack,
        functionName [string] -- Function Name Of Stack,
        lineNo [string] -- Line No That Traceback Occurs
    '''
    error_frame_info = None
    stackLen = len(inspect.stack())

    if len(inspect.trace()) > 0:
        error_frame_info = inspect.trace()[-1]
    elif stackLen >= 3:
        error_frame_info = inspect.stack()[2]
    else:
        error_frame_info = inspect.stack(stackLen - 1)

    parentFrame = error_frame_info.frame

    mod_name_list = []
    module = inspect.getmodule(parentFrame)
    if module:
        mod_name_list.append(module.__name__)

    if moduleNameIncludeClass:
        if 'self' in parentFrame.f_locals:
            modName = parentFrame.f_locals['self'].__class__.__name__
            mod_name_list.append(modName)

        codename = parentFrame.f_code.co_name
        if codename != '<module>':
            mod_name_list.append(codename)

    del parentFrame

    moduleName = ".".join(mod_name_list)
    functionName = error_frame_info.function
    lineNo = error_frame_info.lineno
    del error_frame_info

    return moduleName, functionName, lineNo


def __is_pathname_valid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
    #
    # Did we mention this should be shipped with Python already?


def __is_path_sibling_creatable(pathname: str) -> bool:
    '''
        `True` if the current user has sufficient permissions
        to create **siblings**
        (i.e., arbitrary files in the parent directory) of the passed pathname;
        `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()

    try:
        # For safety, explicitly close and hence delete this temporary file
        # immediately after creating it in the passed path's parent directory.
        with tempfile.TemporaryFile(dir=dirname):
            pass
        return True
    # While the exact type of exception raised by the above function depends on
    # the current version of the Python interpreter,
    # all such types subclass the following exception superclass.
    except EnvironmentError:
        return False


def __is_path_exists_or_creatable(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname on the current OS _and_
    either currently exists or is hypothetically creatable in a cross-platform
    manner optimized for POSIX-unfriendly filesystems; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    '''
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return __is_pathname_valid(pathname) and (
            os.path.exists(pathname) or __is_path_sibling_creatable(pathname))
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues
    # and should not be caught here.
    except OSError:
        return False
