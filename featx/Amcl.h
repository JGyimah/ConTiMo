#include <iostream>
#include "../include/motivml_ros/static_base.h"

namespace static_integration{

    class Amcl: public static_base::StaticInterface{
        std::string feature_id = "amcl";
        public:
            Amcl(){};

            void executeFeature(){
                std::cout << "Hello Amcl!!" << std::endl;
            };

    };

};