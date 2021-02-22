#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"
#include "std_msgs/Float32.h"
#include "std_msgs/Bool.h"
#include "sensor_msgs/PointCloud.h"
#include "sensor_msgs/point_cloud_conversion.h"
#include "std_msgs/Float64.h"
#include <limits>
#include <math.h>
#include <vector>
#include <stdio.h>
#include <iostream>
#include <stdlib.h>

void DataLidar(const sensor_msgs::PointCloud2& msg)
{
	sensor_msgs::PointCloud out_cloud;
	sensor_msgs::convertPointCloud2ToPointCloud(msg, out_cloud);

	std::vector<float> x_vect;
	std::vector<float> y_vect;
	std::vector<float> z_vect;

	float angle_max =  100.; //+70 à re-definir
	float angle_min =  80.;  //+110 à re-definir
    float eps = 3;
	bool avoid = false;


	for(int i = 0 ; i < out_cloud.points.size(); ++i)
	{
		float x = out_cloud.points[i].x;
	    float y = out_cloud.points[i].y;
	    float z = out_cloud.points[i].z;
	    float dist = 10.; // = std::sqrt(x*x+y*y);
	    float angle = (atan2(y,x)*180./M_PI);

        if(angle > angle_min and angle < angle_max)
		{		    
		  	ROS_INFO("ANGLES DISIRED");
		    x_vect.push_back(x);
		    y_vect.push_back(y);
		    //z_vect.push_back(z);

		    if ( x < dist ) // dist. it's not exact, just for test
		    //if ( x < dist && (x_vect.size()> 20 || z_vect.size()> 20)) // 20. it's not exact, just for test
				{ 
					avoid = true;
					ROS_INFO("ATTENTION UN OBSTACLE"); 
					//send a yaw or some waypoints
				    // read a file
				    // where first waypoint x = abs(x-eps) and y = y
				}
		}

		else
		{
			ROS_INFO("NOT INTERSTING FOR U");
		}
	}
}


int main(int argc, char **argv)
{

	ros::init(argc, argv, "Lidar_node");

	ros::NodeHandle n;
	ros::Subscriber sub_cloud = n.subscribe("/velodyne_points", 1000, DataLidar);
	ros::Rate loop_rate(10);
	ros::spin();

	return 0;
}








