#include <iostream>
#include "../include/motivml_ros/plugin_base.h"
#include "Configuration.h"

namespace motivml_plugins{

    class Slam: public plugin_base::PluginInterface{
        
        public:
            Feature slam;
            Slam(){
                slam.setId("slam");
                slam.setName("SLAM");
                slam.setGroup("XOR");
                slam.setIsMandatory(false);
                
                Configuration(slam, Early, Static);
            };

            void executeFeature(){
                std::cout << slam.getName() << "feature run successfully" << std::endl;
            };

    };

};