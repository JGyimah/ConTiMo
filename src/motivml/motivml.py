import os, sys
import json
from motivml.featureModel import FeatureModel

def usage():
    print('motivml.py <model directory name>')

def run(cpp_file, exe_file, proj):
    os.system("echo Compiling " + proj)
    os.system('g++ '+ cpp_file + ' -o ' + exe_file)
    os.system("echo Generating Early Bindings")
    os.system("echo -------------------")
    os.system(exe_file +" "+ proj)

def getModelState(projectName="template", modelPathParam="../template/model.json"):
    modelPathParam = "../" + projectName + "/model.json"
    modelPath = os.path.dirname(os.path.abspath(modelPathParam))
    engineStore = os.path.join(modelPath, 'model.json')
    dataFile = open(engineStore, 'r')
    engineState = json.loads(dataFile.read())
    dataFile.close()
    return engineState

def getConfigurationState(projectName="template", configPathParam="../template/config.json"):
    configPathParam = "../" + projectName + "/config.json"
    configPath = os.path.dirname(os.path.abspath(configPathParam))
    configStore = os.path.join(configPath, 'config.json')
    dataFile = open(configStore, 'r')
    configState = json.loads(dataFile.read())
    dataFile.close()
    return configState

def main(projectName):
    try:
        cpp_file = 'tbind.cpp'
        exe_file = 'tbind.exe'
        run(cpp_file, exe_file, projectName)
    except:
        # print help information and exit
        print("Something went wrong")      
        usage()
        sys.exit(2)
            

if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        commandLineArgProjectName = sys.argv[1]
        modelTemplate = FeatureModel()
        #Generate and save early bindings
        main(commandLineArgProjectName)
        #Validate model schema i.e language sysntax
        modelTemplate.validateModelSchema(getModelState(commandLineArgProjectName), getConfigurationState(commandLineArgProjectName), commandLineArgProjectName)
        #Initiate console interface (Config Run Mode)
        
        
        
           