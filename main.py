import grpc
from concurrent import futures
from StorageService.proto import storage_service_pb2_grpc as pb2_grpc
from StorageService.Server import StorageService
from StorageService import Logger as Log


def main():
    grpc_server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_StorageServicer_to_server(StorageService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    grpc_server.start()
    Log.info("StorageService", "Server was started")
    try:
        grpc_server.wait_for_termination()
    except KeyboardInterrupt as interrupt:
        Log.info("StorageService", f"Was stopped{interrupt}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        Log.error("Service.Storage", f"Closed with error: {error}")
        quit(-1)

    quit(0)
