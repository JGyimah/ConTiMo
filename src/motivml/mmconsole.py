#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sys, os, json
from motivml.cmdExec import CmdExec
from motivml.motivml import Dsl
from motivml.traverse import Traverse
#custom ROS msg to store/transmit feature config object
from motivml_ros.msg import ConfigCommand

try:
    import readline
except ImportError:
    import pyreadline as readline

cmdexec = CmdExec()

class Mmconsole():
    def __init__(self) -> None:
        self.runningConfig = ""
        self._modelTree = None
        self._configProps = None

    def getListOfFeatureIds(self):
        allProps = cmdexec.readConfigurationObject(self.runningConfig)
        allIds = [prop['id'] for prop in allProps['properties']]
        return allIds

    def idCompleter(self, text, state):
        fids = self.getListOfFeatureIds()
        options = [fid for fid in fids if fid.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

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

    def generateEarlyBindings(self, projectName):
        configSettings = CmdExec()
        cObj = configSettings.readConfigurationObject(projectName)
        early_features = []
        for feature in cObj["properties"]:
            if feature["props"]["time"] == "Early":
                early_features.append(feature["id"])
        
        self.writeToBindingFile(early_features, projectName)

    def writeToBindingFile(self, early_binding_list, pName):
        projectsDir = os.path.dirname(os.path.abspath('.'))
        mainProjPath = os.path.join(projectsDir, pName)
        bindingsPath = os.path.join(mainProjPath, 'bindings.motivml')
        try:
            with open(bindingsPath, 'w') as f:
                f.write('\n'.join(early_binding_list))
            print("-- Early bindings generated successfully")
        except:
            print("Writing ids of early features threw an exception")


    def runConsoleInterface(self, executedConfig):
        configSettings = CmdExec()
        configValues = Traverse()
        cObj = configSettings.readConfigurationObject(executedConfig[1])
        
        #initialise  modeller interface node
        rospy.init_node("configuration_interface")
        rospy.loginfo("DSL has been initialised")
        rate = rospy.Rate(2) #Publishing rate in Hertz
        pub = rospy.Publisher("/variability_command", ConfigCommand, queue_size=2)

        #Autocomplete invokation
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.idCompleter)

        self.runningConfig = executedConfig[1]
        prepedPrompt = "MoTiVML:" + self.prepCmdPrompt()
        while not rospy.is_shutdown():
            while(True):
                cmdline = input(prepedPrompt)
                if not cmdline or cmdline[0] == '#' or len(cmdline) == 0:
                    continue
                elif cmdline.strip().lower() == 'exit':
                    confirmation = self.sanitizeCommand(input(prepedPrompt +" Confirm exit (y/n): "))
                    if confirmation[0] == 'y' or confirmation[0] =='Y':
                        break #break out of console loop
                    elif confirmation[0] != 'n' and confirmation[0] != 'y':
                        print("Invalid exit confirmation value provided. Try again")
                else:
                    #get command and run it
                    print("\n")
                    if self.sanitizeCommand(cmdline)[0] == "load" or self.sanitizeCommand(cmdline)[0] == "unload" or self.sanitizeCommand(cmdline)[0] == "dump":
                        if self.sanitizeCommand(cmdline)[0] != "dump":
                            cIdSetting = configValues.getProperties(self.sanitizeCommand(cmdline)[1], cObj)
                        
                        if(self.sanitizeCommand(cmdline)[0] == "dump"):
                            msg = ConfigCommand()
                            msg.command = self.sanitizeCommand(cmdline)[0]
                            msg.featureid = "ALL"
                            msg.btime = "N/A"
                            msg.bmode = "N/A"
                            pub.publish(msg)
                            rate.sleep()
                        else:
                            msg = ConfigCommand()
                            msg.command = self.sanitizeCommand(cmdline)[0]
                            msg.featureid = self.sanitizeCommand(cmdline)[1]
                            msg.btime = cIdSetting["props"]["time"]
                            msg.bmode = cIdSetting["props"]["mode"]
                            pub.publish(msg)
                            rate.sleep()
                    else:
                        self.runCommand(self.sanitizeCommand(cmdline))
                    #print("\n")
            break #break out of ROS node loop

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
    language = Dsl()
    schemaCheck = Traverse()
    if(len(sys.argv) >= 2):
        #check if project exists and model and binding files exist
        validityCheckResults = mmconsole.checkCommandValidity(sys.argv)
        #do schema pass to certify that there arent any errors in model
        if validityCheckResults == "valid":
            #Load server params
            language.initConfigParamServer(sys.argv[1])
            #Generate and save early bindings
            mmconsole.generateEarlyBindings(sys.argv[1]) #py impl
            #language.main(sys.argv[1]) #cpp impl
            #begin model validation
            schemaCheck.parseModelSchema(mmconsole._modelTree, mmconsole._configProps, sys.argv[1])
            if schemaCheck.excludesErrorCount == 0 and schemaCheck.includesErrorCount == 0 and schemaCheck.parentChildErrorCount == 0 and schemaCheck.bindingPropErrorCount == 0:
                if len(schemaCheck._modelErrorCount) > 0:
                    print("[ALERT] Couldnot launch console. Modelling Error(s) Detected. Fix Error(s) to Proceed")
                else:
                    mmconsole.runConsoleInterface(sys.argv)
            else:
                print("[ERRORS DETECTED] Console failed to launch. Model and Configuration Errors were Detected")