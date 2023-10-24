from motivml.traverse import Traverse

class SchemaChecker(Traverse):
    def __init__(self) -> None:
        Traverse.__init__(self)

    def validateModelSchema(self, modelObject, modelBindingObject, commandLineArgProjectName):
        self.parseModelSchema(modelObject, modelBindingObject, commandLineArgProjectName)