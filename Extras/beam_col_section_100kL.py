import openseespy.opensees as ops
import opsvis as opsv
import matplotlib.pyplot as plt
import numpy as np

from Dimensions_and_nodes import *
from Materials import *

def area(diameter):
    return (np.pi * diameter ** 2) / 4.0

Staging_Beam_SecTag = 1
Tank_Buttom_Beam_SecTag = 2
Staging_Col_SecTag = 3

# ------------------------------------------------------------------
# Beams 
# ------------------------------------------------------------------

fiber_section_staging_beam = [

['section', 'Fiber', Staging_Beam_SecTag, '-GJ', 1.0e6],
['patch', 'rect', confined_concrete_tag, 6, 6, *[-225.0, -150.0], *[225.0, 150.0]], # core

['patch', 'quad', unconfined_concrete_tag, 2, 6, *[225.0,-150.0], *[250.0, -175.0], *[250.0, 175.0], *[225.0, 150.0]],    # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-250.0,-175.0], *[-225.0,-150.0], *[-225.0, 150.0], *[-250.0, 175.0]], # left side cover

['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-225.0,150.0], *[225.0,150.0], *[250.0, 175.0], *[-250.0, 175.0]],     # top side cover
['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-250.0,-175.0], *[250.0,-175.0], *[225.0,-150.0], *[-225.0,-150.0]],   # bottom side cover

['layer', 'straight', steel_tag, 3, area(16), *[225.0, -150.0], *[225.0, 150.0]],  # right layer
['layer', 'straight', steel_tag, 3, area(16), *[-225.0, -150.0], *[-225.0, 150.0]] # left layer

]

opsv.fib_sec_list_to_cmds(fiber_section_staging_beam)

opsv.plot_fiber_section(fiber_section_staging_beam)
plt.title("Beam Section for Staging")
plt.axis('equal')
plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

fiber_section_tank_bottom_beam = [

['section', 'Fiber', Tank_Buttom_Beam_SecTag, '-GJ', 1.0e6],
['patch', 'rect', confined_concrete_tag, 9, 6, *[-225.0, -150.0], *[225.0, 150.0]],  # confined core

['patch', 'rect', unconfined_concrete_tag, 4, 6, *[25.0, 150.0], *[225.0, 425.0]],   # unconfined upper core
['patch', 'rect', unconfined_concrete_tag, 4, 6, *[25.0, -425.0], *[225.0, -150.0]], # unconfined bottom core

['patch', 'quad', unconfined_concrete_tag, 2, 18, *[225.0,-425.0], *[250.0, -450.0], *[250.0, 450.0], *[225.0, 425.0]],    # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[0.0,175.0], *[25.0, 150.0], *[25.0, 425.0], *[0.0, 450.0]],            # middle up cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[0.0,-450.0], *[25.0,-425.0], *[25.0, -150.0], *[0.0, -175.0]],         # middle down cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-250.0,-175.0], *[-225.0,-150.0], *[-225.0, 150.0], *[-250.0, 175.0]], # left side cover

['patch', 'quad', unconfined_concrete_tag, 5, 2, *[-225.0,150.0], *[25.0,150.0], *[0.0, 175.0], *[-250.0, 175.0]],        # top left cover
['patch', 'quad', unconfined_concrete_tag, 4, 2, *[25.0,425.0], *[225.0,425.0], *[250.0, 450.0], *[0.0, 450.0]],          # top right cover
['patch', 'quad', unconfined_concrete_tag, 5, 2, *[-250.0,-175.0], *[0.0,-175.0], *[25.0,-150.0], *[-225.0,-150.0]],      # bottom left cover
['patch', 'quad', unconfined_concrete_tag, 4, 2, *[0.0,-450.0], *[250.0,-450.0], *[225.0,-425.0], *[25.0,-425.0]],        # bottom right cover

['layer', 'straight', steel_tag, 4, area(20), *[225.0, -150.0], *[225.0, 150.0]],           # right right layer
['layer', 'straight', steel_tag, 4, area(20), *[175.0, -150.0], *[175.0, 150.0]],           # right left layer
['layer', 'straight', steel_tag, 4, area(20), *[-225.0, -150.0], *[-225.0, 150.0]],         # left left layer
['layer', 'straight', steel_tag, 4, area(20), *[-175.0, -150.0], *[-175.0, 150.0]],         # left right layer
['layer', 'straight', steel_tag, 2, area(12), *[75.0, -150.0], *[75.0, 150.0]],             # middle right layer
['layer', 'straight', steel_tag, 2, area(12), *[-75.0 , -150.0], *[-75.0, 150.0]]           # middle left layer

]

opsv.fib_sec_list_to_cmds(fiber_section_tank_bottom_beam)

opsv.plot_fiber_section(fiber_section_tank_bottom_beam)
plt.title("Beam Section for tank bottom")
plt.axis('equal')
plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

# ------------------------------------------------------------------
# Columns 
# ------------------------------------------------------------------

fiber_section_staging_col = [

['section', 'Fiber', Staging_Col_SecTag, '-GJ', 1.0e6],
['patch', 'rect', confined_concrete_tag, 6, 6, *[-185.0, -185.0], *[185.0, 185.0]], # core

['patch', 'quad', unconfined_concrete_tag, 2, 6, *[185.0,-185.0], *[225.0,-225.0], *[225.0, 225.0], *[185.0,185.0]],     # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-225.0,-225.0], *[-185.0,-185.0], *[-185.0,185.0], *[-225.0, 225.0]], # left side cover

['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-185.0,185.0], *[185.0,185.0], *[225.0, 225.0], *[-225.0,225.0]],     # top side cover
['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-225.0,-225.0], *[225.0,-225.0], *[185.0,-185.0], *[-185.0,-185.0]],  # bottom side cover

['layer', 'straight', steel_tag, 3, area(16), *[185.0, -185.0], *[185.0, 185.0]],               # Right Layer
['layer', 'straight', steel_tag, 3, area(16), *[-185.0, -185.0], *[-185.0, 185.0]],             # Left Layer
['layer', 'straight', steel_tag, 2, area(16), *[0, -185.0], *[0, 185.0]]                        # Middle Layer

]

opsv.fib_sec_list_to_cmds(fiber_section_staging_col)

opsv.plot_fiber_section(fiber_section_staging_col)
plt.title("Column Section for Staging")
plt.axis('equal')
plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

# ------------------------------------------------------------------
# Plotting of the sections 
# ------------------------------------------------------------------

plt.show()