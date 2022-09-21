#include <iostream>
#include "../include/motivml_ros/plugin_base.h"

namespace motivml_plugins{
class Pointscloud: public plugin_base::PluginInterface{
        private:
            std::vector<std::string> ex{"hands"};
        public:
            Pointscloud(){
                Feature::setId("pointscloud");
                Feature::setName("PointsCloud");
                Feature::setFeaturesExcluded(ex);
                Feature::setGroup("XOR");
                Feature::setIsMandatory(false);

                Configuration::setTimeBinding(Late);
                Configuration::setModeBinding(Dynamic);
            }

            void executeFeature(){
                std::cout << Feature::getName() << "feature run successfully" << std::endl;
            };

    };
};