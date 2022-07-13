#include <pluginlib/class_loader.h>
#include <cctype>
#include <map>
#include <algorithm>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <motivml_ros/ConfigCommand.h>
#include <vector>
#include "../../include/motivml_ros/plugin_base.h"

//dynamic early map of plugin objects
std::map<std::string, boost::shared_ptr<plugin_base::PluginInterface>> dynamic_objects;

void callback_load_plugin_features(const motivml_ros::ConfigCommand& msg){

        ROS_INFO("Command received: %s", msg.command.c_str());
        ROS_INFO("Feature ID received: %s", msg.featureid.c_str());
        ROS_INFO("Time received: %s", msg.btime.c_str());
        ROS_INFO("Mode received: %s", msg.bmode.c_str());
        printf("\n----------------------------------------------------\n");

        std::string command = msg.command.c_str();
        std::string featureid = msg.featureid.c_str();
        std::string btime = msg.btime.c_str();
        std::string bmode = msg.bmode.c_str();

        try{
            if(command == "use"){
                printf("command you sent is:",command);
                std::vector<std::string> dynamic_late;
                ros::NodeHandle dl;
                pluginlib::ClassLoader<plugin_base::PluginInterface> dynamic_late_plugin_loader("motivml_ros", "plugin_base::PluginInterface");
                
                dl.getParam("/motivml/dynamic_late", dynamic_late);
                std::string connmadFeatureID = msg.featureid.c_str();

                for(std::string dlfid : dynamic_late){

                    if(dlfid == connmadFeatureID){
                        std::string dlInstanceString = connmadFeatureID;
                        dlInstanceString[0] = toupper(dlInstanceString[0]);
                        std::string dlInstanceCreatString = "motivml_plugins::"+ dlInstanceString;
                        boost::shared_ptr<plugin_base::PluginInterface> sldl_feature_instance = dynamic_late_plugin_loader.createInstance(dlInstanceCreatString);
                        sldl_feature_instance->executeFeature();
                        std::string info_message = "## Dynamic Late "+dlInstanceString+" has been bound";
                        ROS_INFO(info_message.c_str());
                    }

                }
                
            }else{
                ROS_INFO("Dynamic Late ELSE Command Block");
            }

        }catch(pluginlib::PluginlibException& ex){
            ROS_ERROR("The feature you are attempting to load is not available in the configuration. Error: %s", ex.what());
        }
}

int main(int argc, char** argv){

    ros::init(argc, argv, "plugin_builder");
    ros::NodeHandle nh;
    pluginlib::ClassLoader<plugin_base::PluginInterface> dynamic_plugin_loader("motivml_ros", "plugin_base::PluginInterface");
    ROS_INFO("## Initialising dynamic early feature objects");

    std::vector<std::string> dynamic_early;
    nh.getParam("/motivml/dynamic_early", dynamic_early);

    //Dynamic early binding
    if (dynamic_early.size() > 0){
        
        for(std::string fid : dynamic_early){
            ROS_INFO(fid.c_str());
            std::string instanceString = fid;
            instanceString[0] = toupper(instanceString[0]);
            std::string instanceCreatString = "motivml_plugins::"+ instanceString;
            dynamic_objects[fid] = dynamic_plugin_loader.createInstance(instanceCreatString);
            std::string info_message = "## Dynamic Early "+instanceString+" has been bound";
            ROS_INFO(info_message.c_str());

        }
        
    }else{
        ROS_INFO("*** No dynamic early features found");
    }

    
    
    ROS_INFO("## Feature Plugin Loader is Listening for Configuration Interface Commands");
    
    ros::Subscriber sub = nh.subscribe("/variability_command", 100, callback_load_plugin_features);

    ros::spin();
    ROS_INFO("#### DYNAMIC LATE MARKER REACHED ####");
    return 0;

}