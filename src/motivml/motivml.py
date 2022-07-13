#!/usr/bin/env python

import os, sys, subprocess, platform
import rospy
import json
from motivml.featureModel import FeatureModel

class Dsl(FeatureModel):
    def __init__(self) -> None:
        FeatureModel.__init__(self)


    def usage(self):
        print('motivml.py <model directory name>')


    def run(self, cpp_file, exe_file, proj):
        os.system("echo Compiling " + proj)
        os.system('g++ '+ cpp_file + ' -o ' + exe_file)
        os.system("echo Generating Early Bindings")
        os.system("echo -------------------")
        os.system(exe_file +" "+ proj)


    def getModelState(self, projectName="template", modelPathParam="../template/model.json"):
        modelPathParam = "../" + projectName + "/model.json"
        modelPath = os.path.dirname(os.path.abspath(modelPathParam))
        engineStore = os.path.join(modelPath, 'model.json')
        dataFile = open(engineStore, 'r')
        engineState = json.loads(dataFile.read())
        dataFile.close()
        return engineState


    def getConfigurationState(self, projectName="template", configPathParam="../template/config.json"):
        configPathParam = "../" + projectName + "/config.json"
        configPath = os.path.dirname(os.path.abspath(configPathParam))
        configStore = os.path.join(configPath, 'config.json')
        dataFile = open(configStore, 'r')
        configState = json.loads(dataFile.read())
        dataFile.close()
        return configState


    def main(self, projectName):
        user_platform = platform.system()
        print("## "+user_platform + " platform detected")
        try:
            print("## Initialising static binding")
            if user_platform == "Windows":
                cpp_file = 'sebind.cpp'
                exe_file = 'sebind.exe'
            else:
                cpp_file = 'sebind.cpp'
                exe_file = 'a.out'
            self.run(cpp_file, exe_file, projectName)
        except:
            # print help information and exit
            print("Something went wrong")      
            self.usage()
            sys.exit(2)


    def initConfigParamServer(self, selectedProject):
        print("## Initialising server params")
        searlyBound = []
        dearlyBound = []
        slateBound = []
        dlateBound = []
        
        selectedProjConfig = self.getConfigurationState(selectedProject)
        
        for propertyObject in selectedProjConfig['properties']:
            if propertyObject["props"]["time"].lower() == "early" and propertyObject["props"]["mode"].lower() == "static":
                searlyBound.append(propertyObject['id'])
            
            if propertyObject["props"]["time"].lower() == "late" and propertyObject["props"]["mode"].lower() == "static":
                slateBound.append(propertyObject['id'])

            if propertyObject["props"]["time"].lower() == "early" and propertyObject["props"]["mode"].lower() == "dynamic":
                dearlyBound.append(propertyObject['id'])

            if propertyObject["props"]["time"].lower() == "late" and propertyObject["props"]["mode"].lower() == "dynamic":
                dlateBound.append(propertyObject['id'])

        #Save to config param server yaml
        rospy.set_param("/motivml/static_early", searlyBound)
        rospy.set_param("/motivml/static_late", slateBound)
        rospy.set_param("/motivml/dynamic_early", dearlyBound)
        rospy.set_param("/motivml/dynamic_late", dlateBound)
        print("## Server params set successfully")
        



    def dslLaunch(self, commandLineArgProjectName):
        #Generate and save static early bindings
        #self.main(commandLineArgProjectName)
        #Validate model schema i.e language sysntax
        self.validateModelSchema(self.getModelState(commandLineArgProjectName), self.getConfigurationState(commandLineArgProjectName), commandLineArgProjectName)
        #Initiate console interface (Config Run Mode)