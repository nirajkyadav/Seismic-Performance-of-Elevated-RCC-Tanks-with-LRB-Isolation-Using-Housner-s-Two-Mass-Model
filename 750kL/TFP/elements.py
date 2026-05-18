import openseespy.opensees as ops
import numpy as np
import matplotlib.pyplot as plt
import opsvis as opsv

from beam_col_sections import *             

# --------------------------------------------------------------------------------
# Rigid Link and Elastic Link Elements  # rigidLink(type, rNodeTag, cNodeTag)
# --------------------------------------------------------------------------------

ops.rigidLink('beam', 9, 10)
ops.rigidLink('beam', 9, 11)
ops.element('zeroLength', 1112, 11, 12, '-mat', parallel_material_tag, parallel_material_tag, '-dir', 1, 2, '-doRayleigh', 0)

# --------------------------------------------------------------------------------
# Beam and Column Elements
# --------------------------------------------------------------------------------

# Geometry transformations -----------------------
Beam_TransfTag = 1

Col_101_TransfTag = 2
Col_102_TransfTag = 3
Col_103_TransfTag = 4
Col_104_TransfTag = 5
Col_105_TransfTag = 6
Col_106_TransfTag = 7

#geomTransf(transfType, transfTag, *transfArgs)
ops.geomTransf('Linear', Beam_TransfTag, 0, 0, 1)  

ops.geomTransf('PDelta', Col_101_TransfTag, 3735.0, 0.0, 0.0)   
ops.geomTransf('PDelta', Col_102_TransfTag, 3735.0 * np.cos(60*np.pi/180),  3735.0 * np.sin(60*np.pi/180),  0.0)   
ops.geomTransf('PDelta', Col_103_TransfTag, 3735.0 * np.cos(120*np.pi/180), 3735.0 * np.sin(120*np.pi/180), 0.0)   
ops.geomTransf('PDelta', Col_104_TransfTag, 3735.0 * np.cos(180*np.pi/180), 3735.0 * np.sin(180*np.pi/180), 0.0)   
ops.geomTransf('PDelta', Col_105_TransfTag, 3735.0 * np.cos(240*np.pi/180), 3735.0 * np.sin(240*np.pi/180), 0.0)   
ops.geomTransf('PDelta', Col_106_TransfTag, 3735.0 * np.cos(300*np.pi/180), 3735.0 * np.sin(300*np.pi/180), 0.0)   

#  Integration setup -----------------------------

#beamIntegration('Lobatto', tag, secTag, N)
staging_beam_IntTag = 1
tank_bottom_beam_IntTag = 2

Col_IntTag = 3

numIntPts_Beam = 5
numIntPts_Col = 5

ops.beamIntegration('Lobatto', staging_beam_IntTag, Staging_Beam_SecTag, numIntPts_Beam)
ops.beamIntegration('Lobatto', tank_bottom_beam_IntTag, Tank_Buttom_Beam_SecTag, numIntPts_Beam)

ops.beamIntegration('Lobatto', Col_IntTag, Staging_Col_SecTag, numIntPts_Col)

#  Elements setup -----------------------------

staging_beam_mpul = 400.0 * 500.0 * gamma_conc / g  
tank_bottom_beam_mpul = 600.0 * 800.0 * gamma_conc / g
Col_mpul = 700.0 * 700.0 * gamma_conc / g

# --------------------------------------------------------------------------------
# Beam Elements ---- ops.element('forceBeamColumn', XBeamTag, startNode, endNode, Beam_X_TransfTag, Beam_1_IntTag, '-mass', Beam_1_mpul)
# --------------------------------------------------------------------------------

# Floor 1 Beams -----------------------------------
ops.element('forceBeamColumn', 101102, 101, 102, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 102103, 102, 103, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 103104, 103, 104, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 104105, 104, 105, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 105106, 105, 106, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 106101, 106, 101, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)

