from __future__ import print_function
import os
# COM-Server
import win32com.client as com
import numpy as np
#很重要，用Python3.7 Basic COM Command的环境
## Connecting the COM Server => Open a new Vissim Window:
Vissim = com.gencache.EnsureDispatch("Vissim.Vissim") #
# Vissim = com.Dispatch("Vissim.Vissim") # once the cache has been generated, its faster to call Dispatch which also creates the connection to Vissim.
# If you have installed multiple Vissim Versions, you can open a specific Vissim version adding the version number
# Vissim = com.gencache.EnsureDispatch("Vissim.Vissim.10") # Vissim 10
#Vissim = com.gencache.EnsureDispatch("Vissim.Vissim.11") # Vissim 11
### for advanced users, with this command you can get all Constants from PTV Vissim with this command (not required for the example)
##import sys
##Constants = sys.modules[sys.modules[Vissim.__module__].__package__].constants

#Path_of_COM_Basic_Commands_network = os.getcwd() #'C:\\Users\\Public\\Documents\\PTV Vision\\PTV Vissim 11\\Examples Training\\COM\\Basic Commands\\'
#Path_of_COM_Basic_Commands_network = os.getcwd('D:\\ZHOUSHENGHUA\\VISSIM\\')
def Set_Vehicle_Route_Decision (SVRD,SVR,new_relativ_flow,TimeInterval='RelFlow(2)', ): #修改单个方向的车辆比例
    # Set relative flow of a static vehicle route of a static vehicle routing decision:
    #SVRD_number = 1  # SVRD = Static Vehicle Routing Decision
    #SVR_number = 1  # SVR = Static Vehicle Route (of a specific Static Vehicle Routing Decision)
    #new_relativ_flow = 0.6
    Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(SVRD).VehRoutSta.ItemByKey(SVR).SetAttValue(TimeInterval, new_relativ_flow)
    # 'RelFlow(1)' means the first defined time interval; to access the third defined time interval: 'RelFlow(3)'
    return None
#Set_Vehicel_composition里面多了一个设置类别，可以先用Set_Vehicel_composition函数，再用Set_Vehicle_Desired_Speed
def Set_Vehicel_Composition (Veh_composition_number, percentage_of_Car, percentage_of_HGV):
    Rel_Flows = Vissim.Net.VehicleCompositions.ItemByKey(Veh_composition_number).VehCompRelFlows.GetAll()
    Rel_Flows[0].SetAttValue('VehType', 100)  # Changing the vehicle type
    Rel_Flows[1].SetAttValue('VehType', 200)  # Changing the vehicle type
    #Rel_Flows[2].SetAttValue('VehType', 300)  # Changing the vehicle type
    Rel_Flows[0].SetAttValue('RelFlow', percentage_of_Car) # Changing the relative flow
    Rel_Flows[1].SetAttValue('RelFlow', percentage_of_HGV) # Changing the relative flow of the 2nd Relative Flow.
    #Rel_Flows[2].SetAttValue('RelFlow', percentage_of_Bus) # Changing the relative flow of the 2nd Relative Flow.
    return None
def Set_Vehicle_Speed (ItemKey,Bottom,Up):
    p=Vissim.Net.DesSpeedDistributions.ItemByKey(ItemKey).SpeedDistrDatPts.GetAll() #1052
    p[0].SetAttValue('X', Bottom)
    p[1].SetAttValue('X', Up)
    return None
def redistribute(a,b,c,j):
    p=[]
    if c==0:
        b=a+b
        a=0
        p.append(a)
        p.append(b)
    if c!=0:
        s = a + b + c
        if 1==j:
            b = b / (b + c) * s
            c = s - b
            a = 0
        if 2==j:
            a=a / (a + c) * s
            c=s-a
            b=0
        if 3==j:
            a=a / (a + c) * s
            b=s-a
            c=0
        p.append(a)
        p.append(b)
        p.append(c)

    return p
