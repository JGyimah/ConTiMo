class Semantics():
    def __init__(self) -> None:
        self.includesErrorCount = 0
        self.excludesErrorCount = 0
        self.parentChildErrorCount = 0
        self.bindingPropErrorCount = 0


    def includes(self, feature, contraintObject, boundFeatureList):
        if feature in boundFeatureList:
            if len(contraintObject["featuresIncluded"]) > 0:
                featureNotInBoundList = list(filter(lambda x: x not in boundFeatureList, contraintObject["featuresIncluded"]))
                for notIncluded in featureNotInBoundList:
                        self.includesErrorCount += 1
                        print("[INCLUDES CONSTRAINT ERROR]: Feature("+feature+") requires "+ notIncluded) 


    def excludes(self, feature, contraintObject, boundFeatureList):
        if feature in boundFeatureList:
            if len(contraintObject["featuresExcluded"]) > 0:
                featureInBoundList = list(filter(lambda x: x in boundFeatureList, contraintObject["featuresExcluded"]))
                for notExcluded in featureInBoundList:
                        self.excludesErrorCount += 1
                        print("[EXCLUDES CONSTRAINT ERROR]: Feature("+feature+") cannot be selected along with "+ notExcluded) 


    def parentChild(self, feature, contraintObject, restructuredBindings):
        if len(contraintObject["sub"]) > 0:
            if restructuredBindings[feature]["mode"].lower() == "dynamic":
                for sub in contraintObject["sub"]:
                    if restructuredBindings[sub]["mode"].lower() == "static":
                        self.parentChildErrorCount += 1
                        print("[CONSTRAINT ERROR]: Dynamic Parent Feature("+feature+") cannot have a Static Child ("+sub+")")


    def bindingPropertyConstraints(self, featureConstraints, featureBindingProperties):
        anyTime = ["early", "late"]
        anyMode = ["static", "dynamic"]

        if featureConstraints["bindingTimeAllowed"].lower() != featureBindingProperties["time"].lower():
            if featureConstraints["bindingTimeAllowed"].lower() == "any" and ( featureBindingProperties["time"].lower() not in anyTime):
                self.bindingPropErrorCount += 1
                print("[CONSTRAINT ERROR]: An 'Any' binding time must alternate between 'Early' and 'Late'")

        if featureConstraints["bindingModeAllowed"].lower() != featureBindingProperties["mode"].lower():
            if featureConstraints["bindingModeAllowed"].lower() == "any" and ( featureBindingProperties["mode"].lower() not in anyMode):
                self.bindingPropErrorCount += 1
                print("[CONSTRAINT ERROR]: An 'Any' binding mode must alternate between 'Static' and 'Dynamic'")