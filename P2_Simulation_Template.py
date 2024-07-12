ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import random #Import random library

def spawn_container(id):
    #Spawns the containers
    arm.spawn_cage(id)

def pick_up():
#Function for picking up the spawned container
    #Move to spawn Location
    arm.move_arm(0.6, 0.06, 0.05)
    time.sleep(2)
    arm.control_gripper(35)
    #Closes the gripper
    time.sleep(2)
    #Move to home position
    arm.move_arm(0.406, 0.0, 0.48)
    time.sleep(2)
        
def rotate_base(id): #Function for correctly rotating the Q-arm
    #Assign variable that reads right potentiometer
    initial = potentiometer.right() 
    loop = True
    #List of ID's of small containers
    small_ids = [1,2,3]
    #List of ID's of large containers
    big_ids = [4,5,6]
    #Checks to see if the potentiometer.right has changed and if the position is correct
    while loop:
        final = potentiometer.right()
         #Rotates the base by the change in potentiometer
        if initial != final:
            #Assign a variable that gives degrees by taking difference between final and initial potentiometer reading
            #The base can rotate +-175 degrees, change in potentiometer *350 gives the angle
            delta_degree = (final - initial) * 350
            #Rotate arm by delta_degree
            arm.rotate_base(delta_degree)
            initial = final
        #Cancels the loop if condition is met
        if potentiometer.left() == 0.6 and id in small_ids:
            if id == 1:
                if potentiometer.right() == 1.0:
                    loop = False
            elif id == 2:
                if potentiometer.right() == 0.25:
                    loop = False
            elif id == 3:
                if potentiometer.right() == 0.75:
                    loop = False
        #Cancels the loop if condition is met
        if potentiometer.left() == 1.0 and id in big_ids:
            if id == 4:
                if potentiometer.right() == 1.0:
                    loop = False
            elif id == 5:
                if potentiometer.right() == 0.25:
                    loop = False
            elif id == 6:
                if potentiometer.right() == 0.75:
                    loop = False
    drop_off(id)
				
def drop_off(id):
    #List of colours to open correct autoclave
    colours = ['red', 'green', 'blue']
    #Activate autoclaves
    arm.activate_autoclaves()
    #Drop off small red container
    if id == 1:
        arm.move_arm(-0.65,0.25,0.3)
        time.sleep(2)
        #Opens the gripper
        arm.control_gripper(-35)
        time.sleep(2)
    #Drop off small green container
    elif id == 2:
        arm.move_arm(0.0,-0.65,0.3)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
    #Drop off small blue container
    elif id == 3:
        arm.move_arm(0.0,0.65,0.3)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
    #Drop off large red container    
    elif id == 4:
        #Open autoclave for red large container
        arm.open_autoclave(colours[id-4])
        arm.move_arm(-0.45,0.15,0.2)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
        #Closes the autoclave for red large container
        arm.open_autoclave(colours[id-4], False)
    #Drop off large green container
    elif id == 5:
        #Open autoclave for large green container
        arm.open_autoclave(colours[id-4])
        arm.move_arm(0.0,-0.45,0.2)
        time.sleep(2)
        #Opens the gripper
        arm.control_gripper(-35)
        time.sleep(2)
         #Closes the autoclave for green large container
        arm.open_autoclave(colours[id-4], False)
    #Drop off large blue container
    elif id == 6:
        #Open autoclave for large blue container
        arm.open_autoclave(colours[id-4])
        arm.move_arm(0.0,0.45,0.2)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
        #Closes the autoclave for blue large container
        arm.open_autoclave(colours[id-4], False)
    #Deactivates the autoclaves
    arm.deactivate_autoclaves()
def return_home():
    #Returns home position
    arm.home()

  
def main():
    id_list = [1,2,3,4,5,6]
    random.shuffle(id_list)
    #Repeat six times
    for i in range(0,6):
        go = True
        id = id_list[i]
        #Repeat until go variable switches false
        while go:
            #Spawn container when both right and left potentiometer equals 0.5
            if potentiometer.right() == 0.5 and potentiometer.left() == 0.5:
                spawn_container(id)
                go = False
        pick_up()
        rotate_base(id)
        return_home()
    arm.terminate_arm()
main()
    

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

