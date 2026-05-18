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

['section', 'Fiber', Staging_Beam_SecTag, '-GJ', 1.0e10],
['patch', 'rect', confined_concrete_tag, 6, 6, *[-175.0, -225.0], *[175.0, 225.0]], # core

['patch', 'quad', unconfined_concrete_tag, 2, 6, *[175.0, -225.0], *[200.0, -250.0], *[200.0, 250.0], *[175.0, 225.0]],    # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-200.0,-250.0], *[-175.0,-225.0], *[-175.0, 225.0], *[-200.0, 250.0]],  # left side cover

['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-175.0, 225.0], *[175.0, 225.0], *[200.0, 250.0], *[-200.0, 250.0]],    # top cover
['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-200.0,-250.0], *[200.0,-250.0], *[175.0,-225.0], *[-175.0,-225.0]],    # bottom cover

['layer', 'straight', steel_tag, 3, area(16), *[-175.0, 225.0], *[175.0, 225.0]],  # top layer
['layer', 'straight', steel_tag, 3, area(16), *[-175.0, -225.0], *[175.0, -225.0]] # bottom layer

]

opsv.fib_sec_list_to_cmds(fiber_section_staging_beam)

# opsv.plot_fiber_section(fiber_section_staging_beam)
# plt.title("Beam Section for Staging")
# plt.axis('equal')
# plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

fiber_section_tank_bottom_beam = [

['section', 'Fiber', Tank_Buttom_Beam_SecTag, '-GJ', 1.0e10],
['patch', 'rect', confined_concrete_tag, 6, 6, *[-275.0, -375.0], *[275.0, 375.0]], # core

['patch', 'quad', unconfined_concrete_tag, 2, 6, *[275.0, -375.0], *[300.0, -400.0], *[300.0, 400.0], *[275.0, 375.0]],    # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-300.0,-400.0], *[-275.0,-375.0], *[-275.0, 375.0], *[-300.0, 400.0]],  # left side cover

['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-275.0, 375.0], *[275.0, 375.0], *[300.0, 400.0], *[-300.0, 400.0]],    # top cover
['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-300.0,-400.0], *[300.0,-400.0], *[275.0,-375.0], *[-275.0,-375.0]],    # bottom cover

['layer', 'straight', steel_tag, 5, area(20), *[-275.0, 375.0], *[275.0, 375.0]],            # top layer 
['layer', 'straight', steel_tag, 5, area(20), *[-275.0, -375.0], *[275.0, -375.0]],          # bottom layer 
['layer', 'straight', steel_tag, 3, area(16), *[-275.0, -750.0/4], *[-275.0, 750.0/4]],      # left layer 
['layer', 'straight', steel_tag, 3, area(16), *[275.0, -750.0/4], *[275.0, 750.0/4]]         # right layer 

]

opsv.fib_sec_list_to_cmds(fiber_section_tank_bottom_beam)

# opsv.plot_fiber_section(fiber_section_tank_bottom_beam)
# plt.title("Beam Section for tank bottom")
# plt.axis('equal')
# plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

# ------------------------------------------------------------------
# Columns 
# ------------------------------------------------------------------

fiber_section_staging_col = [

['section', 'Fiber', Staging_Col_SecTag, '-GJ', 1.0e10],
['patch', 'rect', confined_concrete_tag, 6, 6, *[-310.0, -310.0], *[310.0, 310.0]], # core

['patch', 'quad', unconfined_concrete_tag, 2, 6, *[310.0,-310.0], *[350.0,-350.0], *[350.0, 350.0], *[310.0,310.0]],     # right side cover
['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-350.0,-350.0], *[-310.0,-310.0], *[-310.0,310.0], *[-350.0, 350.0]], # left side cover

['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-310.0,310.0], *[310.0,310.0], *[350.0, 350.0], *[-350.0,350.0]],     # top side cover
['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-350.0,-350.0], *[350.0,-350.0], *[310.0,-310.0], *[-310.0,-310.0]],  # bottom side cover

['layer', 'straight', steel_tag, 4, area(25), *[310.0, -310.0], *[310.0, 310.0]],               # Right Layer
['layer', 'straight', steel_tag, 4, area(25), *[-310.0, -310.0], *[-310.0, 310.0]],             # Left Layer
['layer', 'straight', steel_tag, 2, area(25), *[-620.0/6.0, 310.0], *[620.0/6.0, 310.0]],       # Top Layer
['layer', 'straight', steel_tag, 2, area(25), *[-620.0/6.0, -310.0], *[620.0/6.0, -310.0]]      # Bottom Layer

]

opsv.fib_sec_list_to_cmds(fiber_section_staging_col)

# opsv.plot_fiber_section(fiber_section_staging_col)
# plt.title("Column Section for Staging")
# plt.axis('equal')
# plt.grid(True, color='gray', linestyle='--', linewidth=0.4, alpha=0.3)

# ------------------------------------------------------------------
# Plotting of the sections 
# ------------------------------------------------------------------

plt.show()