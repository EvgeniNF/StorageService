from threading import Lock


class ScopedMutex:

    def __init__(self, lock: Lock):
        self.__lock = lock
        self.__lock.acquire()

    def __del__(self):
        self.__lock.release()
