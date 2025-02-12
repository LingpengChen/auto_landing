# This program compare the movement of the physical wave and the visual wave by 
# referring to wavegauge3 and the static stick beside it
import rospy
import sys
import select
import termios
import tty
import rospy

import cv2
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.ticker as ticker

from gazebo_msgs.msg import LinkStates
from sensor_msgs.msg import Image
from std_msgs.msg import Int32

import numpy as np
import sys
import rospy

import matplotlib.pyplot as plt  

t = []
phy = []
vis = []

# wavegauge1::wavegauge::base_link

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class Comparator():
    def __init__(self):
        rospy.init_node('wave_comparator', anonymous=True)
        rospy.Subscriber("/gazebo/link_states", LinkStates, self.physical_wave_callback)
        rospy.Subscriber("/stick_length",
                            Int32, self.visual_wave_callback)
        self.visual_wave = 0
        self.physical_wave = 0
    
    def physical_wave_callback(self, msg):
        self.gazebo_link_states = msg
        index = self.gazebo_link_states.name.index(
            'wavegauge100::wavegauge::base_link')
        self.physical_wave = self.gazebo_link_states.pose[index].position.z
    
    def visual_wave_callback(self, msg):
        visual_wave_pix = int(msg.data)
        self.visual_wave = (220-visual_wave_pix)/75.0

    def main_loop(self):
        i = 0
        # r = rospy.Rate(15)

        while(True):
            sim_time = rospy.Time.now().to_sec()
            self.key = getKey()
            i += 1
            t.append(sim_time)
            phy.append(self.physical_wave)
            vis.append(self.visual_wave)
            print("physical_wave = ", self.physical_wave, " visual_wave = ", self.visual_wave)
            if (self.key == '\x03' or i > 500):
                break
            rospy.sleep(0.01)

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)
    # input = input("Do you want to record video or capture image? (0 for video and 1 for picture)")

    controller = Comparator()
    controller.main_loop()

    plt.plot(t, phy, label='physical_wave')
    plt.plot(t, vis, label='visual_wave')
    plt.legend()
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    plt.show()

    # ax = plt.axes(projection ="3d")  
    # # Add x, and y gridlines for the figure  
    # ax.grid(b = True, color ='blue',linestyle ='-.', linewidth = 0.5,alpha = 0.3)  
    # # Creating the color map for the plot  
    # # Creating the 3D plot  
    # sctt = ax.scatter3D(X, Y, Z) 


    # plt.title("3D scatter plot")  
    #     # display the  plot  
    # plt.show()  
    
    

