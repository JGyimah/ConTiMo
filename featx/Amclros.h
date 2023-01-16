#include <iostream>
#include "../include/motivml_ros/static_base.h"
#include "Configuration.h"

namespace static_integration{

    class Amclros: public static_base::StaticInterface{
        
        public:
            Feature amclros;
            Amclros(){
                amclros.setId("amclros");
                amclros.setName("AmclRos");
                amclros.setGroup("OR");
                amclros.setIsMandatory(true);

                Configuration(amclros, Early, Static);
            };

            void executeFeature(){
                std::cout << amclros.getName() << "feature run successfully" << std::endl;
            };

    };

};