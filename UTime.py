import time
import datetime


class UTime:
    @staticmethod
    def timeit(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            delta_time = end_time - start_time
            return delta_time, result
        return wrapper

    @staticmethod
    def timestamp():
        return datetime.datetime.now().strftime("%H:%M:%S")
