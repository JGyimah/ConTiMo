#include <iostream>

#define AMCL_STATIC_EARLY 1

class Amcl{
    std::string feature_id = "amcl";
    public:
        Amcl(){};

        void executeFeature(){
            std::cout << "Amcl [static] feature run successfully" << std::endl;
        };

};