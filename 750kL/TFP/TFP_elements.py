import openseespy.opensees as ops

from Dimensions_and_nodes import *

# --------------------------------------------------------------------------------
# Triple Friction Pendulum Isolator 
# --------------------------------------------------------------------------------

L1, L2, L3 = 400.00, 3940.00, 3940.00   # effective radii (mm)
d1, d2, d3 = 90.00, 380.00, 380.00      # displacement limits (mm)

mu_outer = 0.06        # μ on outer surfaces 2 & 3 (higher, e.g. PTFE-stainless)
mu_inner = 0.02        # μ on inner surfaces 1 & 4 (lower)

# Coulomb friction models — one per interface
ops.frictionModel('Coulomb', 1, mu_outer)   # surface 2
ops.frictionModel('Coulomb', 2, mu_inner)   # inner surfaces 1 & 4
ops.frictionModel('Coulomb', 3, mu_outer)   # surface 3

# Support materials
ops.uniaxialMaterial('Elastic', 10, 1.0e10)   # vertMat (very stiff compression)
ops.uniaxialMaterial('Elastic', 11, 1.0e10)   # rotZ — rigid rotation about Z
ops.uniaxialMaterial('Elastic', 12, 1.0e10)   # rotX (unused in 2D, but required)
ops.uniaxialMaterial('Elastic', 13, 1.0e10)   # rotY (unused in 2D, but required)

# Bearing parameters common to all
uy   = 0.5                  # 0.5 mm sliding threshold
kvt  = 1.0e6                # tension stiffness
tol  = 1.0e-6               # tolerance
W = 13715.3354 * 1000       # N
minFv=0.05*W                # minimum vertical force

# --------------------------------------------------------------------------------
# TFP Elements
# --------------------------------------------------------------------------------

for i in range(1, 7):
    node_i   = 1000 + i
    node_j   = 100  + i
    elem_tag = 1000 * node_i + node_j
    ops.element('TripleFrictionPendulum', elem_tag, node_i, node_j,          
                    1, 2, 3,                   # frnTag1, 2, 3
                    10,                        # vertMatTag
                    11, 12, 13,                # rotZ, rotX, rotY
                    L1, L2, L3,
                    d1, d2, d3,
                    W, uy, kvt, minFv, tol)