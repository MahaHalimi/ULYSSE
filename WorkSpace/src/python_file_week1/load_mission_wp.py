
#!/usr/bin/env python
#-*- coding: utf-8 S
import rospy
import rospkg


from mavros_msgs.msg import Waypoint
from mavros_msgs.srv import WaypointPush
from mavros_msgs.srv import WaypointPushRequest
from mavros_msgs.msg import CommandCode
from mavros_msgs.srv import SetMode
import sys

class Load_wp(object):
    def __init__(self):
        self.data = []
        self.waypoints_list = []

    def parse_file(self):
       # file_name=input("Entrer le nom du fichier: ")
        file = open("../sources/txt_mission_planner/ulysse_promenade.txt","r")
        L = file.readlines()
        nb_wp = len (L)

        print ("Nombre de waypoints :", nb_wp-1)
        self.req = WaypointPushRequest()
        for i in range (1,len(L)):
            ligne = L[i].split("\t")
	    print(ligne)
            wp = Waypoint()

            wp.frame = Waypoint.FRAME_GLOBAL
            wp.command = CommandCode.NAV_WAYPOINT #Navigate to Waypoint
            wp.is_current = True
            wp.autocontinue = False
            wp.param1 = float(ligne[4])
            wp.param2 = float(ligne[5])
            wp.param3 = float(ligne[6])
            wp.param4 = float(ligne[7])
            wp.x_lat = float(ligne[8])
            wp.y_long = float(ligne[9])
            wp.z_alt = float(ligne[10])

            self.waypoints_list.append(wp)

        self.req.waypoints = self.waypoints_list
        print(self.req.waypoints)

    def send(self):
        rospy.wait_for_service('/mavros/mission/push')
        try:
            service = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)
            resp = service(waypoints=self.req.waypoints)
        except rospy.ServiceException as e:
            print(self.namespace, 'service call to push waypoints failed')

    def send_mode(self):
       rospy.wait_for_service('/mavros/set_mode')
       try:
           service=rospy.ServiceProxy('/mavros/set_mode', SetMode)
           cust_mode=service(custom_mode='AUTO')
          # print("yes")
       except rospy.ServiceException as e:
              print("error to call a service") 

# Infos about msgs:
#   http://docs.ros.org/melodic/api/mavros_msgs/html/msg/CommandCode.html
#   http://docs.ros.org/api/mavros_msgs/html/msg/Waypoint.html

if __name__ == "__main__":
   # print(sys.argv[1])
    load = Load_wp()
    load.parse_file()
    load.send()
    #load.send_mode()
