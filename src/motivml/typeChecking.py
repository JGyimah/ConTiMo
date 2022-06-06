class TypeChecking():
    def __init__(self) -> None:
        self._bindingTimesAllowed = ["early", "late", "any"]
        self._bindingModesAllowed = ["static", "dynamic", "any"]
        self._groupsAllowed = ["or", "xor", "none"]
        self._optional = [True, False]
        self._bindingTimeValues = ["early", "late"]
        self._bindingModeValues = ["static", "dynamic"]

    def isAlphaStringType(self, propertyValue):
        return propertyValue.isalpha()

    def isAlphanumStringType(self, propertyValue):
        return propertyValue.isalnum()

    def isValidConstraintBlock(self, propertyValue, featureID):
        collectedKeys = []
        collectedVals = []
        if isinstance(propertyValue, dict):
            #For each constraint key value pair
            for key, value in propertyValue.items():
                if key == "featuresIncluded":
                    collectedKeys.append("featuresIncluded")
                    if not isinstance(value, list):
                        collectedVals.append(featureID+":featuresIncluded:wrongVal")
                        print("[SYNTAX ERROR]: Feature("+featureID+") has invalid includes property value")

                if key == "featuresExcluded":
                    collectedKeys.append("featuresExcluded")
                    if not isinstance(value, list):
                        collectedVals.append(featureID+":featuresExcluded:wrongVal")
                        print("[SYNTAX ERROR]: Feature("+featureID+") has invalid excludes property value")

                if key == "bindingTimeAllowed":
                    collectedKeys.append("bindingTimeAllowed")
                    if value.lower() not in self._bindingTimesAllowed:
                        collectedVals.append(featureID+":bindingTimeAllowed:invalidVal")
                        print("[SYNTAX ERROR]: Feature("+featureID+") has invalid binding time constraint value")

                if key == "bindingModeAllowed":
                    collectedKeys.append("bindingModeAllowed")
                    if value.lower() not in self._bindingModesAllowed:
                        collectedVals.append(featureID+":bindingTimeAllowed:invalidVal")
                        print("[SYNTAX ERROR]: Feature("+featureID+") has invalid binding mode constraint value")

            return [collectedKeys, collectedVals]
        else:
            collectedVals.append(featureID+":constraint:invalidVal")
            print("[SYNTAX ERROR]: Feature("+featureID+") has invalid constraints property value")

    def isValidGroupType(self, propertyValue):
        if propertyValue.lower() not in self._groupsAllowed:
            return "unknownGroup"

    def isValidOptionalType(self, propertyValue):
        if propertyValue not in self._optional:
            return "unknownMandatoryStatus"

    def isValidPropsBlock(self, props, featureID):
        collectedKeys = []
        collectedVals = []
        if isinstance(props, dict):
            for key, value in props.items():
                if key == "mode":
                    collectedKeys.append("mode")
                    if value.lower() not in self._bindingModeValues:
                        collectedVals.append(featureID+":mode")
                        print("[SYNTAX ERROR]: Feature Binding("+featureID+") has an invalid binding mode value")
                        

                if key == "time":
                    collectedKeys.append("time")
                    if value.lower() not in self._bindingTimeValues:
                        collectedVals.append(featureID+":time")
                        print("[SYNTAX ERROR]: Feature Binding("+featureID+") has an invalid binding time value")
            
            return [collectedKeys, collectedVals]
        else:
            collectedVals.append(featureID+":props:invalidVal")
            print("[SYNTAX ERROR]: Feature Binding("+featureID+") has invalid PROPS property value")