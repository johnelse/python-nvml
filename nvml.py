import ctypes

NVML = ctypes.CDLL("libnvidia-ml.so")

def init():
    NVML.nvmlInit()

def shutdown():
    NVML.nvmlShutdown()

def error_string(code):
    error_string = NVML.nvmlErrorString
    error_string.restype = ctypes.c_char_p
    return error_string(code)

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg

class Device():
    def __init__(self, handle):
        self.handle = handle

    @staticmethod
    def get_count():
        c_count = ctypes.c_uint(0)
        code = NVML.nvmlDeviceGetCount(ctypes.byref(c_count))
        if 0 == code:
            return c_count
        else:
            raise Error(error_string(code))

    @staticmethod
    def get_handle_by_index(index):
        c_index = ctypes.c_uint(index)
        handle = ctypes.c_ulonglong(0)
        code = NVML.nvmlDeviceGetHandleByIndex(c_index, ctypes.byref(handle))
        if 0 == code:
            return Device(handle)
        else:
            raise Error(error_string(code))

    def get_fan_speed(self):
        fan_speed = ctypes.c_uint(0)
        code = NVML.nvmlDeviceGetFanSpeed(self.handle, ctypes.byref(fan_speed))
        if 0 == code:
            return fan_speed
        else:
            raise Error(error_string(code))

