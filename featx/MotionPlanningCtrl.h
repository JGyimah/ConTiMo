#include <iostream>
#include "../include/motivml_ros/static_base.h"
#include "Configuration.h"

namespace static_integration{

    class MotionPlanningControl: public static_base::StaticInterface{
        
        public:
            Feature mpctrl;
            MotionPlanningControl(){
                mpctrl.setId("motplannctrl");
                mpctrl.setName("MotionPlanningAndControl");
                mpctrl.setGroup("OR");
                mpctrl.setIsMandatory(true);

                Configuration(mpctrl, Early, Static);
            }

            void executeFeature(){
                std::cout << mpctrl.getName() << "feature run successfully" << std::endl;
            };

    };

};