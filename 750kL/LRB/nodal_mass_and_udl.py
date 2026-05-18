from elements import *

# --------------------------------------------------------------------------------
# Gravity loads
# --------------------------------------------------------------------------------

staging_beam_self_weight = staging_beam_mpul * g             # Staging Beam Self Weight N / mm
tank_bottom_beam_self_weight = tank_bottom_beam_mpul * g     # Tank Buttom Beam Self Weight N / mm
Col_self_weight = Col_mpul * g                               # Column Self Weight N/mm

weight_empty_tand_and_water = ((mass_empty_tank + mass_water) * g) / (3735.0 * 6)

# print(Col_self_weight, tank_bottom_beam_self_weight, staging_beam_self_weight)

# --------------------------------------------------------------------------------
# Nodal Mass Distribution; mass(nodeTag, *massValues)
# --------------------------------------------------------------------------------

ops.mass(10, mass_empty_tank + mass_impulsive_water, mass_empty_tank + mass_impulsive_water, 0.0, 0.0, 0.0, 0.0)
ops.mass(12, mass_convective_water, mass_convective_water, 0.0, 0.0, 0.0, 0.0)

# --------------------------------------------------------------------------------
# Application Of UDL in local coordinate axes # eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', '-beamUniform', Wy, <Wz>, Wx=0.0, '-beamPoint', Py, <Pz>, xL, Px=0.0, '-beamThermal', *tempPts)
# --------------------------------------------------------------------------------
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)

def UDL_applier():
    # UDL Application on Beams
    ops.eleLoad('-ele', *staging_beams, '-type', '-beamUniform', 0.0, -staging_beam_self_weight, 0.0)
    ops.eleLoad('-ele', *tank_bottom_beams, '-type', '-beamUniform', 0.0, -tank_bottom_beam_self_weight, 0.0)
    ops.eleLoad('-ele', *tank_bottom_beams, '-type', '-beamUniform', 0.0, -weight_empty_tand_and_water, 0.0)

    # weight_impulsive_node = (mass_empty_tank + mass_impulsive_water) * g
    # weight_convective_node = mass_convective_water * g

    # ops.load(10, 0.0, 0.0, -weight_impulsive_node, 0.0, 0.0, 0.0)
    # ops.load(12, 0.0, 0.0, -weight_convective_node, 0.0, 0.0, 0.0)

    # UDL Application on Columns
    ops.eleLoad('-ele', *all_columns, '-type', '-beamUniform', 0.0, 0.0, -Col_self_weight)