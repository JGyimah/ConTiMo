#include <iostream>
#include "../include/motivml_ros/plugin_base.h"

namespace motivml_plugins{
class Pointscloud: public plugin_base::PluginInterface{
        std::string feature_id = "pointscloud";
        public:
            Pointscloud(){};

            void executeFeature(){
                std::cout << "Pointscloud [dynamic] feature run successfully" << std::endl;
            };

    };
};