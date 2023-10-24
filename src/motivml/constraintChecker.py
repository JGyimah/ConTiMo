from motivml.constraints import Constraints

class ConstraintChecker(Constraints):
    def __init__(self) -> None:
        Constraints.__init__(self)

    def validateModelConstraints(self, modelObject, bindingObject, runningProject):
        self.checkAllConstraints(modelObject, bindingObject, runningProject)