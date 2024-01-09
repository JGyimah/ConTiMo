from enum import Enum

class BindingTimeAllowed(Enum):
    Early = "Early"
    Late = "Late"
    Any = "Any"

class BindingModeAllowed(Enum):
    Static = "Static"
    Dynamic = "Dynamic"
    Any = "Any"

class Feature():
    def __init__(self) -> None:
        self.id:str = ""
        self.name:str = ""
        self.featuresIncluded:list[str] = []
        self.featuresExcluded:list[str] = []
        self.bindingTimeAllowed: BindingTimeAllowed = BindingTimeAllowed.Early
        self.bindingModeAllowed: BindingModeAllowed = BindingModeAllowed.Static
        self.group:str = ""
        self.isMandatory:bool = False

    def getId(self):
        return self.id
    
    def setId(self, id:str):
        self.id = id

    def setName(self, name:str):
        self.name = name

    def setFeatureIncluded(self, fid:str):
        self.featuresIncluded.append(fid)

    def setFeatureExcluded(self, fid:str):
        self.featuresExcluded.append(fid)

    def setGroup(self, group:str):
        self.group = group

    def setIsMandatory(self, mandtoryStatus:bool):
        self.isMandatory = mandtoryStatus

    def setBindingTimeAllowed(self, anAllowedBTime:BindingTimeAllowed):
        self.bindingTimeAllowed = anAllowedBTime

    def setBindingModeAllowed(self, anAllowedBMode:BindingModeAllowed):
        self.bindingModeAllowed = anAllowedBMode

    def printFeature(self):
        pass