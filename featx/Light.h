#include <iostream>
#include "../include/motivml_ros/static_base.h"
#include "Configuration.h"

namespace static_integration{

    class Light: public static_base::StaticInterface{
        
        public:
            Feature light;
            Light(){
                light.setId("light");
                light.setName("Light");
                light.setGroup("OR");
                light.setIsMandatory(false);

                Configuration(light, Early, Static);
            };

            void executeFeature(){
                std::cout << light.getName() << "Light feature run successfully" << std::endl;
            };

    };

};