#include <iostream>
#include "../include/motivml_ros/static_base.h"

namespace static_integration{

    class Amclros: public static_base::StaticInterface{
        std::string feature_id = "amclros";
        public:
            Amclros(){};

            void executeFeature(){
                std::cout << "Hello Amclros!!" << std::endl;
            };

    };

};