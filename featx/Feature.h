#include <string>
#include <vector>

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
};