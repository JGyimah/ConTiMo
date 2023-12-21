#ifndef MOTIVML_ROS__FEATURE_H_
#define MOTIVML_ROS__FEATURE_H_

#include <string>
#include <vector>

namespace motivml_feature{

    enum class BindingTimeAllowed{Early, Late, Any};
    enum class BindingModeAllowed{Static, Dynamic, Any};

    class Feature{
    private:
        std::string id;
        std::string name;

        std::vector<std::string> featuresIncluded;
        std::vector<std::string> featuresExcluded;
        BindingTimeAllowed bindingTimeAllowed = BindingTimeAllowed::Early;
        BindingModeAllowed bindingModeAllowed = BindingModeAllowed::Static;

        //TODO: Add group and configuration composition eg Configuration config, Group group
        //dont forget to use namespace of config
        std::string group;
        bool isMandatory;

    public:
        Feature(){};

        //setters
        void setId(std::string id){
            id = id;
        }

        void setName(std::string name){
            name = name;
        }

        void setBindingTimeAllowed(BindingTimeAllowed bindingTimeAllowed){
            bindingTimeAllowed = bindingTimeAllowed;
        }

        void setBindingModeAllowed(BindingModeAllowed bindingModeAllowed){
            bindingModeAllowed = bindingModeAllowed;
        }

        void setGroup(std::string group){
            group = group;
        }

        void setIsMandatory(bool isMandatoory){
            isMandatoory = isMandatoory;
        }

        void setFeaturesIncluded(std::vector<std::string>& inclusions){
            for(std::string &included : inclusions){
                featuresIncluded.push_back(included);
            }
        }

        void setFeaturesExcluded(std::vector<std::string>& exclusions){
            for(std::string &excluded : exclusions){
                featuresExcluded.push_back(excluded);
            }
        }

        //getters
        std::string getName() const{
            return name;
        }

        std::string getId() const{
            return id;
        }
    };
};

#endif