# Floor 2 Beams -----------------------------------
ops.element('forceBeamColumn', 201202, 201, 202, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 202203, 202, 203, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 203204, 203, 204, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 204205, 204, 205, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 205206, 205, 206, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 206201, 206, 201, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)

# Floor 3 Beams -----------------------------------
ops.element('forceBeamColumn', 301302, 301, 302, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 302303, 302, 303, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 303304, 303, 304, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 304305, 304, 305, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 305306, 305, 306, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 306301, 306, 301, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)

# Floor 4 Beams -----------------------------------
ops.element('forceBeamColumn', 401402, 401, 402, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 402403, 402, 403, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 403404, 403, 404, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 404405, 404, 405, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 405406, 405, 406, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 406401, 406, 401, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)

# Floor 5 Beams -----------------------------------
ops.element('forceBeamColumn', 501502, 501, 502, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 502503, 502, 503, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 503504, 503, 504, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 504505, 504, 505, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 505506, 505, 506, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 506501, 506, 501, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)

# Floor 6 Beams -----------------------------------
ops.element('forceBeamColumn', 601602, 601, 602, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 602603, 602, 603, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 603604, 603, 604, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 604605, 604, 605, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 605606, 605, 606, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 606601, 606, 601, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)

# Floor 7 Beams -----------------------------------
ops.element('forceBeamColumn', 701702, 701, 702, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 702703, 702, 703, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 703704, 703, 704, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 704705, 704, 705, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 705706, 705, 706, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 706701, 706, 701, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)

# Floor 8 Beams -----------------------------------
ops.element('forceBeamColumn', 801802, 801, 802, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 802803, 802, 803, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 803804, 803, 804, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 804805, 804, 805, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 805806, 805, 806, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)
ops.element('forceBeamColumn', 806801, 806, 801, Beam_TransfTag, staging_beam_IntTag, '-mass', staging_beam_mpul)

# Floor 9 Beams -----------------------------------
ops.element('forceBeamColumn', 901902, 901, 902, Beam_TransfTag, tank_bottom_beam_IntTag, '-mass', tank_bottom_beam_mpul)
ops.element('forceBeamColumn', 902903, 902, 903, Beam_TransfTag, tank_bottom_beam_IntTag, '-mass', tank_bottom_beam_mpul)
ops.element('forceBeamColumn', 903904, 903, 904, Beam_TransfTag, tank_bottom_beam_IntTag, '-mass', tank_bottom_beam_mpul)
ops.element('forceBeamColumn', 904905, 904, 905, Beam_TransfTag, tank_bottom_beam_IntTag, '-mass', tank_bottom_beam_mpul)
ops.element('forceBeamColumn', 905906, 905, 906, Beam_TransfTag, tank_bottom_beam_IntTag, '-mass', tank_bottom_beam_mpul)
ops.element('forceBeamColumn', 906901, 906, 901, Beam_TransfTag, tank_bottom_beam_IntTag, '-mass', tank_bottom_beam_mpul)


# --------------------------------------------------------------------------------
# Beam Element Tag Lists
# --------------------------------------------------------------------------------

staging_beams = [101102, 102103, 103104, 104105, 105106, 106101,
            201202, 202203, 203204, 204205, 205206, 206201,
            301302, 302303, 303304, 304305, 305306, 306301,
            401402, 402403, 403404, 404405, 405406, 406401,
            501502, 502503, 503504, 504505, 505506, 506501,
            601602, 602603, 603604, 604605, 605606, 606601,
            701702, 702703, 703704, 704705, 705706, 706701,
            801802, 802803, 803804, 804805, 805806, 806801
]

tank_bottom_beams = [901902, 902903, 903904, 904905, 905906, 906901]

all_beams = staging_beams + tank_bottom_beams

# --------------------------------------------------------------------------------
# Column Elements
# --------------------------------------------------------------------------------

