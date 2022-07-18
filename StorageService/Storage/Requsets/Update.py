from StorageService.Storage.Requsets.Request import RequestWere


class RequestUpdate(RequestWere):
    set = ""

    def __insertDeliver(self):
        if self.set != "":
            self.set += ', '

    def addSet(self, column, value):
        self.__insertDeliver()

        if type(value) is str:
            self.set += f"{column} = '{value}'"
        else:
            self.set += f"{column} = {value}"

    def getRequest(self):
        if self.where == "":
            return f"UPDATE {self.name_table} SET {self.set}"
        else:
            return f"UPDATE {self.name_table} SET {self.set} WHERE {self.where}"
