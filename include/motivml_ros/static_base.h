#ifndef MOTIVML_ROS__STATIC_BASE_H_
#define MOTIVML_ROS__STATIC_BASE_H_

#include "../../featx/Feature.h"

namespace static_base{

    class StaticInterface: public motivml_feature::Feature{
        public:
            virtual void executeFeature() = 0;
            virtual ~StaticInterface(){};

        protected:
            StaticInterface(){};
    };

};
#endif