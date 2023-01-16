#include <iostream>
#include "../include/motivml_ros/static_base.h"
#include "Configuration.h"

namespace static_integration{

    class Amcl: public static_base::StaticInterface{
        
        public:
            Feature amcl;
            Amcl(){
                amcl.setId("amcl");
                amcl.setName("AMCL");
                amcl.setGroup("XOR");
                amcl.setIsMandatory(false);

                Configuration(amcl, Early, Static);
            }

            void executeFeature(){
                std::cout << amcl.getName() << "feature run successfully" << std::endl;
            };

    };

};