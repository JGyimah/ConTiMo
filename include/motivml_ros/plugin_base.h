#ifndef MOTIVML_ROS__PLUGIN_BASE_H_
#define MOTIVML_ROS__PLUGIN_BASE_H_

#include "../../featx/Feature.h"

namespace plugin_base{

    class PluginInterface: public motivml_feature::Feature{
        public:
            virtual void executeFeature() = 0;
            virtual ~PluginInterface(){};

        protected:
            PluginInterface(){};
    };

};
#endif