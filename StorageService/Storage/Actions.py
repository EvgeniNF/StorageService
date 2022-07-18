from StorageService.Storage.Connection import StorageConnection
from mysql.connector import Error
import StorageService.Logger as Log


class ActionResult:

    def __init__(self, success: bool=True, message: str="Ok", result_value=None):
        self.success = success
        self.message = message
        self.result_value = result_value

    def isSuccess(self):
        return self.success


class Action:

    def __init__(self):
        self.connection = StorageConnection()
        self.request = ""

    def __checkConnection(self) -> ActionResult:
        if not self.connection.isConnected():
            if not self.connection.reconnect():
                ActionResult(
                    success=False,
                    message="Can't connect to database"
                )

        return ActionResult()

    def execute(self):
        ...


class SetAction(Action):

    def execute(self):
        cursor = self.connection.getCursor()

        try:
            Log.info("Action", f"Request to data base: {self.request}")
            cursor.execute(self.request)
            commit_result = self.connection.commit()
            if commit_result:
                return ActionResult()
            else:
                return ActionResult(
                    success=False,
                    message="Commit was not success"
                )
        except Error as execute_error:
            return ActionResult(
                success=False,
                message=execute_error.msg
            )


class GetAction(Action):

    def execute(self):
        cursor = self.connection.getCursor()

        try:
            Log.info("Action", f"Request to data base: {self.request}")
            cursor.execute(self.request)
            result = cursor.fetchall()
            return ActionResult(
                result_value=result)
        except Error as execute_error:
            return ActionResult(
                success=False,
                message=execute_error.msg)
