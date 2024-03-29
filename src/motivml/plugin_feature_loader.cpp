//Static early definitions begin
#define AMCL
#define MTNPLNCTRL
#define COMPCTRL
#define LIGHT
//Static early definitions end
#include <stdlib.h>
#include <pluginlib/class_loader.h>
#include <cctype>
#include <map>
#include <sys/stat.h>
#include <algorithm>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <motivml_ros/ConfigCommand.h>
#include <vector>
#include "../../include/motivml_ros/plugin_base.h"
#include "../../include/motivml_ros/static_base.h"
#include "static_feature_loader.h"


//dynamic early map of plugin objects
std::vector<std::string> static_early_server_params;
pluginlib::ClassLoader<plugin_base::PluginInterface> dynamic_plugin_loader("motivml_ros", "plugin_base::PluginInterface");
pluginlib::ClassLoader<static_base::StaticInterface> static_plugin_loader("motivml_ros", "static_base::StaticInterface");
std::map<std::string, boost::shared_ptr<plugin_base::PluginInterface>> dynamic_objects;
std::map<std::string, boost::shared_ptr<static_base::StaticInterface>> static_late_objects;

void load_dynamic_early(){

    ros::NodeHandle dynamicEarlyNodeHandler;
    std::vector<std::string> dynamic_early_server_params;
    dynamicEarlyNodeHandler.getParam("/motivml/dynamic_early", dynamic_early_server_params);

    if (dynamic_early_server_params.size() > 0){
        
        for(std::string defid : dynamic_early_server_params){
            std::string lowerFid = defid;
            lowerFid[0] = toupper(lowerFid[0]);
            std::string instanceCreatString = "motivml_plugins::"+ lowerFid;
            try{
                dynamic_objects[defid] = dynamic_plugin_loader.createInstance(instanceCreatString);
            }catch(pluginlib::PluginlibException& ex){
                ROS_INFO("Dynamic Early Plugin Instance Creation Error. Error: %s", ex.what());
            }
            std::string info_message = "## Dynamic Early "+lowerFid+" has been bound";
            ROS_INFO(info_message.c_str());
        }
        
    }else{
        ROS_INFO("*** No dynamic early features found");
    }


}

void load_static_late(){
    ros::NodeHandle staticLateNodeHandler;
    std::vector<std::string> static_late_server_params;
    staticLateNodeHandler.getParam("/motivml/static_late", static_late_server_params);

    if (static_late_server_params.size() > 0){
        
        for(std::string slfid : static_late_server_params){
            std::string lowerFid = slfid;
            lowerFid[0] = toupper(lowerFid[0]);
            std::string instanceCreatString = "static_integration::"+ lowerFid;
            try{
                static_late_objects[slfid] = static_plugin_loader.createInstance(instanceCreatString);
            }catch(pluginlib::PluginlibException& ex){
                ROS_INFO("Static Late Plugin Instance Creation Error. Error: %s", ex.what());
            }
            std::string info_message = "## Static Late "+lowerFid+" has been bound";
            ROS_INFO(info_message.c_str());
        }
        
    }else{
        ROS_INFO("*** No static late features found");
    }

}

void load_static_late_feature(std::string &featurue_id){

    std::string lowerFid = featurue_id;
    lowerFid[0] = toupper(lowerFid[0]);
    std::string instanceCreatString = "static_integration::"+ lowerFid;
    try{
        static_late_objects[featurue_id] = static_plugin_loader.createInstance(instanceCreatString);
    }catch(pluginlib::PluginlibException& ex){
        ROS_INFO("Static Late Plugin Instance Creation Error. Error: %s", ex.what());
    }
    std::string info_message = "## Static Late "+lowerFid+" has been bound";
    ROS_INFO(info_message.c_str());

}

