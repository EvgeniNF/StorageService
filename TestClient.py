import grpc
import StorageService.proto.storage_service_pb2_grpc as pb2_grpc
import StorageService.proto.storage_service_pb2 as pb2


class UnaryClient(object):
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        self.stub = pb2_grpc.StorageStub(self.channel)

    def get_url(self):
        message = pb2.UserExpense(user=pb2.User(chat_id=323), expense=pb2.Expense(value=0.0))
        return self.stub.setExpense(message)


if __name__ == '__main__':
    client = UnaryClient()
    result = client.get_url()
