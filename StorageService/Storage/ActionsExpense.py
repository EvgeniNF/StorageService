from StorageService.Storage.Actions import GetAction, SetAction, Action
from StorageService.Storage.Requsets import Insert
from StorageService.Storage.Requsets import Delete
from StorageService.Storage.Requsets import Select
from StorageService.Storage.Requsets import Update


class Expenses(Action):

    def __init__(self):
        super().__init__()
        self.table_name = "Expenses"

    @staticmethod
    def formatLogicalCondition(request, chat_id, expense):
        request.addCondition("chat_id", "=", chat_id)
        request.addLogicOperator("AND")
        request.addCondition("expense", "=", expense)


class AddExpenses(Expenses, SetAction):

    def createRequest(self, chat_id, expense, value):
        request_insert = Insert.Insert(self.table_name)
        request_insert.addColumn("chat_id", chat_id)
        request_insert.addColumn("expense", expense)
        request_insert.addColumn("value", value)
        self.request = request_insert.getRequest()


class UpdateExpenses(Expenses, SetAction):

    def createRequest(self, chat_id, expense, value):
        request_update = Update.RequestUpdate(self.table_name)
        request_update.addSet("value", value)
        Expenses.formatLogicalCondition(request_update, chat_id, expense)
        self.request = request_update.getRequest()


class RemoveExpenses(Expenses, SetAction):

    def createRequest(self, chat_id, expense, value=None):
        request_delete = Delete.Delete(self.table_name)
        Expenses.formatLogicalCondition(request_delete, chat_id, expense)
        self.request = request_delete.getRequest()


class GetExpenses(Expenses, GetAction):

    def createRequest(self, chat_id, expense=None, only_name=False, only_value=False):
        request_select = Select.RequestSelect(self.table_name)
        if expense is not None:
            Expenses.formatLogicalCondition(request_select, chat_id, expense)
        else:
            request_select.addCondition("chat_id", "=", chat_id)

        if only_name:
            request_select.add_what("expense")

        if only_value:
            request_select.add_what("value")

        self.request = request_select.getRequest()
