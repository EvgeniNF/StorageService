import StorageService.proto.storage_service_pb2 as pb2
import StorageService.proto.storage_service_pb2_grpc as pb2_grpc
import StorageService.Logger as Log
from StorageService.Storage.UserChats import ChatIsExist, GetValue, AddNewUser, BaseStrategy
from StorageService.Storage.StorageConnection import StorageConnection as Connection
from StorageService.Storage.StorageConnection import ConnectionSettings as Settings


logger = "StorageService"


class StorageService(pb2_grpc.StorageServicer):

    def __init__(self, *args, **kwargs):
        Log.info("StorageService", "Service was initialized")
        self.connection = Connection("Storage/storage.parameters.json")
        self.logger = 'Service.Storage'

    def getValues(self, request, context):
        Log.info(self.logger, f"Receive new request on getValues")
        Log.info(self.logger, f"Request User: [chat_id: {request.chat_id}, name: {request.name}]")

        response = pb2.GetDataResponse()

        if not self.connection.isConnected():
            if not self.connection.reconnect():
                response.status.is_success = False
                response.status.message = "Failed connection to database"
                Log.error(self.logger, response.status.message)
                return response

        user_exist = ChatIsExist(self.connection, request.chat_id, request.name)

        if not user_exist.execute():
            add_user = AddNewUser(self.connection, {"ChatId":request.chat_id, "UserName":request.name})
            if not add_user.execute():
                response.status.is_success = False
                response.status.message = "Failed create a new user"
                Log.error(self.logger, response.status.message)
                return response

        get_data = GetValue(self.connection, chat_id=request.chat_id, values=["Eat", "HouseHold", "Closes"])
        data = get_data.execute()


        return response

    def setValues(self, request, context):
        Log.info("StorageService.setValues", f"Input user: {request.user.user_name}, {request.user.chat_id}")
        return pb2.Status()

    def removeUser(self, request, context):
        Log.info("StorageService.removeUser", f"Input user: {request.user_name}, {request.chat_id}")
        return pb2.Status()

    def addUser(self, request, context):
        Log.info("StorageService.addUser", f"Input user: {request.user_name}, {request.chat_id}")
        return pb2.Status()

    def userIsExist(self, request, context):
        Log.info("StorageService.userIsExist", f"Input user: {request.user_name}, {request.chat_id}")
        return pb2.IsExist()
