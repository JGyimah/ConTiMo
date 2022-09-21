#include <iostream>
#include "../include/motivml_ros/static_base.h"

namespace static_integration{

    class ComponentControl: public static_base::StaticInterface{
       
        public:
            ComponentControl(){
                Feature::setId("compcontrol");
                Feature::setName("ComponentControl");
                Feature::setGroup("OR");
                Feature::setIsMandatory(true);

                Configuration::setTimeBinding(Early);
                Configuration::setModeBinding(Static);
            }

            void executeFeature(){
                std::cout << Feature::getName() << "feature run successfully" << std::endl;
            };

    };

};