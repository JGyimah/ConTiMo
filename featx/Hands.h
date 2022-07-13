#include <iostream>
#include "../include/motivml_ros/plugin_base.h"

namespace motivml_plugins{
class Hands: public plugin_base::PluginInterface{
        std::string feature_id = "hands";
        public:
            Hands(){};

            void executeFeature(){
                std::cout << "Hands [dynamic] feature run successfully" << std::endl;
            };

    };
};