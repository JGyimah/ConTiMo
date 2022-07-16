#include <iostream>
#include "../include/motivml_ros/static_base.h"

namespace static_integration{

    class MotionPlanningControl: public static_base::StaticInterface{
        std::string feature_id = "motplannctrl";
        public:
            MotionPlanningControl(){};

            void executeFeature(){
                std::cout << "Hello Motion Planning!!" << std::endl;
            };

    };

};