#ifndef MOTIVML_ROS__CONFIGURATION_H_
#define MOTIVML_ROS__CONFIGURATION_H_

#include <string>
#include "Feature.h"

class Configuration: public Feature{

    std::string time;
    std::string mode;

};

#endif