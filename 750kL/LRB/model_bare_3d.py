import openseespy.opensees as ops
import numpy as np
import matplotlib.pyplot as plt
import opsvis as opsv
import vfo

from nodal_mass_and_udl import *

if LRB_inclusion == 1:
    from LRB_elements import *

# --------------------------------------------------------------------------------
# Eigenvalue Analysis 
# --------------------------------------------------------------------------------
numModes = 5
lambdas = ops.eigen(numModes)  # returns a list of eigenvalues
# print(lambdas)

omega = []
frequencies = []
periods = []

for lam in lambdas:
    sqrt_lam = lam ** 0.5
    omega.append(sqrt_lam)
    frequencies.append(sqrt_lam / (2 * np.pi))
    periods.append((2 * np.pi) / sqrt_lam)

print("Initial Time Periods:", [f"{p:.10f}" for p in periods])

UDL_applier()

# def Plotter():
#     # Define extruded shapes for elements
#     ele_shapes = {}
    
#     # Staging beams: 400mm width x 500mm depth
#     for ele in staging_beams:
#         ele_shapes[ele] = ['rect', [500.0, 400.0]]
        
#     # Tank bottom beams: 600mm width x 800mm depth
#     for ele in tank_bottom_beams:
#         ele_shapes[ele] = ['rect', [800.0, 600.0]]
        
#     # Columns: 700mm width x 700mm depth
#     for ele in all_columns:
#         ele_shapes[ele] = ['rect', [700.0, 700.0]]
        
#     # Monkey-patch ops.getEleTags to avoid opsvis crashing on zeroLength elements
#     original_getEleTags = ops.getEleTags
#     ops.getEleTags = lambda: all_columns + staging_beams + tank_bottom_beams
    
#     try:
#         # Plot the extruded 3D shapes
#         opsv.plot_extruded_shapes_3d(ele_shapes, fig_wi_he=(14.0, 10.0))
#     finally:
#         # Restore original ops.getEleTags
#         ops.getEleTags = original_getEleTags
        
#     ax = plt.gca()
    
#     # 1. Rigid shell like diaphragm at top of staging
#     R = 3735.0
#     z_top = 28200.0
#     angles = [0, 60, 120, 180, 240, 300]
#     diaphragm_pts = []
#     for ang in angles:
#         rad = ang * np.pi / 180
#         diaphragm_pts.append([R * np.cos(rad), R * np.sin(rad), z_top])
    
#     from mpl_toolkits.mplot3d.art3d import Poly3DCollection
#     poly = Poly3DCollection([diaphragm_pts], alpha=0.6, facecolor='cyan', edgecolor='black')
#     ax.add_collection3d(poly)
    
#     # 2. Rigid link from center (Node 9) to impulsive mass (Node 10)
#     z_9 = 28200.0
#     z_10 = 28200.0 + 2995.0
#     ax.plot([0, 0], [0, 0], [z_9, z_10], color='black', alpha =1.0, linewidth=3)
    
#     # 3. Spring from impulsive mass (Node 10) to convective mass (Node 12)
#     z_12 = 28200.0 + 4720.2
#     num_coils = 5
#     t = np.linspace(0, num_coils * 2 * np.pi, 100)
#     spring_radius = 100.0
#     x_spring = spring_radius * np.cos(t)
#     y_spring = spring_radius * np.sin(t)
#     z_spring = np.linspace(z_10, z_12, 100)
#     ax.plot(x_spring, y_spring, z_spring, color='green', linewidth=2)
    
#     # 4. Represent the masses
#     # Impulsive mass
#     ax.scatter([0], [0], [z_10], color='red', s=50, depthshade=False)
#     # Convective mass
#     ax.scatter([0], [0], [z_12], color='blue', s=50, depthshade=False)
    
#     plt.title("3D Extruded Model")

#     plt.show()

def newPlotter():
    # Define extruded shapes for elements
    ele_shapes = {}
    
    # Staging beams: 400mm width x 500mm depth
    for ele in staging_beams:
        ele_shapes[ele] = ['rect', [500.0, 400.0]]
        
    # Tank bottom beams: 600mm width x 800mm depth
    for ele in tank_bottom_beams:
        ele_shapes[ele] = ['rect', [800.0, 600.0]]
        
    # Columns: 700mm width x 700mm depth
    for ele in all_columns:
        ele_shapes[ele] = ['rect', [700.0, 700.0]]
        
    # Monkey-patch ops.getEleTags to avoid opsvis crashing on zeroLength elements
    original_getEleTags = ops.getEleTags
    ops.getEleTags = lambda: all_columns + staging_beams + tank_bottom_beams
    
    try:
        # Plot the extruded 3D shapes
        opsv.plot_extruded_shapes_3d(ele_shapes, fig_wi_he=(14.0, 10.0))
    finally:
        # Restore original ops.getEleTags
        ops.getEleTags = original_getEleTags
        
    ax = plt.gca()
    
    # --- THE FIXED LAYER ENGINE ---
    # 1. Disable dynamic camera-distance sorting so manual zorders are strictly obeyed
    ax.computed_zorder = False
    
    # 2. Push all existing structural elements from opsvis into the furthest background layer
    for artist in ax.collections + ax.lines + ax.patches:
        artist.set_zorder(1)
    # ------------------------------

    # 1. Rigid shell like diaphragm at top of staging
    R = 3735.0
    z_top = 28200.0
    angles = [0, 60, 120, 180, 240, 300]
    diaphragm_pts = []
    for ang in angles:
        rad = ang * np.pi / 180
        diaphragm_pts.append([R * np.cos(rad), R * np.sin(rad), z_top])
    
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    # Layer 2: Diaphragm sits right in front of the tower elements
    poly = Poly3DCollection([diaphragm_pts], alpha=0.6, facecolor='cyan', edgecolor='black', zorder=2)
    ax.add_collection3d(poly)
    
    # 2. Rigid link from center (Node 9) to impulsive mass (Node 10)
    z_9 = 28200.0
    z_10 = 28200.0 + 2995.0
    # Layer 3: Solid black line drawn purely over the diaphragm
    ax.plot([0, 0], [0, 0], [z_9, z_10], color='black', alpha=1.0, linewidth=3, zorder=3)
    
    # 3. Spring from impulsive mass (Node 10) to convective mass (Node 12)
    z_12 = 28200.0 + 4720.2
    num_coils = 5
    t = np.linspace(0, num_coils * 2 * np.pi, 100)
    spring_radius = 100.0
    x_spring = spring_radius * np.cos(t)
    y_spring = spring_radius * np.sin(t)
    z_spring = np.linspace(z_10, z_12, 100)
    # Layer 4: Spring drawn above the rigid link layer
    ax.plot(x_spring, y_spring, z_spring, color='green', linewidth=2, zorder=4)
    
    # 4. Represent the masses
    # Layer 5: Point masses pinned to the absolute front layer
    # Impulsive mass
    ax.scatter([0], [0], [z_10], color='red', s=50, depthshade=False, zorder=5)
    # Convective mass
    ax.scatter([0], [0], [z_12], color='blue', s=50, depthshade=False, zorder=5)
    
    # Hide axes
    ax.set_axis_off()
    
    # Maximize plot area by removing margins
    fig = plt.gcf()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    
    # Zoom in slightly (default is usually 10)
    ax.dist = 8
    
    # Attempt to full screen the window
    manager = plt.get_current_fig_manager()
    try:
        manager.full_screen_toggle()
    except Exception:
        pass
        
    plt.title("3D Extruded Model")
    plt.show()

newPlotter()