from threading import Lock
from StorageService.Logger import error


class SingleTone(type):
    __instance = {}
    __mutex = Lock()

    def __call__(cls, *args, **kwargs):
        cls.__mutex.acquire()

        if cls not in cls.__instance:
            try:
                cls.__instance[cls] = super(SingleTone, cls).__call__(*args, **kwargs)
            except BaseException as instance_error:
                error("SingleTone", f"Instance object has instance error: {instance_error}")
                cls.__mutex.release()
                return None

        cls.__mutex.release()
        return cls.__instance[cls]
