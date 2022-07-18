from mysql.connector import connect, Error
from mysql.connector import CMySQLConnection
from StorageService.SingleTone import SingleTone
from StorageService import Logger as Log
from StorageService.Exceptions import BaseError
from StorageService.Mutex import ScopedMutex
from threading import Lock
import json


class ConnectionSettings:
    user_name = None
    password = None
    host = None
    database = None

    def readParametersFormJson(self, path_to_json) -> bool:
        try:
            with open(path_to_json) as document:
                data = json.load(document)[0]["connection_settings"]
                self.user_name = data["user_name"]
                self.password = data["password"]
                self.host = data["host"]
                self.database = data["database"]
            return True
        except Exception as error:
            Log.error("Storage.ReadConnectionSettings", f"Read file with connection settings error: {error}")
            return False


class StorageConnection(metaclass=SingleTone):
    __lock = Lock()

    def __init__(self) -> None:
        self.__connection = None

    def connect(self, path_to_connection_settings):
        settings = ConnectionSettings()

        if not settings.readParametersFormJson(path_to_connection_settings):
            raise BaseError("Error read connection settings")

        try:
            self.__connection = connect(
                host=settings.host,
                user=settings.user_name,
                password=settings.password,
                database=settings.database)
            Log.success("Storage.Connection", "Connection success")
        except Error as connection_error:
            Log.error("Storage.Connection", connection_error.msg)

    def isConnected(self) -> bool:
        _ = ScopedMutex(self.__lock)
        return self.__connection.is_connected()

    def getCursor(self) -> [CMySQLConnection, None]:
        _ = ScopedMutex(self.__lock)
        try:
            cursor = self.__connection.cursor()
            return cursor
        except Error as error:
            Log.error("Storage.Connection", error.msg)
            return None

    def reconnect(self) -> bool:
        _ = ScopedMutex(self.__lock)
        try:
            self.__connection.reconnect(5, 100)
            return True
        except Error as error:
            Log.error("Storage.Connection", error.msg)
            return False

    def commit(self) -> bool:
        _ = ScopedMutex(self.__lock)
        try:
            self.__connection.commit()
            return True
        except Error as commit_error:
            Log.error("Storage.Connection", commit_error.msg)
            return False
