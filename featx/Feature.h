#ifndef MOTIVML_ROS__FEATURE_H_
#define MOTIVML_ROS__FEATURE_H_

#include <string>
#include <vector>

enum BindingTimeAllowed{Early, Late, Any};
enum BindingModeAllowed{Static, Dynamic, Any};

class Feature{
    std::string id;
    std::string name;

    struct contraints{
        std::vector<std::string> featuresIncluded;
        std::vector<std::string> featuresExcluded;
        BindingTimeAllowed bindingTimeAllowed{Early};
        BindingModeAllowed bindingModeAllowed{Static};
    };

    std::string group;
    bool isMandatory;
};

#endif