#include <iostream>
#include "../include/motivml_ros/plugin_base.h"

namespace motivml_plugins{
class Hands: public plugin_base::PluginInterface{
        private:
            std::vector<std::string> ex{"pointscloud"};

        public:
            Hands(){
                Feature::setId("hands");
                Feature::setName("Hands");
                Feature::setFeaturesExcluded(ex);
                Feature::setGroup("XOR");
                Feature::setIsMandatory(false);

                Configuration::setTimeBinding(Late);
                Configuration::setModeBinding(Dynamic);
            };

            void executeFeature(){
                std::cout << Feature::getName() << "feature run successfully" << std::endl;
            };

    };
};