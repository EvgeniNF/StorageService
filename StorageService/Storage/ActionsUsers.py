from StorageService.Storage.Actions import GetAction, SetAction, Action
from StorageService.Storage.Requsets import Insert
from StorageService.Storage.Requsets import Delete
from StorageService.Storage.Requsets import Select


class Users(Action):

    def __init__(self):
        super().__init__()
        self.table_name = "Users"


class AddUser(Users, SetAction):

    def createRequest(self, chat_id, user_name):
        request_insert = Insert.Insert(self.table_name)
        request_insert.addColumn("chat_id", chat_id)
        request_insert.addColumn("name", user_name)
        self.request = request_insert.getRequest()


class RemoveUser(Users, SetAction):

    def createRequest(self, chat_id, user_name):
        request_delete = Delete.Delete(self.table_name)
        request_delete.addCondition("chat_id", "=", chat_id)
        request_delete.addLogicOperator("AND")
        request_delete.addCondition("name", "=", user_name)
        self.request = request_delete.getRequest()


class GetUser(Users, GetAction):

    def createRequest(self, chat_id, user_name=None, only_name=False, only_id=False):
        request_select = Select.RequestSelect(self.table_name)
        request_select.addCondition("chat_id", "=", chat_id)

        if user_name is not None:
            request_select.addLogicOperator("AND")
            request_select.addCondition("name", "=", user_name)

        if only_id:
            request_select.add_what("chat_id")

        if only_name:
            request_select.add_what("name")

        self.request = request_select.getRequest()
