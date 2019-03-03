
from vu4py.UTime import UTime
import enum
from time import sleep


class ULogger:
    class Settings:
        RECORD_LOG = False

    class Data:
        log = list()

    class Levels(enum.Enum):
        DEBUG = 0
        TRACE = 1
        INFO = 2
        WARNING = 3
        ERROR = 4
        FATAL = 5

    @staticmethod
    def log(message, level=Levels.INFO):
        time = UTime.timestamp()
        log_message = "[{}][{}]: {}".format(time, level.name, message)
        print(log_message)
        if ULogger.Settings.RECORD_LOG:
            Data.log.append(log_message)
