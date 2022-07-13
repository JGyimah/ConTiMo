import os
import json
from motivml.typeChecking import TypeChecking
from motivml.constraintChecker import ConstraintChecker

class Traverse(TypeChecking, ConstraintChecker):
    def __init__(self) -> None:
        TypeChecking.__init__(self)
        ConstraintChecker.__init__(self)
        self._modelErrorCount = []
        self._bindingErrorCount = []

    def getLexicon(self):
        modelPath = os.path.dirname(os.path.abspath('lexicons.json'))
        lexiconStore = os.path.join(modelPath, 'lexicons.json')
        dataFile = open(lexiconStore, 'r')
        lexiconState = json.loads(dataFile.read())
        dataFile.close()
        return lexiconState

    def getProperties(self, featureID, modelBinding):
        for prop in modelBinding['properties']:
            if prop['id'] == featureID:
                return prop

    def parseModelSchema(self, modelObject, modelBindingObject, runningProject):
        print("## Validating Model")
        if "sub" in modelObject:
            print("--------------Parsing Model----------------")
            self.parseModelSubSchema(modelObject, modelBindingObject)
            
            #if there are no modelling errors
            if len(self._modelErrorCount) == 0:
                print("[SUCCESS] Model Schema Has Zero Syntax Errors")
            else:
                print("[ALERT] Model Schema Has "+ str(len(self._modelErrorCount))+ " Syntax Error(s)")
                #see captured model syntax error
            print("--------------Model Parsing Ended-----------")
            print("                                            ")
            print("--------------Parsing Binding-----------------")
            self.parseBindingSchema(modelBindingObject)

            #if there are no binding errors
            if len(self._bindingErrorCount) == 0:
                print("[SUCCESS] Model Binding Schema Has Zero Syntax Errors")
            else:
                print("[ALERT] Model Binding Schema Has "+ str(len(self._bindingErrorCount))+ " Syntax Error(s)")
            print("-------------- Binding Parsing Ended-----------")
            
            #if there are no modelling and binding errors
            if(len(self._modelErrorCount) == 0 and len(self._bindingErrorCount) == 0):
                #Validate model constraints
                print("                                            ")
                print("--------------Constraint Checker Validation-----------------")
                #model constraints checking
                self.validateModelConstraints(modelObject, modelBindingObject, runningProject)

    def parseModelSubSchema(self, subArray, subArrayBinding):
        collectedTokens = []
        propGet = self.getProperties(subArray['id'], subArrayBinding)
        
        if propGet != None:
            collectedConstraintTokens = []
            if "id" in subArray:
                collectedTokens.append("id")
                if self.isAlphanumStringType(subArray['id']) == False:
                    self._modelErrorCount.append(['alphanum'])
                    print("[SYNTAX ERROR]: Feature("+subArray['id']+") has non-alphanumeric charactersIN ID")
                #Only if there is the specified ID in the feature that the feature will be fully evaluated. Else skip
                if "name" in subArray:
                    collectedTokens.append("name")
                    if self.isAlphaStringType(subArray['name']) == False:
                        self._modelErrorCount.append(['alpha'])
                        print("[SYNTAX ERROR]: Feature("+subArray['name']+") has non-alphanumeric characters in NAME")

                if "constraints" in subArray:
                    collectedTokens.append("constraints")   
                    collectedConstraintTokens = self.isValidConstraintBlock(subArray['constraints'], subArray['id'])

                if "group" in subArray:
                    collectedTokens.append("group")
                    groupTypeCheckResponse = self.isValidGroupType(subArray['group'])
                    if groupTypeCheckResponse == "unknownGroup":
                        self._modelErrorCount.append(subArray['id']+":group:unknownGroup")
                        print("[SYNTAX ERROR]: Feature("+subArray['id']+") has unknown GROUP type")

                if "isMandatory" in subArray:
                    collectedTokens.append("isMandatory")
                    groupTypeCheckResponse = self.isValidOptionalType(subArray['isMandatory'])
                    if groupTypeCheckResponse == "unknownMandatoryStatus":
                        self._modelErrorCount.append(subArray['id']+":isMandatory:unknownMandStatus")
                        print("[SYNTAX ERROR]: Feature("+subArray['id']+") has unknown isMandatory type")

                allcollectedTokens = collectedTokens + collectedConstraintTokens[0]
                languageTokens = self.getLexicon()
                tokenDiff = set(languageTokens['feature']) - set(allcollectedTokens)
                tokenDiff = list(tokenDiff)
                
                #if there is any token missing
                if len(tokenDiff) > 0:
                    missingFeatString = " ".join(tokenDiff)
                    self._modelErrorCount.append(subArray['id']+":mfeat:"+missingFeatString)
                    print("[SYNTAX ERROR]: Feature("+subArray['id']+") has missing attribute(s) "+missingFeatString)

                #If there are token value errors
                if len(collectedConstraintTokens[1]) > 0:
                        for eachValError in collectedConstraintTokens[1]:
                            self._modelErrorCount.append(eachValError)

            else:
                print("[SYNTAX ERROR]: Unidentified Feature. Feature has no ID property")

        elif propGet == None and subArray['id'] != "root_feature":
            self._modelErrorCount.append(['missing_config'+subArray['id']])
            print("[SYNTAX ERROR]: Feature("+subArray['id']+") has no corresponding binding properties")
        
        if "sub" in subArray:
            for sub in subArray['sub']:
                self.parseModelSubSchema(sub, subArrayBinding)

    
    def parseBindingSchema(self, modelBindingObject):
        for property in modelBindingObject['properties']:
            collectedTokens = []
            collectedPropsTokens = []
            #allcollectedTokens = []
            if "id" in property:
                #register ID token found
                collectedTokens.append("id")
                if self.isAlphanumStringType(property['id']) == False:
                    self._bindingErrorCount.append(['alphanum'])
                    print("[SYNTAX ERROR]: Feature Binding("+property['id']+") has non-alphanumeric charactersIN ID")

                if "props" in property:
                    collectedTokens.append("props")  
                    collectedPropsTokens = self.isValidPropsBlock(property['props'], property['id'])
                else:
                    print("[SYNTAX ERROR]: Feature Binding("+property['id']+") has no PROPS property")

                #Collect Bnding Errors
                allcollectedTokens = collectedTokens + collectedPropsTokens[0]
                languageTokens = self.getLexicon()
                #get missing tokens
                tokenDiff = set(languageTokens['binding']) - set(allcollectedTokens)
                tokenDiff = list(tokenDiff)
        
                #if there is any token missing
                if len(tokenDiff) > 0:
                    missingPropsString = " ".join(tokenDiff)
                    self._bindingErrorCount.append(property['id']+":mprop:"+missingPropsString)
                    print("[SYNTAX ERROR]: Feature Binding("+property['id']+") has missing PROPS "+missingPropsString)

                if len(collectedPropsTokens[1]) > 0:
                    for eachValError in collectedPropsTokens[1]:
                        self._bindingErrorCount.append(eachValError)

            else:
                print("[SYNTAX ERROR]: Unidentified Feature Binding. Feature Binding has no ID property")