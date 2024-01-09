from enum import Enum
from feature import Feature

class BindingTimes(Enum):
    Early = "Early"
    Late = "Late"

class BindingModes(Enum):
    Static = "Static"
    Dynamic = "Dynamic"

class Configuration():
    def __init__(self, createdFeature: Feature) -> None:
        self.id:str = createdFeature.getId()
        self.time:BindingTimes = BindingTimes.Early
        self.time:BindingModes = BindingModes.Static

    def setConfigId(self, cid):
        self.id = cid

    def setBTime(self, btime:BindingTimes):
        self.time = btime

    def setBMode(self, bmode:BindingModes):
        self.mode = bmode

    def printConfig(self):
        pass