void callback_load_plugin_features(const motivml_ros::ConfigCommand& msg){

        ROS_INFO("Command: %s, Feature ID: %s, Time: %s, Mode: %s", msg.command.c_str(), msg.featureid.c_str(), msg.btime.c_str(), msg.bmode.c_str());
        printf("\n----------------------------------------------------\n");

        std::string command = msg.command.c_str();
        std::string featureid = msg.featureid.c_str();
        std::string btime = msg.btime.c_str();
        std::string bmode = msg.bmode.c_str();

        try{
            
            if(command == "load"){

                ROS_INFO("## Attempting to load feature %s", featureid);

                if(bmode == "Static"){
                    
                    if(btime == "Early"){
                        //instantiate and run
                        if(featureid == "compcontrol"){
                            ROS_INFO("## Found static early feature");
                            static_integration::ComponentControl compctrl;
                            compctrl.executeFeature();
                        }else if(featureid == "amcl"){
                            ROS_INFO("## Found static early feature");
                            static_integration::Amcl amcl;
                            amcl.executeFeature();
                        }else if(featureid == "motplannctrl"){
                            ROS_INFO("## Found static early feature");
                            static_integration::MotionPlanningControl motplctrl;
                            motplctrl.executeFeature();
                        }else if(featureid == "light"){
                            ROS_INFO("## Found static early feature");
                            static_integration::Light light;
                            light.executeFeature();
                        }

                    }else if(btime == "Late"){
                        //find plugin instance and run i.e loadable static feature at runtime but unloadable forever
                        ROS_INFO("## Found static late feature");
                        load_static_late_feature(featureid);
                        static_late_objects[featureid]->executeFeature();
                        
                    }

                }else if(bmode == "Dynamic"){
                    //check if exists in dynamic_objects
                    if(dynamic_objects.find(featureid) == dynamic_objects.end()){
                            ///if doesnot exist, push in object and run from object
                            ROS_INFO("-- Dynamic feature doesnot exist in configuration");
                            std::string recievedID = featureid;
                            recievedID[0] = toupper(recievedID[0]);
                            std::string CPP_FEATURE_CLASS_PATH = "../../"+recievedID+".h";
                            struct stat sb;
                            if(stat(CPP_FEATURE_CLASS_PATH.c_str(), &sb) == 0){
                                //if there exists a c++ feature header with said name
                                std::string classInstance = "motivml_plugins::"+ recievedID;
                                try{
                                    ROS_INFO("-- Loading dynamic feature into configuration");
                                    dynamic_objects[featureid] = dynamic_plugin_loader.createInstance(classInstance);
                                    dynamic_objects[featureid]->executeFeature();
                                }catch(pluginlib::PluginlibException& ex){
                                    ROS_INFO("Dynamic Plugin Instance Creation Error. Error: %s", ex.what());
                                }
                            }else{
                                //else if there exists NO c++ feature header with said name
                                ROS_INFO("-- No feature class of type Cpp found");
                            }

                        }else{
                            //if exists, run it
                            ROS_INFO("-- Found dynamic feature");
                            ROS_INFO("-- Executing dynamic feature");
                            dynamic_objects[featureid]->executeFeature();
                        }
                    
                    
                }

            }else if(command == "unload"){

                ROS_INFO("## Attempting to unload feature %s", featureid);

                if(bmode == "Static"){

                    ROS_INFO("-- Static configuration cannot be altered at runtime");

                }else if(bmode == "Dynamic"){
                    
                    //check if exists in dynamic_objects
                    if(dynamic_objects.find(featureid) == dynamic_objects.end()){
                         //if doesnot exist in cpp form
                        ROS_INFO("-- No corresponding Cpp feature exists for specified unload");
                    }else{
                        //if exists, unload and print unload success message
                        dynamic_objects.erase(featureid);
                        ROS_INFO("-- Dynamic Cpp feature unloaded successfully");
                    }
                }

            }else if(command == "dump"){

                ROS_INFO("## Dumping All Bindings");
                printf("\n----------------------------------------------------\n");
                printf("-- Static");
                printf("\n----------------------------------------------------\n");
                std::map<std::string, boost::shared_ptr<static_base::StaticInterface>>::iterator statIter;
                //static early dump
                for(std::string seid: static_early_server_params){
                    printf(seid.c_str());
                    printf("\n");
                }
                //static late dump
                for(statIter = static_late_objects.begin(); statIter != static_late_objects.end(); statIter++){
                    printf(statIter->first.c_str());
                    printf("\n");
                }
                printf("\n----------------------------------------------------\n");
                printf("-- Dynamic");
                printf("\n----------------------------------------------------\n");
                std::map<std::string, boost::shared_ptr<plugin_base::PluginInterface>>::iterator dyIter;
                for(dyIter = dynamic_objects.begin(); dyIter != dynamic_objects.end(); dyIter++){
                    printf(dyIter->first.c_str());
                    printf("\n");
                }
                printf("\n----------------------------------------------------\n");

            }

        }catch(pluginlib::PluginlibException& ex){
            ROS_ERROR("The feature you are attempting to load is not available in the configuration. Error: %s", ex.what());
        }
}

int main(int argc, char** argv){

    ros::init(argc, argv, "plugin_builder");
    ros::NodeHandle nh;

    //Read static early features
    nh.getParam("/motivml/static_early", static_early_server_params);

    ROS_INFO("## Loading Static");
    //load py early features from launchfile
    //std::system("roslaunch motivml_ros py_early.launch");
    //load all features bound at dynamic early
    ROS_INFO("## Initialising dynamic early features");
    //load cpp-based dynamic early features
    load_dynamic_early();
    
    ROS_INFO("## Feature Plugin Loader is Listening for Configuration Interface Commands");
    
    ros::Subscriber sub = nh.subscribe("/variability_command", 100, callback_load_plugin_features);

    ros::spin();
    return 0;

}