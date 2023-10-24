import os, json


class CmdExec():
    def __init__(self) -> None:
        self._bound = []

    def run(self, runnignConfig, featureSrcEntrypoint):
        getBoundFeatures = self.readBound(runnignConfig)
    
        if featureSrcEntrypoint.upper() in getBoundFeatures:
            projectsDir = os.path.dirname(os.path.abspath('mmconsole.py'))
            featuresDirPath = os.path.join(projectsDir, "featx")
            allSrcFiles = [f for f in os.listdir(featuresDirPath) if os.path.isfile(os.path.join(featuresDirPath, f))]
        
            srcToBeExecuted = list(filter(lambda src: src.split(".")[0].lower() == featureSrcEntrypoint, allSrcFiles))
            
            if len(srcToBeExecuted) > 0:
                if srcToBeExecuted[0].split(".")[1] == "cpp":
                    print("[ALERT] C++ source detected")
                    print("[ALERT] Compiling feature '"+ featureSrcEntrypoint+"'")
                    compilePath = os.path.join(featuresDirPath, "mbin")
                    targetCppPath = os.path.join(compilePath, srcToBeExecuted[0].split(".")[0]+".exe")
                    cppSrcFilePath = os.path.join(featuresDirPath, srcToBeExecuted[0])
                    os.system('g++ -o'+ targetCppPath + ' ' + cppSrcFilePath)
                    os.system(targetCppPath)
                else:
                    
                    fullPyPath = os.path.join(featuresDirPath, srcToBeExecuted[0])
                    os.system("python "+ fullPyPath)
            else:
                print("[ALERT] No source file with the name '"+featureSrcEntrypoint+"' exists")
        else:
            print("[ALERT] Cannot execute feature '"+featureSrcEntrypoint+"'. Feature doesnot exist in the set of bound features")

    def load(self):
        pass

    def unload(self):
        pass

    def readBound(self, projectName):
        projectsDir = os.path.dirname(os.path.abspath('.'))
        mainProjPath = os.path.join(projectsDir, projectName)
        bindPath = os.path.join(mainProjPath, 'bindings.motivml')
        bFile = open(bindPath, 'r')
        bState = str(bFile.read()).split("\n")
        bFile.close()
        return bState

    def show(self, runnignConfig, showLevel="all"):
        if showLevel == "all":
            self._bound = []
            modelObj = self.readModelObject(runnignConfig)
            configObj = self.readConfigurationObject(runnignConfig)
            self.treePrint(modelObj, configObj, showLevel)
            print("\n\tNotation:[ m = Mandatory, !m = Optional, o = OR, x = XOR, s = Static, D = Dynamic]")
        elif showLevel == "config":
            self._bound = []
            self._bound = self.readBound(runnignConfig)
            modelObj = self.readModelObject(runnignConfig)
            configObj = self.readConfigurationObject(runnignConfig)
            self.treePrint(modelObj, configObj, showLevel)
            print("\n\tNotation:[ m = Mandatory, !m = Optional, o = OR, x = XOR, s = Static, D = Dynamic]")
        else:
            print("Incorrect parameter passed with command")
        

    def readModelObject(self, projectName):
        projectsDir = os.path.dirname(os.path.abspath('.'))
        mainProjPath = os.path.join(projectsDir, projectName)
        modelPath = os.path.join(mainProjPath, 'model.json')
        mFile = open(modelPath, 'r')
        mState = json.loads(mFile.read())
        mFile.close()
        return mState

    def readConfigurationObject(self, projectName):
        projectsDir = os.path.dirname(os.path.abspath('.'))
        mainProjPath = os.path.join(projectsDir, projectName)
        configPath = os.path.join(mainProjPath, 'config.json')
        cFile = open(configPath, 'r')
        cState = json.loads(cFile.read())
        cFile.close()
        return cState

    def treePrint(self, modelObject, modelBindingObject, param):
        if "sub" in modelObject:
            self.printSubtree(modelObject, modelBindingObject, param)


    def printSubtree(self, subArray, subArrayBinding, param, level='', desc='', group='', mode=''):
        propGet = self.getSingleFeatureProperties(subArray['id'], subArrayBinding)
        
        if propGet != None:
            if subArray['isMandatory'] == False:
                    desc += "!m"
            elif subArray['isMandatory'] == True:
                    desc += "m"

            if subArray['group'] == "XOR":
                group += "x"
            elif subArray['group'] == "OR":
                group += 'o'

            if propGet['props']['mode'] == "Static":
                    mode += "s"
            elif propGet['props']['mode'] == "Dynamic":
                    mode += "D"

        if param == "all":
            print(f'{level}|{desc}--{mode}--{group} '+ subArray['name'] + '--{id: '+ subArray['id']+'}')
        elif param == "config":
            if subArray['id'] in self._bound:
                print(f'{level}|{desc}--{mode}--{group} '+ subArray['name'] + '--{id: '+ subArray['id']+'}')

        
        if "sub" in subArray:
            level += '\t'
            for sub in subArray['sub']:
                self.printSubtree(sub, subArrayBinding, param, level) 

    
    def getSingleFeatureProperties(self, featureID, modelBinding):
        for prop in modelBinding['properties']:
            if prop['id'] == featureID:
                return prop