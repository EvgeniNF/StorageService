from StorageService.Storage.Requsets.Request import RequestWere


class Delete(RequestWere):

    def getRequest(self) -> str:
        return f"DELETE FROM {self.name_table} WHERE {self.where}"

