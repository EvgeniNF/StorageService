from StorageService.Storage.Requsets.Request import RequestWere


class RequestSelect(RequestWere):
    what = "*"

    def add_what(self, value):
        if self.what == "*":
            self.what = value
        else:
            self.what += f", {value}"

    def getRequest(self):
        if self.where is None:
            return f"SELECT {self.what} FROM {self.name_table}"
        else:
            return f"SELECT {self.what} FROM {self.name_table} WHERE {self.where}"
