#ifndef MOTIVML_ROS__CONFIGURATION_H_
#define MOTIVML_ROS__CONFIGURATION_H_

#include <string>
#include "Feature.h"

enum BindingTimes{Early, Late};
enum BindingModes{Static, Dynamic};

class Configuration: public motivml_feature::Feature{
private:
    BindingTimes time;
    BindingModes mode;

public:
    Configuration(){}
    
    void setTimeBinding(BindingTimes time){
        time = time;
    }

    void setModeBinding(BindingModes mode){
        mode = mode;
    }
};

#endif