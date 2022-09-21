#ifndef MOTIVML_ROS__PLUGIN_BASE_H_
#define MOTIVML_ROS__PLUGIN_BASE_H_

#include "../../featx/Configuration.h"

namespace plugin_base{

    class PluginInterface: public Configuration{
        public:
            virtual void executeFeature() = 0;
            virtual ~PluginInterface(){};

        protected:
            PluginInterface();
    };

};
#endif