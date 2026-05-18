import openseespy.opensees as ops
import numpy as np

from Dimensions_and_nodes import *

# --------------------------------------------------------------------------------
# LRB Properties
# --------------------------------------------------------------------------------

alpha = 0.077						# Post-elastic stiffness ratio in shear

Fy_h = 10.6						# Yield stress of lead initially MPa
# Qd = Fyl0*np.pi*D1*D1/4             # Characteristic strength of lead rubber bearing  around 100 to around 500 kN
# Fy_h = Qd/(1-alpha)				  # Yield strength of elastomeric bearing in horizontal direction

Gr = 0.4                            # shear modulus of elastomeric bearing MPa
Kbulk = 2.0e+03                 	# Bulk modulus of rubber MPa

kc = 20.0							# Parameter for vertical cavitation
PhiM = 0.75							# Maximum damage index
ac = 1.0			                # Strength degradation parameter
sDratio = 0.5						# Shear distance ratio
mb = 0.0							# Mass of the bearing
cd = 0.0							# Viscous damping parameter, 128 Ns/mm

qL = 1.12e-8      					# Density of lead in N-s2/mm4
cL = 130.0e6                  		# Specific heat of lead in mm2/s2 oC
kS = 50.0							# Thermal conductivity of steel in N/s oC
aS = 14.1	  					    # Thermal Diffusitivity of steel in mm2/s

tag1 = 0						    # Tag for cavitation and post-cavitation
tag2 = 0	    	    			# Tag for buckling load variation
tag3 = 0			        		# Tag horizontal stiffness variation
tag4 = 0				        	# Tag for vertical stiffness variation
tag5 = 1		    				# Tag for strength degradation in shear due to heating of lead core

# --------------------------------------------------------------------------------
# LRB Elements
# --------------------------------------------------------------------------------

for i in range(1, 7):
    node_i   = 1000 + i
    node_j   = 100  + i
    elem_tag = 1000 * node_i + node_j
    ops.element('LeadRubberX', elem_tag, node_i, node_j,
                Fy_h, alpha, Gr, Kbulk,
                D1, D2, ts, tr, n,
                *[0.0, 0.0, 1.0], *[0.0, 1.0, 0.0],
                kc, PhiM, ac, sDratio, mb, cd,
                tc,
                qL, cL, kS, aS,
                tag1, tag2, tag3, tag4, tag5)