1. Mac system install UTM \
   https://mac.getutm.app/

2. Download linux system Ubuntu 22.04 ARM64 \
    https://mac.getutm.app/gallery/
3. Open UTM and load <Ubuntu 22.04.utm> or double click <Ubuntu 22.04.utm>
4. install linux system
5. login linux system. user: ubuntu, password: ubuntu.
6. update linux \
    sudo apt update \
    sudo apt install -y git wget curl \
    sudo apt install ntpdate \
    sudo ntpdate ntp.ubuntu.com \
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o ros.gpg \
    sudo cp ros.gpg /etc/apt/trusted.gpg.d \
    sudo rm ros.gpg \
    sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros2.list' \
    sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros2.list' \
    sudo apt update \
    sudo apt list --upgradable \
    sudo apt upgrade 
7. install ROS 2  \
    sudo apt install -y ros-humble-desktop python3-rosdep python3-argcomplete python3-colcon-common-extensions \
    sudo apt install python3-colcon-mixin \
    sudo apt install python3-vcstool \
    sudo apt install ros-humble-joint-state-publisher \
    sudo apt install ros-humble-joint-state-publisher-gui 
8. init rosdep \
    sudo rosdep init \
    rosdep update \
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc \
    source ~/.bashrc 
9. test \
   ros2 run rviz2 rviz2 \
   mkdir -p ros2_ws/src \
   cd ros2_ws/src \
   git clone https://github.com/olmerg/lesson_urdf.git \
   cd .. \
   colcon build \
   colcon build --packages-select lesson_urdf --allow-overriding lesson_urdf \
   source install/setup.bash \
   ros2 launch lesson_urdf view_robot_launch.py 

10. transform URDF to ROS2 \
    git clone https://github.com/yangzk161228/mac-utm-ros2-urdf-to-ros2.git \
    cp mac-utm-ros2-urdf-to-ros2/create_ros2_urdf.py ./ \
    python3 create_ros2_urdf.py


# mac-utm-ros2-urdf-to-ros2
