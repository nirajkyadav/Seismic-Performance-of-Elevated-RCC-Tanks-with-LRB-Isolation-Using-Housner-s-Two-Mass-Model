# Dimensions and Nodes
# Materials
# Beam column secion
# Beam column elements
# Nodal mass and udl
# Model Bare
# Gravity Analysis
# Pushover Analysis
# Nonlinear Time History Analysis

import openseespy.opensees as ops
import numpy as np
import matplotlib.pyplot as plt
import opsvis as opsv

ops.wipe()
ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)

# ----------------------------------------------------------------------------------
# Geometry, Dimensions And Units (mm, s, N) , Global axes X, Y, Z (vertical) 
# ----------------------------------------------------------------------------------

inch = 25.4
ft = 12. * inch
rigidDiaphragm = 1

LRB_inclusion = 0           # 1 for LRB, 0 for fixed base

print("# ---------------------------------------------------")
print("# Rigid Diaphragm ON.")
if LRB_inclusion == 1:
    print("# LRB is installed.")
else:
    print("# LRB is NOT installed.")
print("# ---------------------------------------------------")

# --------------------------------------------------------------------------------
# LRB Dimensions
# --------------------------------------------------------------------------------

D1 = 120.             	            # Internal diameter of lead rubber bearing
D2 = 800.               		    # Outer diameter of lead rubber bearing (excluding cover thickness)

ts = 4.0         				    # Thickness of single steel shim plate mm
tr = 8.9       					    # Thicness of a single rubber layer mm
tc = 15.            				# Bearing cover mm

n = 18                				# Number of rubber layers

Tr = n*tr             				# Total rubber thickness
h_LRB = Tr + (n-1)*ts          		# Total height of bearing

# --------------------------------------------------------------------------------
# Nodes # ops.node(nodeTag, x, y, z)
# --------------------------------------------------------------------------------

# LRB nodes ------------------------------------------------------------
if LRB_inclusion == 1:
    ops.node(1001, 3735.0, 0.0, -h_LRB)  
    ops.node(1002, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  -h_LRB)
    ops.node(1003, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), -h_LRB)
    ops.node(1004, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), -h_LRB)
    ops.node(1005, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), -h_LRB)
    ops.node(1006, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), -h_LRB)

    LRB_nodes = [1001, 1002, 1003, 1004, 1005, 1006]

# Floor 1 nodes ------------------------------------------------------------
ops.node(101, 3735.0, 0.0, 0.0)  
ops.node(102, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  0.0)
ops.node(103, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 0.0)
ops.node(104, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 0.0)
ops.node(105, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 0.0)
ops.node(106, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 0.0)

floor_1_nodes = [101, 102, 103, 104, 105, 106]

if LRB_inclusion == 1:
    for node in LRB_nodes:
        ops.fix(node, 1, 1, 1, 1, 1, 1)

    Base_nodes = LRB_nodes
else:
    for node in floor_1_nodes:
        ops.fix(node, 1, 1, 1, 1, 1, 1)

    Base_nodes = floor_1_nodes

# Floor 2 nodes ------------------------------------------------------------
ops.node(201, 3735.0, 0.0, 4000.0)  
ops.node(202, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  4000.0)
ops.node(203, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 4000.0)
ops.node(204, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 4000.0)
ops.node(205, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 4000.0)
ops.node(206, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 4000.0)

floor_2_nodes = [201, 202, 203, 204, 205, 206]

# Floor 3 nodes ------------------------------------------------------------
ops.node(301, 3735.0, 0.0, 7500.0)  
ops.node(302, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  7500.0)
ops.node(303, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 7500.0)
ops.node(304, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 7500.0)
ops.node(305, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 7500.0)
ops.node(306, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 7500.0)

floor_3_nodes = [301, 302, 303, 304, 305, 306]

# Floor 4 nodes ------------------------------------------------------------
ops.node(401, 3735.0, 0.0, 11000.0)  
ops.node(402, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  11000.0)
ops.node(403, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 11000.0)
ops.node(404, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 11000.0)
ops.node(405, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 11000.0)
ops.node(406, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 11000.0)

floor_4_nodes = [401, 402, 403, 404, 405, 406]

# Floor 5 nodes ------------------------------------------------------------
ops.node(501, 3735.0, 0.0, 14500.0)  
ops.node(502, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  14500.0)
ops.node(503, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 14500.0)
ops.node(504, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 14500.0)
ops.node(505, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 14500.0)
ops.node(506, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 14500.0)

floor_5_nodes = [501, 502, 503, 504, 505, 506]

# Floor 6 nodes ------------------------------------------------------------
ops.node(601, 3735.0, 0.0, 18000.0)  
ops.node(602, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  18000.0)
ops.node(603, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 18000.0)
ops.node(604, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 18000.0)
ops.node(605, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 18000.0)
ops.node(606, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 18000.0)

