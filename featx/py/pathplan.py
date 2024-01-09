#!/usr/bin/env python

import rospy
from configuration import Configuration
from feature import Feature
from motivml_ros.msg import ConfigCommand

class PathPlanning():
    def __init__(self) -> None:
        self.pathplan = Feature()
        self.pathplan.setId("pathplan")
        self.pathplan.setName("PathPlanning")
        self.pathplan.setGroup("OR")
        self.pathplan.setIsMandatory(False)
        self.pathplanconf = Configuration(self.pathplan)
        #TODO:Reconfigure to match the model config description
        self.vcomm_subscriber = rospy.Subscriber("/variability_command", ConfigCommand, self.callback_feature, queue_size=10)

    def callback_feature(self, msg:ConfigCommand):
        activeNodeName = str(rospy.get_name())[1:].strip()
        if msg.command == "unload" and msg.bmode == "Static" and str(msg.featureid).strip() == activeNodeName:
            print("-- Static Py Feature " + str(msg.featureid).strip() + " Unloading Blocked")
        elif msg.command == "unload" and msg.bmode == "Dynamic" and str(msg.featureid).strip() == activeNodeName:
            reason = "Dynamic Py Feature unloaded from configuration"
            try:
                rospy.signal_shutdown(reason)
            except:
                print("Node shutdown process failed")
            
def main():
    rospy.init_node("pathplan")
    PathPlanning()
    rospy.spin()

if __name__== "__main__":
    main()