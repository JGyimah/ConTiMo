#include <iostream>
#include "../include/motivml_ros/plugin_base.h"
#include "Configuration.h"

namespace motivml_plugins{
class Uvc: public plugin_base::PluginInterface{
        private:
            std::vector<std::string> ex{"indicator"};

        public:
            Feature uvc;
            Uvc(){
                uvc.setId("uvc");
                uvc.setName("Uvc");
                uvc.setFeaturesExcluded(ex);
                uvc.setGroup("OR");
                uvc.setIsMandatory(false);

                Configuration(uvc, Late, Dynamic);
            };

            void executeFeature(){
                std::cout << uvc.getName() << "UVC feature run successfully" << std::endl;
            };

    };
};