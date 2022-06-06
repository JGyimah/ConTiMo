import os
from motivml.semantics import Semantics

class Constraints(Semantics):
    def __init__(self) -> None:
        Semantics.__init__(self)
        self.restructuredBindings = {}
        self.restructuredModelFeatures = {}

    def checkAllConstraints(self, modelObj, bindingObj, runningProject):
        self.restructureModelBinding(bindingObj)
        #traverse model and check constraints
        if "sub" in modelObj:
            self.subTraverse(modelObj["sub"])
        #read bound features
        #check if all features in model have associated binding
        if len(self.restructuredModelFeatures) == len(self.restructuredBindings):
            allBoundFeatures = self.readBoundFeatures(runningProject)
            #get all bindings and loop to validate constraints
            for feature in self.restructuredModelFeatures:
                #check includes
                self.includes(feature, self.restructuredModelFeatures[feature], allBoundFeatures)
                    
                #check excludes
                self.excludes(feature, self.restructuredModelFeatures[feature], allBoundFeatures)

                #check parent child constraints
                self.parentChild(feature, self.restructuredModelFeatures[feature], self.restructuredBindings)

                #binding prop constraints
                self.bindingPropertyConstraints(self.restructuredModelFeatures[feature], self.restructuredBindings[feature])

            #print error count
            if self.excludesErrorCount == 0 and self.includesErrorCount == 0 and self.parentChildErrorCount == 0 and self.bindingPropErrorCount == 0:
                print("[SUCCESS] Constraint Checker Found Zero Constraint Errors")
            else:
                print("[ALERT] Constraint Checker Found ("+ str(self.excludesErrorCount+self.includesErrorCount+self.parentChildErrorCount+self.bindingPropErrorCount)+") Constraint Error(s)")
        

        elif len(self.restructuredModelFeatures) > len(self.restructuredBindings):
            print("[SYNTAX ERROR]: Some features DO NOT have associated configurations")
        elif len(self.restructuredModelFeatures) < len(self.restructuredBindings):
            print("[SYNTAX ERROR]: Some configurations DO NOT have associated features")


    def restructureModelBinding(self, modelBindingObject):
        #restructure bindings and save in self.restructuredBindings
        for binding in modelBindingObject["properties"]:
            self.restructuredBindings[binding["id"]] = binding["props"]

    def subTraverse(self, subFeatureObject):
        for feature in subFeatureObject:
            if "sub" in feature:
                self.restructuredModelFeatures[feature["id"]] = feature["constraints"]
                newsubList = []
               
                for eachSub in feature["sub"]:
                    newsubList.append(eachSub["id"])
               
                self.restructuredModelFeatures[feature["id"]]["sub"] = newsubList
                self.subTraverse(feature["sub"])
            else:
                self.restructuredModelFeatures[feature["id"]] = feature["constraints"]
                self.restructuredModelFeatures[feature["id"]]["sub"] = []

    def readBoundFeatures(self, projectName):
        projPath = os.path.dirname(os.path.abspath("../" + projectName +"/bindings.motivml"))
        bindingStore = os.path.join(projPath, "bindings.motivml")
        with open(bindingStore) as bindingfile:
            boundFeatures = bindingfile.readlines()
        strippedBoundFeatures = [unstripped.strip() for unstripped in boundFeatures]
        return strippedBoundFeatures
        