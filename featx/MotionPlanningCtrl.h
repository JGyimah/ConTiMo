#include <iostream>
#include "../include/motivml_ros/static_base.h"

namespace static_integration{

    class MotionPlanningControl: public static_base::StaticInterface{
        
        public:
            MotionPlanningControl(){
                Feature::setId("motplannctrl");
                Feature::setName("MotionPlanningAndControl");
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