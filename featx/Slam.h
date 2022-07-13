#include <iostream>
#include "../include/motivml_ros/plugin_base.h"

namespace motivml_plugins{

    class Slam: public plugin_base::PluginInterface{
        std::string feature_id = "slam";
        public:
            Slam(){};

            void executeFeature(){
                std::cout << "Slam [static] feature run successfully" << std::endl;
            };

    };

};