def adjust_traffic_flow(affectdroad):
    for i in range (1,158): # 158 change 158 as a parameter
        if i!=None:
            a=[0,0,0,0] # python的数组索引0开始，VISSIM API是1开始，所以三个destination link的依然要四个位置
            Number_of_Dest_Links=len(Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.GetAll())
            print(Number_of_Dest_Links)
            for j in range (1,Number_of_Dest_Links+1):
                a[j]=Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.ItemByKey(j).AttValue('DestLink')
                print(Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.ItemByKey(j).AttValue('DestLink'))
                print(int(a[j])==affectdroad)
                if int(a[j])==affectdroad:
                    if  Number_of_Dest_Links==2:
                        Newly_allocated_traffic = float(
                            Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.ItemByKey(1).AttValue(
                                'RelFlow(1)')) + float(
                            Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.ItemByKey(2).AttValue(
                                'RelFlow(1)'))
                        if j==1:
                            Set_Vehicle_Route_Decision(i, 1, 0, 'RelFlow(1)')
                            Set_Vehicle_Route_Decision(i, 2, Newly_allocated_traffic, 'RelFlow(1)')
                        else:
                            Set_Vehicle_Route_Decision(i, 1, Newly_allocated_traffic, 'RelFlow(1)')
                            Set_Vehicle_Route_Decision(i, 2, 0, 'RelFlow(1)')
                    if Number_of_Dest_Links == 3:
                        Flow=[0,0,0]
                        Flow[0]=float(Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.ItemByKey(1).AttValue(
                                'RelFlow(1)'))
                        Flow[1]=float(Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.ItemByKey(2).AttValue(
                                'RelFlow(1)'))
                        Flow[2]=float(Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.ItemByKey(3).AttValue(
                                'RelFlow(1)'))
                        sum=Flow[0]+Flow[1]+Flow[2]
                        print(sum)
                        print(j)
                        print(redistribute(Flow[0], Flow[1], Flow[2], j))
                        Newly_allocated_traffic=redistribute(Flow[0], Flow[1], Flow[2], j)
                        Set_Vehicle_Route_Decision(i, 1, Newly_allocated_traffic[0], 'RelFlow(1)')
                        Set_Vehicle_Route_Decision(i, 2, Newly_allocated_traffic[1], 'RelFlow(1)')
                        Set_Vehicle_Route_Decision(i, 3, Newly_allocated_traffic[2], 'RelFlow(1)')
Filename = os.path.join('D:\\ZHOUSHENGHUA\\VISSIM\\', 'lexingtonforTestingtheOptimizationofSignals.inpx')
Vissim.LoadNet(Filename)
turning =np.loadtxt('D:\\ZHOUSHENGHUA\\VISSIM\\Interoperability\\turning.txt', delimiter=',')#导入转向数据，一共八个路口
composition=np.loadtxt('D:\\ZHOUSHENGHUA\\VISSIM\\Interoperability\\composition.txt', delimiter=',') #导入车流比例数据，一共六个输入比例
vehicle_input_in_lane =np.loadtxt('D:\\ZHOUSHENGHUA\\VISSIM\\Interoperability\\vehicle_input.txt', delimiter=',')
vehicle_speed=np.loadtxt('D:\\ZHOUSHENGHUA\\VISSIM\\Interoperability\\vehicle_speed.txt', delimiter=',')
#affectdroad=76 # change affected road







#print(Vissim.Net.ReducedSpeedAreas.ItemByKey(3).VehClassSpeedRed)


#AttValue('DesSpeedDistr'))
# DesiredSpeed=[1047,1048,1049,1050,1051,1052]
#
# for i in range (1,9):
#     Set_Vehicle_Route_Decision(i,1,turning[i-1][0],'RelFlow(1)')
#     Set_Vehicle_Route_Decision(i,2,turning[i-1][1],'RelFlow(1)')
#     Set_Vehicle_Route_Decision(i,3,turning[i-1][2],'RelFlow(1)')
# DesiredSpeed=[1047,1048,1049,1050,1051,1052]
# for i in range (1,7):
#     Vissim.Net.VehicleInputs.ItemByKey(i).SetAttValue('Volume(2)', vehicle_input_in_lane[i-1])
#     print(i,vehicle_input_in_lane[i-1])
#     Set_Vehicel_Composition(i, composition[i-1][0], composition[i-1][1])
#     Set_Vehicle_Speed (DesiredSpeed [i-1],vehicle_speed[i-1][0],vehicle_speed[i-1][1])


