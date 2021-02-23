# Velodyne : indications to launch the velodyne (Personal computer and NUC)

-- Git clone the repository on a Workspace 

    $ mkdir ws_velodyne/src
    $ cd ws_velodyne && catkin_make
    $ cd src 
    $ git clone https://github.com/ros-drivers/velodyne.git
    $ cd ws_velodyne && catkin_make 

-- Setting up your computer to communicate with the Velodyne sensor :

    1.Power the LIDAR via the included adapter
    2.Connect the LIDAR to an Ethernet port on your computer.
    3.For now, disable the WiFi connection on your computer.

-- Configure your computer’s IP address through the Gnome interface :

    1.Access the Gnome Menu (Super key), type "Networks Connections" then run it. Select the connection's name and click on "edit". Choose the IPV4 Settings tab and change the “Method” field to "Manual".

    2.Click on "add" and set the IP address field to 192.168.1.100 (“100” can be any number except in a range between 1 and 254, except 201).

    3.Set the “Netmask” to 255.255.255 and the "Gateway" to 0.0.0.0.
  
    4.To finish it click on "save". 

-- Connecting your computer to LIDAR through terminal

Power the LIDAR via the included adapter Connect the LIDAR to an Ethernet port on your computer. Statically assign an IP to this port in the 10.0.1.X range.

sudo ifconfig eth0  10.0.1.X


-- Checking the configurations :

 verfication of the adress IP on your web browser #our IP adress 10.0.1.85

--------------------------------------------------------------------------------------

-- Installing ROS dependencies :

    $ sudo apt-get install ros-VERSION-velodyne (we have melodic version) #remplace VERSION with the version want it

--------------------------------------------------------------------------------------

-- Installing the VLP16 driver :

1.On a "WorkSpace" clone the Velodyne repisitory 

    $ cd ~/"WorkSpace"/src
    $ git clone https://github.com/ros-drivers/velodyne.git

2.After that, on terminal, inside your workspace, update all dependecies:

    $ rosdep install --from-paths src --ignore-src --rosdistro YOURDISTRO -y 

3.Then build your "WorkSpace":

    $ cd ~/"WorkSpace"
    $ catkin_make

--------------------------------------------------------------------------------------

-- Viewing the Data : 

on your terminal run the following command :

    $ roslaunch velodyne_pointcloud VLP16_points.launch

You can check the necessary nodes with 

    $ rosnode list

You'll be able to see the messages being published and subscribed to the following topic: 

    $ rostopic echo /velodyne_points

Launch rviz, with the "velodyne" as a fixed frame: 

    $ rosrun rviz rviz -f velodyne

* On the "displays", click "Add", and select "Point Cloud2", and press "OK"
* In the "Topic" field of the new "Point Cloud2" tab, enter "/velodyne_points".
    

-- Avoiding obstacles : 

A script for avoiding obstacles its wortten on C++, you can launch it with 

    $ rosrun script lidar

-- If you want send your folder to UYLYSSE:

for sending the folder to ULYSSE you have to tape

    $ scp /Path/"NAME_OF_FOLDER"/ user@10.0.1.111:/home/"path_desired/" #where 10.0.1.111 it's the NUC's adress IP and our NAME_OF_FOLDER = VELODYNE

On ULYSSE's nuc :
    
    $ cd VELODYNE    
   
Delete devel and build folders and tape :
    
    $ catkin_make
 

    
    
    
