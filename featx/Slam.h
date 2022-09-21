#include <iostream>
#include "../include/motivml_ros/plugin_base.h"

namespace motivml_plugins{

    class Slam: public plugin_base::PluginInterface{
        
        public:
            Slam(){
                Feature::setId("slam");
                Feature::setName("SLAM");
                Feature::setGroup("XOR");
                Feature::setIsMandatory(false);

                Configuration::setTimeBinding(Early);
                Configuration::setModeBinding(Static);
            };

            void executeFeature(){
                std::cout << Feature::getName() << "feature run successfully" << std::endl;
            };

    };

};