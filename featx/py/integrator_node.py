#!/usr/bin/env python
import rospy
from motivml_ros.msg import ConfigCommand
import os

def callback_integrator(msg:ConfigCommand):
    if msg.command == "load" and msg.bmode == "Static":
        print("-- Static Py Feature " + str(msg.featureid).strip() + " Already Loaded In Start-up")
    elif msg.command == "load" and msg.bmode == "Dynamic":
        try:
            nodeToBeStarted = str(msg.featureid).strip()
            start_node(nodeToBeStarted)
        except rospy.ROSInterruptException:
            print("There was a problem starting the "+nodeToBeStarted+ " python node")

def start_node(nodename:str):
    rospy.loginfo("Starting "+nodename+" ...")
    package = "motivml_ros"
    executable = nodename + ".py"
    if os.path.isfile(executable):
        os.system("rosrun "+package+" "+executable)
    else:
        rospy.loginfo("-- No feature class of type Py found")

def main():
    rospy.init_node("py_integrator")
    rospy.Subscriber("/variability_command", ConfigCommand, callback_integrator, queue_size=10)
    rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except:
        print("Py Integrator Node Encountered a Problem in its Initialisation")