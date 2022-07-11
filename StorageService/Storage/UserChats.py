from mysql.connector import Error
from StorageService.Storage.StorageConnection import StorageConnection
import StorageService.Logger as Log


class BaseStrategy:

    def __init__(self, connection: StorageConnection):
        self.connection = connection

    def getUserId(self, chat_id: int) -> [int, None]:
        cursor = self.connection.getCursor()

        if cursor is None:
            return None

        cursor.execute(f"SELECT ID FROM UserChats WHERE ChatId={chat_id}")
        response = cursor.fetchall()

        if len(response) == 1:
            return response[0][0]
        return None

    def execute(self):
        ...


class AddNewUser(BaseStrategy):
    cursor = None
    values: dict = {}

    def __init__(self, connection: StorageConnection, values: dict):
        super().__init__(connection)
        self.values = values

    def execute(self) -> bool:
        self.cursor = self.connection.getCursor()

        if not self._createNewUserChat(self.values["chat_id"], self.values["user_name"]):
            return False

        user_id = self.getUserId(self.values["chat_id"])
        if user_id is None:
            Log.error("Add.New.User", f"Can't create user! User id {self.values['chat_id']} not found in table UserChats")
            return False

        if not self._createNewWastes(user_id):
            return False

        return True

    def _createNewUserChat(self, chat_id: int, name_user: str):
        try:
            request = f"INSERT INTO UserChats (ChatId, UserName) VALUES ({chat_id}, '{name_user}')"
            self.cursor.execute(request)
            return self.connection.commit()
        except Error as insertion_error:
            Log.error("Add.New.User", insertion_error.msg)
            return False

    def _createNewWastes(self, user_id):
        try:
            self.cursor.execute(f"INSERT INTO Wastes (UserId, Eat, HouseHold, Closes) VALUES ({user_id}, 0, 0, 0)")
            return self.connection.commit()
        except Error as insertion_error:
            Log.error("Add.New.Wastes", insertion_error.msg)
            return False


class ChatIsExist(BaseStrategy):

    def __init__(self, connection: StorageConnection, chat_id, user_name):
        super().__init__(connection)
        self.chat_id = chat_id
        self.user_name = user_name

    def execute(self):
        cursor = self.connection.getCursor()
        if cursor is None:
            return False

        cursor.execute(f"SELECT UserName FROM UserChats WHERE ChatId={self.chat_id}")
        response = cursor.fetchall()

        if len(response) != 1:
            return False

        return response[0][0] == self.user_name


class ChangeValue(BaseStrategy):

    def __init__(self, connection: StorageConnection, values:dict, user_chat_id):
        super().__init__(connection)
        self.values = values
        self.user_chat_id = user_chat_id

    def execute(self):
        value = []
        for key in self.values.keys():
            value.append(str(key) + " = " + str(self.values[key]))
        value = ', '.join(value)

        request = f"UPDATE Wastes INNER JOIN UserChats " \
                  f"ON Wastes.UserId = UserChats.ID " \
                  f"SET {value} " \
                  f"WHERE UserChats.ChatId = {self.user_chat_id} "

        cursor = self.connection.getCursor()
        if cursor is None:
            return False

        cursor.execute(request)
        return self.connection.commit()


class GetValue(BaseStrategy):

    def __init__(self, connection: StorageConnection, chat_id, values):
        super().__init__(connection)
        self.chat_id = chat_id
        self.values = values

    def execute(self):
        cursor = self.connection.getCursor()
        if cursor is None:
            return None

        data = ", ".join(self.values)
        cursor.execute(f"SELECT {data} "
                       f"FROM UserChats JOIN Wastes "
                       f"WHERE ChatId={self.chat_id} AND Wastes.UserId=UserChats.ID")
        request = cursor.fetchall()
        if len(request) == 0:
            return None

        size_data = len(request[0])
        if size_data != len(self.values):
            return None

        result = {}
        for i in range(size_data):
            result[self.values[i]] = request[0][i]

        return result


class RemoveUser(BaseStrategy):

    def __init__(self, connection: StorageConnection, chat_id):
        super().__init__(connection)
        self.chat_id = chat_id

    def execute(self):
        cursor = self.connection.getCursor()
        if cursor is None:
            return False

        cursor.execute(f"DELETE FROM UserChats WHERE ChatId={self.chat_id}")
        return self.connection.commit()
