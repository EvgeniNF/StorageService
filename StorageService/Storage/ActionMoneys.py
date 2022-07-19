import decimal

from StorageService.Storage.Actions import Action, SetAction, GetAction
from StorageService.Storage.Requsets import Insert
from StorageService.Storage.Requsets import Delete
from StorageService.Storage.Requsets import Select
from StorageService.Storage.Requsets import Update


class Money(Action):

    def __init__(self):
        super().__init__()
        self.table_name = "Money"


class AddMoney(Money, SetAction):

    def createRequest(self, chat_id):
        insert_request = Insert.Insert(self.table_name)
        insert_request.addColumn("chat_id", chat_id)
        insert_request.addColumn("balance", decimal.Decimal("0.0"))
        self.request = insert_request.getRequest()


class UpdateMoney(Money, SetAction):

    def createRequest(self, chat_id, balance):
        update_request = Update.RequestUpdate(self.table_name)
        update_request.addSet("balance", balance)
        update_request.addCondition("chat_id", "=", chat_id)
        self.request = update_request.getRequest()


class RemoveMoney(Money, SetAction):

    def createRequest(self, chat_id):
        remove_request = Delete.Delete(self.table_name)
        remove_request.addCondition("chat_id", "=", chat_id)
        self.request = remove_request.getRequest()


class GetMoney(Money, GetAction):

    def createRequest(self, chat_id):
        select_request = Select.RequestSelect(self.table_name)
        select_request.addCondition("chat_id", "=", chat_id)
        self.request = select_request.getRequest()
