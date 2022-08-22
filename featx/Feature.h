#ifndef MOTIVML_ROS__FEATURE_H_
#define MOTIVML_ROS__FEATURE_H_

#include <string>
#include <vector>
#include "Configuration.h"

class Feature{
    std::string id;
    std::string name;

    struct contraints{
        std::vector<std::string> featuresIncluded;
        std::vector<std::string> featuresExcluded;
        std::string bindingTimeAllowed;
        std::string bindingModeAllowed;
    };

    std::string group;
    bool isMandatory;

    Configuration configuration;
};

#endif