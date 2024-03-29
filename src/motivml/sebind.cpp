#include <windows.h>
#include <cstdio>
#include <string>
#include <limits.h>
#include <fstream>
#include <filesystem>
#include <cctype>
#include <iostream>
#include "json/single_include/nlohmann/json.hpp"

#define COMPILE_TIME 1

using namespace std;

string early_bindings {""};

void traverse(nlohmann::json &subArray){
    if(subArray.is_object() && subArray.contains("id")){
       cout << subArray["id"] << endl;
       cout << "-----------------------------------" << endl;
    }

    for (auto obj : subArray) {
            if(obj.is_array()){
                traverse(obj);
            }else{
                if(obj.is_object()){
                    traverse(obj);
                }
            }
        }
}

void configurationIteration(nlohmann::json &configJsonData){

    for(auto& configObj : configJsonData){
        if(configObj.is_array()){
            configurationIteration(configObj);
        }else{
            
            string idStr = to_string(configObj["id"]);
            string timeStr = to_string(configObj["props"]["time"]);
            string modeStr = to_string(configObj["props"]["mode"]);

            transform(timeStr.begin(), timeStr.end(), timeStr.begin(), ::tolower); // convert time string iterable to lower case
            timeStr.erase(std::remove(timeStr.begin(),timeStr.end(),'\"'),timeStr.end()); // remove trailing newline character from time string

            transform(modeStr.begin(), modeStr.end(), modeStr.begin(), ::tolower); // convert mode string iterable to lower case
            modeStr.erase(std::remove(modeStr.begin(),modeStr.end(),'\"'),modeStr.end()); // remove trailing newline character from mode string
            
            const string EARLY_BINDING_TIME = "early";
            //const string STATIC_BINDING_MODE = "static";

            if(timeStr == EARLY_BINDING_TIME){
                //only bind features with early binding time at this moment
                idStr.erase(std::remove(idStr.begin(),idStr.end(),'\"'),idStr.end());
                early_bindings += idStr + "\n";

                //printf("%s %s binding for model completed\n", STATIC_BINDING_MODE, EARLY_BINDING_TIME);
                cout <<"Feature ["+ idStr + "] selected" << endl;
            }
            
        }
    }

}

void modelIteration(nlohmann::json& jsonData){
    traverse(jsonData);
}

void readModel(string modelPath, string projDir="template"){
    int motivmlpo = modelPath.find("motivml");
    string subPath = modelPath.substr(0, motivmlpo + 11)+ "\\src\\" + projDir +"\\model.json";
    
    fstream modelfile;
    modelfile.open(subPath, ios::in);

    if(modelfile.is_open()){
        cout << "Reading model: " << subPath << endl;
        nlohmann::json jsonData = nlohmann::json::parse(modelfile);
        modelIteration(jsonData);
        modelfile.close();
    }else{
        cout << "model file could not be opened - path: " << subPath << endl;
    }
}

void readConfiguration(string modelPath, string projDir="template"){
    int motivmlpo = modelPath.find("motivml");
    string subPath = modelPath.substr(0, motivmlpo + 11)+ "\\src\\" + projDir +"\\config.json"; //old path manip
    
    fstream modelfile;
    modelfile.open(subPath, ios::in);

    if(modelfile.is_open()){
        cout << "Reading configuration: " << subPath << endl;
        nlohmann::json jsonData = nlohmann::json::parse(modelfile);
        configurationIteration(jsonData);
        modelfile.close();
    }else{
        cout << "config file could not be opened - path: " << subPath << endl;
    }

}

string getCurrentDir() {
        //add linux file get file directory
        char buff[MAX_PATH];
        GetModuleFileNameA( NULL, buff, MAX_PATH );
        string::size_type position = string( buff ).find_last_of( "\\/" );
        return string( buff ).substr( 0, position);
}

void generateAndSaveBindings(string projDir="template"){
    ofstream bindingFile;

    string currentDir = getCurrentDir();

    int motivmlpo = currentDir.find("motivml");
    string outputFilePath = currentDir.substr(0, motivmlpo + 11)+ "\\src\\" + "\\" + projDir +"\\bindings.motivml";

    bindingFile.open(outputFilePath);
    bindingFile << early_bindings;
    bindingFile.close();

}

int main(int argc, char* argv[]){
    #if COMPILE_TIME
    //static early binding
    string projectName = argv[1];
    readConfiguration(getCurrentDir(), projectName);
    //generate and save static bindings in custom .motvml file
    generateAndSaveBindings(projectName);
    printf("Compile time exited successfully\n\n");
    #endif

    return 0;
}