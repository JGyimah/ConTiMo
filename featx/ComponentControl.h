#include <iostream>
#include "../include/motivml_ros/static_base.h"
#include "Configuration.h"

namespace static_integration{

    class ComponentControl: public static_base::StaticInterface{
       
        public:
            Feature cctrl;
            ComponentControl(){
                cctrl.setId("compcontrol");
                cctrl.setName("ComponentControl");
                cctrl.setGroup("OR");
                cctrl.setIsMandatory(true);

                Configuration(cctrl, Early, Static);
            }

            void executeFeature(){
                std::cout << cctrl.getName() << "feature run successfully" << std::endl;
            };

    };

};