# Columns between floor 1 and floor 2 -----------------------------------
ops.element('forceBeamColumn', 101201, 101, 201, Col_101_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 102202, 102, 202, Col_102_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 103203, 103, 203, Col_103_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 104204, 104, 204, Col_104_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 105205, 105, 205, Col_105_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 106206, 106, 206, Col_106_TransfTag, Col_IntTag, '-mass', Col_mpul)

# Columns between floor 2 and floor 3 -----------------------------------
ops.element('forceBeamColumn', 201301, 201, 301, Col_101_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 202302, 202, 302, Col_102_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 203303, 203, 303, Col_103_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 204304, 204, 304, Col_104_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 205305, 205, 305, Col_105_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 206306, 206, 306, Col_106_TransfTag, Col_IntTag, '-mass', Col_mpul)

# Columns between floor 3 and floor 4 -----------------------------------
ops.element('forceBeamColumn', 301401, 301, 401, Col_101_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 302402, 302, 402, Col_102_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 303403, 303, 403, Col_103_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 304404, 304, 404, Col_104_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 305405, 305, 405, Col_105_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 306406, 306, 406, Col_106_TransfTag, Col_IntTag, '-mass', Col_mpul)

# Columns between floor 4 and floor 5 -----------------------------------
ops.element('forceBeamColumn', 401501, 401, 501, Col_101_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 402502, 402, 502, Col_102_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 403503, 403, 503, Col_103_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 404504, 404, 504, Col_104_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 405505, 405, 505, Col_105_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 406506, 406, 506, Col_106_TransfTag, Col_IntTag, '-mass', Col_mpul)

# Columns between floor 5 and floor 6 -----------------------------------
ops.element('forceBeamColumn', 501601, 501, 601, Col_101_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 502602, 502, 602, Col_102_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 503603, 503, 603, Col_103_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 504604, 504, 604, Col_104_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 505605, 505, 605, Col_105_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 506606, 506, 606, Col_106_TransfTag, Col_IntTag, '-mass', Col_mpul)

# Columns between floor 6 and floor 7 -----------------------------------
ops.element('forceBeamColumn', 601701, 601, 701, Col_101_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 602702, 602, 702, Col_102_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 603703, 603, 703, Col_103_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 604704, 604, 704, Col_104_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 605705, 605, 705, Col_105_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 606706, 606, 706, Col_106_TransfTag, Col_IntTag, '-mass', Col_mpul)

# Columns between floor 7 and floor 8 -----------------------------------
ops.element('forceBeamColumn', 701801, 701, 801, Col_101_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 702802, 702, 802, Col_102_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 703803, 703, 803, Col_103_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 704804, 704, 804, Col_104_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 705805, 705, 805, Col_105_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 706806, 706, 806, Col_106_TransfTag, Col_IntTag, '-mass', Col_mpul)

# Columns between floor 8 and floor 9 -----------------------------------
ops.element('forceBeamColumn', 801901, 801, 901, Col_101_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 802902, 802, 902, Col_102_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 803903, 803, 903, Col_103_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 804904, 804, 904, Col_104_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 805905, 805, 905, Col_105_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 806906, 806, 906, Col_106_TransfTag, Col_IntTag, '-mass', Col_mpul)

# --------------------------------------------------------------------------------
# Column Element Tag Lists
# --------------------------------------------------------------------------------

all_columns = [
    101201, 102202, 103203, 104204, 105205, 106206,
    201301, 202302, 203303, 204304, 205305, 206306,
    301401, 302402, 303403, 304404, 305405, 306406,
    401501, 402502, 403503, 404504, 405505, 406506,
    501601, 502602, 503603, 504604, 505605, 506606,
    601701, 602702, 603703, 604704, 605705, 606706,
    701801, 702802, 703803, 704804, 705805, 706806,
    801901, 802902, 803903, 804904, 805905, 806906
]

all_elements = all_columns + all_beams