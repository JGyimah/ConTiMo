#include <iostream>
#include "../include/motivml_ros/static_base.h"

namespace static_integration{

    class ComponentControl: public static_base::StaticInterface{
        std::string feature_id = "compcontrol";
        public:
            ComponentControl(){};

            void executeFeature(){
                std::cout << "Hello Component Control!!" << std::endl;
            };

    };

};