floor_6_nodes = [601, 602, 603, 604, 605, 606]

# Floor 7 nodes ------------------------------------------------------------
ops.node(701, 3735.0, 0.0, 21500.0)  
ops.node(702, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  21500.0)
ops.node(703, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 21500.0)
ops.node(704, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 21500.0)
ops.node(705, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 21500.0)
ops.node(706, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 21500.0)

floor_7_nodes = [701, 702, 703, 704, 705, 706]

# Floor 8 nodes ------------------------------------------------------------
ops.node(801, 3735.0, 0.0, 25000.0)  
ops.node(802, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  25000.0)
ops.node(803, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 25000.0)
ops.node(804, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 25000.0)
ops.node(805, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 25000.0)
ops.node(806, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 25000.0)

floor_8_nodes = [801, 802, 803, 804, 805, 806]

# Floor 9 nodes ------------------------------------------------------------
ops.node(901, 3735.0, 0.0, 28200.0)  
ops.node(902, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  28200.0)
ops.node(903, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 28200.0)
ops.node(904, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 28200.0)
ops.node(905, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 28200.0)
ops.node(906, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 28200.0)

floor_9_nodes = [901, 902, 903, 904, 905, 906]

# Nodes for impulsive and empty tank mass, convective mass ------------------------------------------------------------
ops.node(10, 0.0, 0.0, 28200.0 + 2995.0)  # impulsive and empty tank mass location
ops.node(11, 0.0, 0.0, 28200.0 + 3720.2)  # convective mass node for rigid link with staging
ops.node(12, 0.0, 0.0, 28200.0 + 3720.2)  # convective mass node for zero length element 

ops.fix(10, 0, 0, 1, 1, 1, 1)
ops.fix(11, 0, 0, 1, 1, 1, 1)
ops.fix(12, 0, 0, 1, 1, 1, 1)

# --------------------------------------------------------------------------------
# Master Nodes # ops.node(nodeTag, x, y, z)
# --------------------------------------------------------------------------------

ops.constraints('Transformation')
perp_direction = 3 

master_nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
vertical_nodes = master_nodes + [10, 11, 12]

ops.node(1, 0.0, 0.0, 0.0)          # Master node for floor 1
ops.node(2, 0.0, 0.0, 4000.0)       # Master node for floor 2
ops.node(3, 0.0, 0.0, 7500.0)       # Master node for floor 3
ops.node(4, 0.0, 0.0, 11000.0)      # Master node for floor 4
ops.node(5, 0.0, 0.0, 14500.0)      # Master node for floor 5
ops.node(6, 0.0, 0.0, 18000.0)      # Master node for floor 6
ops.node(7, 0.0, 0.0, 21500.0)      # Master node for floor 7
ops.node(8, 0.0, 0.0, 25000.0)      # Master node for floor 8
ops.node(9, 0.0, 0.0, 28200.0)      # Master node for floor 9

# ops.rigidDiaphragm(perp_direction, master_nodeTag, *slaveNodeTags)  
ops.rigidDiaphragm(perp_direction, 1, *floor_1_nodes)      
ops.rigidDiaphragm(perp_direction, 2, *floor_2_nodes)      
ops.rigidDiaphragm(perp_direction, 3, *floor_3_nodes)      
ops.rigidDiaphragm(perp_direction, 4, *floor_4_nodes)      
ops.rigidDiaphragm(perp_direction, 5, *floor_5_nodes)      
ops.rigidDiaphragm(perp_direction, 6, *floor_6_nodes)      
ops.rigidDiaphragm(perp_direction, 7, *floor_7_nodes)      
ops.rigidDiaphragm(perp_direction, 8, *floor_8_nodes)      
ops.rigidDiaphragm(perp_direction, 9, *floor_9_nodes)    

# ops.fix(master_nodeTag, x, y, z, Mx, My, Mz)     

if LRB_inclusion == 1: 
    ops.fix(1, 0, 0, 1, 1, 1, 0) 
else:
    ops.fix(1, 1, 1, 1, 1, 1, 1)

ops.fix(2, 0, 0, 1, 1, 1, 0)       
ops.fix(3, 0, 0, 1, 1, 1, 0)      
ops.fix(4, 0, 0, 1, 1, 1, 0)     
ops.fix(5, 0, 0, 1, 1, 1, 0)
ops.fix(6, 0, 0, 1, 1, 1, 0)
ops.fix(7, 0, 0, 1, 1, 1, 0)
ops.fix(8, 0, 0, 1, 1, 1, 0)
ops.fix(9, 0, 0, 1, 1, 1, 0)