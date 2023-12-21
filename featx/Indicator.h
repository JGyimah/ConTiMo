#include <iostream>
#include "../include/motivml_ros/plugin_base.h"
#include "Configuration.h"

namespace motivml_plugins{
class Indicator: public plugin_base::PluginInterface{
        private:
            std::vector<std::string> ex{"uvc"};

        public:
            Feature indicator;
            Indicator(){
                indicator.setId("indicator");
                indicator.setName("Indicator");
                indicator.setFeaturesExcluded(ex);
                indicator.setGroup("OR");
                indicator.setIsMandatory(false);

                Configuration(indicator, Late, Dynamic);
            };

            void executeFeature(){
                std::cout << indicator.getName() << "Indicator feature run successfully" << std::endl;
            };

    };
};