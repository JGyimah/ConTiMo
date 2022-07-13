#!/usr/bin/env python

import sys
from motivml.motivml import Dsl

if __name__=='__main__':
    
    if(len(sys.argv) >= 2):
        dsl = Dsl()
        ProjectName = sys.argv[1]
        dsl.dslLaunch(ProjectName)