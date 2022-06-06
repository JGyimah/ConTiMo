import sys, os, json
from motivml.cmdExec import CmdExec
from motivml.motivml import main
from motivml.traverse import Traverse

cmdexec = CmdExec()

class Mmconsole():
    def __init__(self) -> None:
        self.runningConfig = ""
        self._modelTree = None
        self._configProps = None

    def runCommand(self, cmd):
        if cmd[0] == "show":
            getattr(cmdexec, cmd[0])(self.runningConfig, cmd[1])
        if cmd[0] == "run":
            getattr(cmdexec, cmd[0])(self.runningConfig, cmd[1])

    def sanitizeCommand(self, cmd):
        sanitized = cmd.strip().lower()
        return sanitized.split()

    def prepCmdPrompt(self):
        return "["+self.runningConfig+"]>> "

    def runConsoleInterface(self, executedConfig):
        self.runningConfig = executedConfig[1]
        prepedPrompt = "MoTiVML:" + self.prepCmdPrompt()
        while(True):
            cmdline = input(prepedPrompt)
            if not cmdline or cmdline[0] == '#' or len(cmdline) == 0:
                continue
            elif cmdline.strip().lower() == 'exit':
                confirmation = self.sanitizeCommand(input(prepedPrompt +" Confirm exit (y/n): "))
                if confirmation[0] == 'y' or confirmation[0] =='Y':
                    break
                elif confirmation[0] != 'n' and confirmation[0] != 'y':
                    print("Invalid exit confirmation value provided. Try again")
            else:
                #get command and run it
                print("\n")
                self.runCommand(self.sanitizeCommand(cmdline))
                print("\n")

    def checkCommandValidity(self, commandArray):
        existsResult = self.modelFilesExists(commandArray[1])
        #if project files exist, checkexistence and length of command
        if existsResult == "all_files_exist":
            return "valid"
        else:
            return "invalid"


    def getConsoleCommands(self):
        ccommandsPath = os.path.dirname(os.path.abspath('consoleCmds.json'))
        consoleCommandStore = os.path.join(ccommandsPath, 'consoleCmds.json')
        dataFile = open(consoleCommandStore, 'r')
        consoleCommandState = json.loads(dataFile.read())
        dataFile.close()
        return consoleCommandState

    def modelFilesExists(self, projectName):
        projectsDir = os.path.dirname(os.path.abspath('.'))
        mainProjPath = os.path.join(projectsDir, projectName)
        modelPath = os.path.join(mainProjPath, 'model.json')
        configPath = os.path.join(mainProjPath, 'config.json')

        if (not os.path.exists(modelPath)) and (not os.path.exists(configPath)):
            print("Could not find either a model.json or a config.json in Project("+projectName+")")
            return "project_file_exists_error"
        else:
            #load and read model
            modelFile = open(modelPath, 'r')
            self._modelTree = json.loads(modelFile.read())
            #load and read config
            configFile = open(configPath, 'r')
            self._configProps = json.loads(configFile.read())

            modelFile.close()
            configFile.close()
        
        return "all_files_exist"
        

if __name__=='__main__':
    mmconsole = Mmconsole()
    schemaCheck = Traverse()
    if(len(sys.argv) >= 2):
        #check if project exists and model and binding files exist
        validityCheckResults = mmconsole.checkCommandValidity(sys.argv)
        #do schema pass to certify that there arent any errors in model
        if validityCheckResults == "valid":
            main(sys.argv[1])
            schemaCheck.parseModelSchema(mmconsole._modelTree, mmconsole._configProps, sys.argv[1])
            if schemaCheck.excludesErrorCount == 0 and schemaCheck.includesErrorCount == 0 and schemaCheck.parentChildErrorCount == 0 and schemaCheck.bindingPropErrorCount == 0:
                if len(schemaCheck._modelErrorCount) > 0:
                    print("[ALERT] Couldnot launch console. Modelling Error(s) Detected. Fix Error(s) to Proceed")
                else:
                    mmconsole.runConsoleInterface(sys.argv)
            else:
                print("[ERRORS DETECTED] Console failed to launch. Model and Configuration Errors were Detected")