import decimal

import StorageService.proto.storage_service_pb2 as pb2
import StorageService.proto.storage_service_pb2_grpc as pb2_grpc
import StorageService.Logger as Log
from StorageService.Storage.Connection import StorageConnection as Connection
from StorageService.Storage.ActionsUsers import AddUser, RemoveUser
from StorageService.Storage.ActionsExpense import AddExpenses, RemoveExpenses, GetExpenses, UpdateExpenses
from StorageService.Storage.ActionMoneys import AddMoney, RemoveMoney, GetMoney, UpdateMoney

logger = "Storage.Service"


class StorageService(pb2_grpc.StorageServicer):

    def __init__(self, parameters_path):
        self.logger = 'Service.Storage'
        Log.info(self.logger, "Service was initialized")
        connection = Connection()
        connection.connect(parameters_path)

    def addUser(self, request, context):
        Log.info(self.logger, f"Input user: {request.name}, {request.chat_id}")
        action = AddUser()
        action.createRequest(request.chat_id, request.name)
        result = action.execute()

        if not result.isSuccess():
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

        action = AddMoney()
        action.createRequest(request.chat_id)
        result = action.execute()

        if result.isSuccess():
            Log.success(self.logger, f"User was added: name={request.name}, chat_id={request.chat_id}")
            return pb2.Status(is_success=True)
        else:
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

    def removeUser(self, request, context):
        Log.info(self.logger, f"Input user: {request.name}, {request.chat_id}")

        action = RemoveUser()
        action.createRequest(request.chat_id, request.name)
        result = action.execute()

        if not result.isSuccess():
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

        action = RemoveMoney()
        action.createRequest(request.chat_id)
        result = action.execute()

        if result.isSuccess():
            Log.success(self.logger, f"User was added: name={request.name}, chat_id={request.chat_id}")
            return pb2.Status(is_success=True)
        else:
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

    def addExpense(self, request, context):
        Log.info(self.logger, f"Input user: name={request.user.name}; chat_id={request.user.chat_id}")
        Log.info(self.logger, f"Input expense: name_expense={request.expense.name}; value={request.expense.value}")

        action = AddExpenses()
        action.createRequest(request.user.chat_id, request.expense.name, request.expense.value)
        result = action.execute()

        if result.isSuccess():
            Log.success(self.logger, f"Expense was added: name_expense={request.expense.name}; "
                                     f"value={request.expense.value}")
            return pb2.Status(is_success=True)
        else:
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

    def removeExpense(self, request, context):
        Log.info(self.logger, f"Input user: name={request.user.name}; chat_id={request.user.chat_id}")
        Log.info(self.logger, f"Input expense: name_expense={request.expense.name}; value={request.expense.value}")

        action = RemoveExpenses()
        action.createRequest(request.user.chat_id, request.expense.name)
        result = action.execute()

        if result.isSuccess():
            Log.success(self.logger, f"Expense was removed: name_expense={request.expense.name}; "
                                     f"value={request.expense.value}")
            return pb2.Status(is_success=True)
        else:
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

    def getExpenses(self, request, context):
        Log.info(self.logger, f"Input user: {request.name}, {request.chat_id}")

        action = GetExpenses()
        action.createRequest(request.chat_id, only_value=True, only_name=True)
        result = action.execute()

        if result.isSuccess():
            response = pb2.Expenses(status=pb2.Status(is_success=True))
            for value in result.result_value:
                response.data.append(pb2.Expense(name=value[0], value=value[1]))
            Log.success(self.logger, f"Data was resived for user: name:{request.name}, chat_id:{request.chat_id}")
            return response
        else:
            Log.error(self.logger, result.message)
            return pb2.Expenses(status=pb2.Status(is_success=False))

    def setExpense(self, request, context):
        Log.info(self.logger, f"Input user: name={request.user.name}; chat_id={request.user.chat_id}")
        Log.info(self.logger, f"Input expense: name_expense={request.expense.name}; value={request.expense.value}")

        action = GetExpenses()
        action.createRequest(request.user.chat_id, request.expense.name, only_value=True)
        result = action.execute()

        additional_value = decimal.Decimal(str(round(request.expense.value, 2)))

        value = additional_value
        if result.isSuccess() and len(result.result_value) != 0:
            value += result.result_value[0][0]
        else:
            Log.error(self.logger, "Expense was not created")
            return pb2.Status(is_success=False)

        action = UpdateExpenses()
        action.createRequest(request.user.chat_id, request.expense.name, value)
        result = action.execute()

        if result.isSuccess():
            Log.success(self.logger, f"Expense was updated: name_expense={request.expense.name}; "
                                     f"value={value}")
            return pb2.Status(is_success=True)
        else:
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

    def addMoney(self, request, context):
        Log.info(self.logger, f"Add money: name={request.user.name}; chat_id={request.user.chat_id}")
        Log.info(self.logger, f"Input value: money={request.value}")

        additional_value = decimal.Decimal(str(round(request.value, 2)))

        action = GetMoney()
        action.createRequest(request.user.chat_id)
        result = action.execute()

        if not result.isSuccess():
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

        if not len(result.result_value) != 0:
            Log.error(self.logger, f"Money for user {request.user.chat_id} not exist")
            return pb2.Status(is_success=False)

        value = result.result_value[0][1] + additional_value

        action = UpdateMoney()
        action.createRequest(request.user.chat_id, value)
        result = action.execute()

        if result.isSuccess():
            Log.success(self.logger, f"Money was update for user {request.user.chat_id} "
                                     f"value={value}")
            return pb2.Status(is_success=True)
        else:
            Log.error(self.logger, result.message)
            return pb2.Status(is_success=False)

    def getMoney(self, request, context):
        Log.info(self.logger, f"Input user: name={request.name}; chat_id={request.chat_id}")

        action = GetMoney()
        action.createRequest(request.chat_id)
        result = action.execute()

        if not result.isSuccess():
            Log.error(self.logger, result.message)
            return pb2.GetMoneyResponse(status=pb2.Status(is_success=False))

        if len(result.result_value) != 0:
            response = pb2.GetMoneyResponse(status=pb2.Status(is_success=True), value=result.result_value[0][1])
            Log.success(self.logger, f"Money was received for user {request.chat_id} "
                                     f"value={result.result_value[0][1]}")
            return response
        else:
            Log.error(self.logger, "Money was not created")
            return pb2.GetMoneyResponse(status=pb2.Status(is_success=False))