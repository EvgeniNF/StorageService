from StorageService.Storage.Requsets.Request import Request


class Insert(Request):
    columns = ""
    values = ""

    def insertDeliver(self):
        if self.columns != "":
            self.columns += ", "

        if self.values != "":
            self.values += ", "

    def addColumn(self, column, value):
        self.insertDeliver()

        self.columns += column

        if type(value) is str:
            self.values += f"'{value}'"
        else:
            self.values += f"{value}"

    def getRequest(self) -> str:
        return f"INSERT INTO {self.name_table} ({self.columns}) VALUES ({self.values})"

