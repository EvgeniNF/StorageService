
class Request:

    def __init__(self, name_table: [str, list]):
        if type(name_table) is str:
            self.name_table = name_table
        else:
            self.name_table = ", ".join(name_table)

    def getRequest(self) -> str:
        ...


class RequestWere(Request):
    where = ""

    def startScope(self):
        self.where += "("

    def endScope(self):
        self.where += ")"

    def addLogicOperator(self, operator):
        self.where += f" {operator} "

    def addCondition(self, lvalue, operator, rvalue, use_type_rvalue=True):
        if use_type_rvalue and type(rvalue) is str:
            self.where += f"{lvalue} {operator} '{rvalue}'"
        else:
            self.where += f"{lvalue} {operator} {rvalue}"