# def Set_Vehicle_Route_Decision (ItemKey,Bottom,Up):
#     p=Vissim.Net.DesSpeedDistributions.ItemByKey(ItemKey).SpeedDistrDatPts.GetAll() #1052
#     p[0].SetAttValue('X', Bottom)
#     p[1].SetAttValue('X', Up)
#     return None
#Vissim.Simulation.RunSingleStep()
def Add_Reduced_Speed_Area(UnsignedKey, ItemByKeyOfLink,ItemByKeyOflane, Location, Length=30, TimeFrom=0, TimeTo=99999,DesSpeedDistr1='20',DesSpeedDistr2='20',DesSpeedDistr3='20'):
    # Vissim.Net.ReducedSpeedAreas.AddReducedSpeedArea(6, Vissim.Net.Links.ItemByKey(31).Lanes.ItemByKey(1), 10) #例子
    # Vissim.Net.ReducedSpeedAreas.ItemByKey(6).SetAttValue('Length', 100)
    # Vissim.Net.ReducedSpeedAreas.ItemByKey(6).SetAttValue('TimeFrom', 100)
    # Vissim.Net.ReducedSpeedAreas.ItemByKey(6).SetAttValue('TimeTo', 300)
    # Vissim.Net.ReducedSpeedAreas.ItemByKey(6).SetAttValue('DesSpeedDistr(10)', 20)
    # Vissim.Net.ReducedSpeedAreas.ItemByKey(6).SetAttValue('DesSpeedDistr(20)', 20)
    # Vissim.Net.ReducedSpeedAreas.ItemByKey(6).SetAttValue('DesSpeedDistr(30)', 20)
    Vissim.Net.ReducedSpeedAreas.AddReducedSpeedArea(UnsignedKey, Vissim.Net.Links.ItemByKey(ItemByKeyOfLink).Lanes.ItemByKey(ItemByKeyOflane), Location)
    Vissim.Net.ReducedSpeedAreas.ItemByKey(UnsignedKey).SetAttValue('Length', Length)
    Vissim.Net.ReducedSpeedAreas.ItemByKey(UnsignedKey).SetAttValue('TimeFrom', TimeFrom)
    Vissim.Net.ReducedSpeedAreas.ItemByKey(UnsignedKey).SetAttValue('TimeTo', TimeTo)
    Vissim.Net.ReducedSpeedAreas.ItemByKey(UnsignedKey).SetAttValue('DesSpeedDistr(10)', DesSpeedDistr1)
    Vissim.Net.ReducedSpeedAreas.ItemByKey(UnsignedKey).SetAttValue('DesSpeedDistr(20)', DesSpeedDistr2)
    Vissim.Net.ReducedSpeedAreas.ItemByKey(UnsignedKey).SetAttValue('DesSpeedDistr(30)', DesSpeedDistr3)
    return None
#Add_Reduced_Speed_Area(1, 76, 1, 10,50)
#adjust_traffic_flow(76)
#Vissim.Simulation.RunContinuous()
Vissim.Net.SignalControllers.OptimizeAll()



# def Set_Vehicle_Route_Decision (SVRD,SVR,new_relativ_flow,TimeInterval='RelFlow(2)', ): #修改单个方向的车辆比例
#     # Set relative flow of a static vehicle route of a static vehicle routing decision:
#     #SVRD_number = 1  # SVRD = Static Vehicle Routing Decision
#     #SVR_number = 1  # SVR = Static Vehicle Route (of a specific Static Vehicle Routing Decision)
#     #new_relativ_flow = 0.6
#     Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(SVRD).VehRoutSta.ItemByKey(SVR).SetAttValue(TimeInterval, new_relativ_flow)
#     # 'RelFlow(1)' means the first defined time interval; to access the third defined time interval: 'RelFlow(3)'
#     return None
#
# #Set_Vehicel_composition里面多了一个设置类别，可以先用Set_Vehicel_composition函数，再用Set_Vehicle_Desired_Speed
# def Set_Vehicel_Composition (Veh_composition_number, percentage_of_Car, percentage_of_HGV):
#     Rel_Flows = Vissim.Net.VehicleCompositions.ItemByKey(Veh_composition_number).VehCompRelFlows.GetAll()
#     Rel_Flows[0].SetAttValue('VehType', 100)  # Changing the vehicle type
#     Rel_Flows[1].SetAttValue('VehType', 200)  # Changing the vehicle type
#     #Rel_Flows[2].SetAttValue('VehType', 300)  # Changing the vehicle type
#     Rel_Flows[0].SetAttValue('RelFlow', percentage_of_Car) # Changing the relative flow
#     Rel_Flows[1].SetAttValue('RelFlow', percentage_of_HGV) # Changing the relative flow of the 2nd Relative Flow.
#     #Rel_Flows[2].SetAttValue('RelFlow', percentage_of_Bus) # Changing the relative flow of the 2nd Relative Flow.
#     return None

# for i in range (1,9):
#     for j in range (1,3):
#         print(Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(i).VehRoutSta.ItemByKey(j).AttValue('DeatLink'))
#
# DesiredSpeed=[1047,1048,1049,1050,1051,1052]

# Reduced Speed Area
#--------------------------------------
#Vissim.Net.ReducedSpeedAreas.AddReducedSpeedArea(10, 3-1, 10) # unsigned int Key, ILane* Lane, double Pos