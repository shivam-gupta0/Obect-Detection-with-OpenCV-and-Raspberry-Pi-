#  Object Detection,OpenCV, and Raspberry Pi for Traffic Light Control System

This project aims to develop a smart traffic light control system using computer vision and Arduino. The system detects the presence of cars and switches the traffic light phase accordingly. <br />
# Usage
Connect the Raspberry Pi and Arduino board. <br />
Install the required libraries: OpenCV, NumPy, and PySerial.<br />
Connect the Pi Camera module to the Raspberry Pi.<br />
Run the traffic_light.py file using the following command:<br />
<br />
**python3 traffic_light.py** <br />
<br />
The system will detect the presence of cars and switch the traffic light phase accordingly.
# Requirements Hardware and Software
- Raspberry Pi 4 Model B  <br />
- Raspberry Pi High-Quality Camera <br />
- Micro SD Card <br />
- Power Supply <br />
- Monitor <br />
- HDMI Cord <br />
- VNC viewer <br />
- OpenCV

# INSTALL OpenCV in Raspberry Pi.
sudo apt update <br />
sudo apt upgrade <br />
sudo apt install cmake build-essential pkg-config git <br />
sudo apt install libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev <br />
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev <br />
sudo apt install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 <br />
sudo apt install libatlas-base-dev liblapacke-dev gfortran <br />
sudo apt install libhdf5-dev libhdf5-103 <br />
sudo apt install python3-dev python3-pip python3-numpy <br />
sudo apt install python3-opencv <br />
apt show python3-opencv <br />

# Code Overview
The TrafficLight class is defined to implement the smart traffic light control system. The class has the following methods: <br />

__init__(self): Initializes the PiCamera and sets its resolution and framerate.<br />
detect_cars(self, frame): Detects the presence of cars in the frame using computer vision.<br />
switch_phase(self, phase): Switches the traffic light phase based on the detected cars and the current traffic light phase.<br />
run(self): Runs the traffic light control system.<br />
The main program creates an instance of the TrafficLight class and runs the traffic light control system by calling the run() method. The system continuously captures frames from the PiCamera, detects the presence of cars using the detect_cars() method, and switches the traffic light phase using the switch_phase() method.<br />

![toy_detection](https://user-images.githubusercontent.com/85798077/177434860-8b693e29-af2e-4856-b60b-a2d168864f3a.jpg)
