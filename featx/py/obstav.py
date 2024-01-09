#!/usr/bin/env python

import rospy
from configuration import Configuration
from feature import Feature
from motivml_ros.msg import ConfigCommand

class ObstacleAvoidance():
    def __init__(self) -> None:
        obsatav = Feature()
        obsatav.setId("obstav")
        obsatav.setName("ObstacleAvoidance")
        obsatav.setGroup("OR")
        obsatav.setIsMandatory(False)
        obsatavconf = Configuration(obsatav)
        #TODO:Reconfigure to match the model config description
        self.vcomm_subscriber = rospy.Subscriber("/variability_command", ConfigCommand, self.callback_feature)
        rospy.loginfo("obstav started")

    def callback_feature(self, msg:ConfigCommand):
        activeNodeName = str(rospy.get_name())[1:].strip()
        if msg.command == "unload" and msg.bmode == "Static" and str(msg.featureid).strip() == activeNodeName:
            print("-- Static Py Feature " + str(msg.featureid).strip() + " Unloading Blocked")
        elif msg.command == "unload" and msg.bmode == "Dynamic" and str(msg.featureid).strip() == activeNodeName:
            reason = "Dynamic Py Feature unloaded from configuration"
            try:
                rospy.loginfo("obstav shutdown")
                rospy.signal_shutdown(reason)
            except:
                print("Node shutdown process failed")


if __name__== "__main__":
    rospy.init_node("obstav")
    ObstacleAvoidance()
    rospy.spin()