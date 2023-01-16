#include <iostream>
#include "../include/motivml_ros/plugin_base.h"
#include "Configuration.h"

namespace motivml_plugins{
class Hands: public plugin_base::PluginInterface{
        private:
            std::vector<std::string> ex{"pointscloud"};

        public:
            Feature hands;
            Hands(){
                hands.setId("hands");
                hands.setName("Hands");
                hands.setFeaturesExcluded(ex);
                hands.setGroup("XOR");
                hands.setIsMandatory(false);

                Configuration(hands, Late, Dynamic);
            };

            void executeFeature(){
                std::cout << hands.getName() << "feature run successfully" << std::endl;
            };

    };
};