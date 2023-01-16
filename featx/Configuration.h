#ifndef MOTIVML_ROS__CONFIGURATION_H_
#define MOTIVML_ROS__CONFIGURATION_H_

#include <string>
#include "Feature.h"

enum BindingTimes{Early, Late};
enum BindingModes{Static, Dynamic};

class Configuration{
private:
    std::string id;
    BindingTimes time;
    BindingModes mode;

public:
    Configuration(){}
    Configuration(motivml_feature::Feature modelledFeature, BindingTimes timeSetting, BindingModes modeSetting)
    :id{modelledFeature.getId()}, time{timeSetting}, mode{modeSetting}{}
};

#endif