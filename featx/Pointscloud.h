#include <iostream>
#include "../include/motivml_ros/plugin_base.h"
#include "Configuration.h"

namespace motivml_plugins{
class Pointscloud: public plugin_base::PluginInterface{
        private:
            std::vector<std::string> ex{"hands"};
        public:
            Feature pcloud;
            Pointscloud(){
                pcloud.setId("pointscloud");
                pcloud.setName("PointsCloud");
                pcloud.setFeaturesExcluded(ex);
                pcloud.setGroup("XOR");
                pcloud.setIsMandatory(false);

                Configuration(pcloud, Late, Dynamic);
            }

            void executeFeature(){
                std::cout << pcloud.getName() << "feature run successfully" << std::endl;
            };

    };
};