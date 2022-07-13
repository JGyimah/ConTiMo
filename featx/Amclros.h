#include <iostream>

#define AMCLROS_STATIC_EARLY 0
    
class Amclros{
        std::string feature_id = "amclros";
        public:
            Amclros(){};

            void executeFeature(){
                std::cout << "Amclros [static] feature run successfully" << std::endl;
            };
};