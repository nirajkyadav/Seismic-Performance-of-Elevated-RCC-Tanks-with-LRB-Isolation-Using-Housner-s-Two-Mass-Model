import csv
import os

# --------------------------------------------------------------
# Moment Curvature Analysis 
# --------------------------------------------------------------
def MomentCurvature3D(secTag, axialLoad, DimBA, Cover, mu, numIncr, bendingAxis, Fy_steel, E0_steel):
    # Estimate yield curvature (Assuming no axial load and only top and bottom steel)
    epsy = Fy_steel / E0_steel   # Steel yield strain
    eff_d = DimBA - Cover        # d -- from top cover to lower rebar center in tension
    Kaxis = epsy/(0.7 * eff_d)   # Approximate yield curvature (when only steel yields)

    maxK = Kaxis * mu  # Maximum curvature for analysis
    
    # Define two nodes at (0,0,0)
    ops.node(1, 0.0, 0.0, 0.0)
    ops.node(2, 0.0, 0.0, 0.0)

    if bendingAxis == 'z':
        # Bending about local y-axis (curvature about z-axis, rotation DOF 6)
        ops.fix(1, 1, 1, 1, 1, 1, 1)
        ops.fix(2, 0, 1, 1, 1, 1, 0)
    elif bendingAxis == 'y':
        # Bending about local z-axis (curvature about y-axis, rotation DOF 5)
        ops.fix(1, 1, 1, 1, 1, 1, 1)
        ops.fix(2, 0, 1, 1, 1, 0, 1)
    else:
        raise ValueError("Invalid bendingAxis. Choose 'y' or 'z'.")

    # element('zeroLengthSection', eleTag, *eleNodes, secTag, <'-orient', *vecx, *vecyp>, <'-doRayleigh', rFlag>)
    ops.element('zeroLengthSection', 1, 1, 2, secTag) # zeroLengthSection element

    # Define constant axial load only at node 2
    ops.timeSeries('Constant', 100)
    ops.pattern('Plain', 100, 100)
    ops.load(2, axialLoad, 0.0, 0.0, 0.0, 0.0, 0.0)

    # Define analysis parameters
    # integrator('LoadControl', incr, numIter=1, minIncr=incr, maxIncr=incr)

    ops.integrator('LoadControl', 0, 1, 0, 0)
    ops.system('SparseGeneral', '-piv')
    ops.test('EnergyIncr', 1e-9, 10)
    ops.numberer('Plain')
    ops.constraints('Plain')
    ops.algorithm('Newton')
    ops.analysis('Static')

    # Apply the constant axial load only and reset time to zero
    ops.analyze(1)
    ops.loadConst('-time', 0.0)

    # Define reference moment based on the bending axis
    ops.timeSeries('Linear', 101)
    ops.pattern('Plain',101, 101)

    if bendingAxis == 'z':
        disp_dof = 6 
    elif bendingAxis == 'y':
        disp_dof = 5
        
    if bendingAxis == 'z':
        ops.load(2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)  # Moment about z-axis
    elif bendingAxis == 'y':
        ops.load(2, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)  # Moment about y-axis

    dK = maxK / numIncr
    # integrator('DisplacementControl', nodeTag, dof, incr, numIter=1, dUmin=incr, dUmax=incr)
    ops.integrator('DisplacementControl', 2, disp_dof, dK, 1, dK, dK)

    # Section analysis one step at a time to record results
    moments = []
    curvatures = []

    for i in range(numIncr):
        ops.analyze(1)
        curvature = ops.nodeDisp(2, disp_dof)
        moment = ops.getLoadFactor(101)  # Load factor multiplied by unit moment
        curvatures.append(curvature)
        moments.append(moment)

    # Estimate yield curvature and yield moment
    yield_curvature = None
    yield_moment = None
    for c, m in zip(curvatures, moments):
        if c >= (Kaxis):
            yield_curvature = c
            yield_moment = m
            break

    # Ultimate moment and curvature (maximum moment value)
    ultimate_moment = max(moments)
    ultimate_index = moments.index(ultimate_moment)
    ultimate_curvature = curvatures[ultimate_index]

    return abs(yield_curvature), abs(ultimate_curvature), abs(yield_moment), abs(ultimate_moment)


columns_by_floor = [[] for _ in range(NBayZ)]        # One list per floor
columns_by_floor[k].append(ColTag)

# Pre-allocate storage for results
section_data = {}  # Nested dict: {floor: {tag: {sec: [(time, deform, energy), ...]}}}
for floor in range(NBayZ):
    section_data[floor] = {}
    for tag in columns_by_floor[floor]:
        section_data[floor][tag] = {}
        for sec in range(1, 6):
            section_data[floor][tag][sec] = []  # List of (time, deformation, energy)

while ok == 0 and tCurrent < tFinal: 
    ok = ops.analyze(1, dt)

    if ok != 0:
        print("regular newton failed ... trying ModifiedNewton...")
        ops.test('NormDispIncr', 5.0e-4,  50, 0)
        ops.algorithm('ModifiedNewton')
        ok = ops.analyze( 1, .001)
        if ok == 0:
            # print("ModifiedNewton worked .. back to regular newton")
            ops.test('EnergyIncr', 5.0e-4,  10 )
            ops.algorithm('Newton')
        else:
            # print("ModifiedNewton failed ... trying Broyden...")
            ops.algorithm('Broyden')
            ok = ops.analyze( 1, .001)
        if ok == 0:
            # print("Broyden worked .. back to regular newton")
            ops.algorithm('Newton')
        else:
            # print("Broyden failed ... trying NewtonLineSearch...")
            ops.algorithm('NewtonLineSearch')
            ok = ops.analyze( 1, .001)
        if ok == 0:
            # print("NewtonLineSearch worked .. back to regular newton")
            ops.algorithm('Newton')
        else:
            # print("NewtonLineSearch failed ... trying KrylovNewton...")
            ops.algorithm('KrylovNewton')
            ok = ops.analyze( 1, .001)
        if ok == 0:
            # print("KrylovNewton worked .. back to regular newton")
            ops.algorithm('Newton')
        # else:
        #     print('Analysis Not Successful..')

    tCurrent = ops.getTime()
    time.append(tCurrent)
    ops.reactions()
    basereac = sum(ops.nodeReaction(n, direction) for n in support_nodes)
    baseshear.append(basereac / 1000)
    control_node_disp.append(ops.nodeDisp(control_node, direction))

    for temp_floor in range(NBayZ):
        base_node = nodes_forIDR[temp_floor]   
        top_node = nodes_forIDR[temp_floor + 1]    

        base_disp = ops.nodeDisp(base_node, direction)
        top_disp = ops.nodeDisp(top_node, direction)

        drift = abs(top_disp - base_disp) / bay_width_Z
        drifts_all_floors[temp_floor].append(drift)

    # Collect section results (deformation and energy)
    for floor in range(NBayZ):
        for tag in columns_by_floor[floor]:
            for sec in range(1, 6):
                try:
                    deform = ops.eleResponse(tag, 'section', sec, 'deformation')
                    energy = ops.eleResponse(tag, 'section', sec, 'energy')
                    section_data[floor][tag][sec].append((tCurrent, deform, energy))
                except:
                    # Skip if not available
                    section_data[floor][tag][sec].append((tCurrent, [0.0]*4, 0.0))
                    print("ERRRRRRR....")

for floor, tag_data in section_data.items():
    floor_output_dir = output_dir / f"Floor_{floor}"
    floor_output_dir.mkdir(parents=True, exist_ok=True)

    for tag, sec_data in tag_data.items():
        for sec, records in sec_data.items():
            f_curv = floor_output_dir / f"ele{tag}_sec{sec}_curv.out"
            f_ener = floor_output_dir / f"ele{tag}_energy_sec{sec}.out"

            with open(f_curv, 'w') as f1, open(f_ener, 'w') as f2:
                for t, deform, energy in records:
                    f1.write(f"{t:.3f} " + ' '.join(f"{val:.5e}" for val in deform) + "\n")
                    f2.write(f"{t:.3f} {' '.join(map(str, energy))}\n")

# -----------------------------------------------------
# Time History Output Analysis
# -----------------------------------------------------

# ops.wipe()
# ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)

# materials_function()
# Section_Builder()

direction = 2  # 1, 2 in X and Y Direction respectively

mu = 15.0           # Target ductility for analysis
numIncr = 100       # Number of analysis increment
P = -1000.0         # Set reference axial load 

phiy = [0,0,0] 
phiu = [0,0,0] 
yieldM = [0,0,0]
ultM = [0,0,0]

if direction == 2:
    ops.wipe()
    ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)
    materials_function()
    Section_Builder()
    phiy[0], phiu[0], yieldM[0], ultM[0] = MomentCurvature3D(Col_2_SecTag, P, Col_2_z, Col_2_Cover, mu, numIncr, 'z', Fy_steel, E0_steel)

    ops.wipe()
    ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)
    materials_function()
    Section_Builder()
    phiy[1], phiu[1], yieldM[1], ultM[1] = MomentCurvature3D(Col_3_SecTag, P, Col_3_z, Col_3_Cover, mu, numIncr, 'z', Fy_steel, E0_steel)

    if NBayZ == 3:
        ops.wipe()
        ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)
        materials_function()
        Section_Builder()
        phiy[2], phiu[2], yieldM[2], ultM[2] = MomentCurvature3D(Col_4_SecTag, P, Col_4_z, Col_4_Cover, mu, numIncr, 'z', Fy_steel, E0_steel)
else:
    print("ERROR Direction.")



nume_per_floor_park = []
deno_per_floor_park = []

for floor in range(NBayZ):

    beta = 0.1
    Et = []
    Sum_Et = 0.0
    DI_Storey = []

    print(f'Analyzing Damage in Storey {floor + 1}')
    DI_Local = []
    floor_output_dir = output_dir / f"Floor_{floor}"

    for tag in columns_by_floor[floor]:    
        file_curv = [floor_output_dir / f"ele{tag}_sec{i}_curv.out" for i in range(1, 6)]
        file_energy = [floor_output_dir / f"ele{tag}_energy_sec{i}.out" for i in range(1, 6)]

        phi_list = []
        total_ET = 0.0

        for file in file_curv:
            with open(file) as f:
                data = [list(map(float, line.split()[:4])) for line in f if len(line.split()) >= 4]
                filtered_data = np.array(data)  # time, curvature
            if direction == 1:
                phi = np.max(np.abs(filtered_data[:,3]))    # phi y
            else:
                phi = np.max(np.abs(filtered_data[:,2]))    # phi z
            phi_list.append(phi)
        phim = max(np.abs(phi_list))

        for file in file_energy:
            with open(file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1]
                    energy_value = float(last_line.strip().split()[1])
                    total_ET += energy_value

        if phim >= phiy[floor] and phiu[floor] > phiy[floor]:
            Et.append(total_ET)
            Sum_Et += total_ET

            DI_l = ((phim - phiy[floor]) / (phiu[floor] - phiy[floor])) + ((beta * total_ET) / (yieldM[floor] * phiu[floor]))
            DI_Local.append(DI_l)

    if len(DI_Local) > 0:
        DI_floor = sum(d * e for d, e in zip(DI_Local, Et)) / Sum_Et

        nume_per_floor_park.append(sum(d * e for d, e in zip(DI_Local, Et)))
        deno_per_floor_park.append(Sum_Et)

        # print(f"DI for Storey {floor + 1} for Ground Motion {CarlSagan} = {DI_floor * 100:.7f} %")
    else:
        DI_floor = 0.

        nume_per_floor_park.append(0.)
        deno_per_floor_park.append(0.)

        # print(f"Max induced curvature < Yield Curvature, so no damage for Storey {floor + 1}")

    DI_Storey.append(DI_floor)
    print(DI_floor)
    # print("-------------------------------")

DI_Global = max(DI_Storey)
if DI_Global >= 1.0:
    DI_Global = 1.0
print(f"Global Damage Index for Ground Motion {int(GM_no_data[CarlSagan])} = {DI_Global * 100:.7f} %")
output_array.append(round((DI_Global * 100),3))   # storey maximum

if sum(deno_per_floor_park) > 0:
    output_array.append( round((((sum(nume_per_floor_park)) / (sum(deno_per_floor_park))) * 100),3))  # all storey combined
else:
    output_array.append(0.0)

append_results(output_array)


# Clean up: delete all files in output_dir and its subdirectories, but keep the results file

import stat

def remove_readonly(func, path, excinfo):
    # Clear the readonly bit and reattempt the removal
    os.chmod(path, stat.S_IWRITE)
    func(path)

try:
    if output_dir.exists():
        shutil.rmtree(output_dir, onerror=remove_readonly)
        print(f"Deleted analysis output directory: {output_dir}")
except Exception as e:
    print(f"Error deleting analysis files: {e}")

completed_array = []
completed_array.append(int(sample_no_data[u]))
completed_array.append(int(GM_no_data[CarlSagan]))

append_completed_results(completed_array)
    












































# --------------------------------------------------------------
# Ground Motion
# --------------------------------------------------------------

GM_RSN = 334

pga = 0.35

original_pga_data = {
    5676: 0.36297,
    5259: 0.34798,
    4199: 0.29655,
    3282: 0.32222,
    2510: 0.33066,
    2476: 0.36627,
    334:  0.28209
}

original_pga = original_pga_data[GM_RSN]
factor = (pga * 9810) / original_pga # mm/s2 see the calculation in sheets Final Models Output Data          

direction = 1    # 1, 2 in X and Y Direction respectively

print("=====================================================")
if direction == 1:
    print("Time History Analysis in X Direction...")
elif direction == 2:
    print("Time History Analysis in Y Direction...")
else:
    print("ERROR Direction")

GM_input_file = f"/Users/niraj/Downloads/Projects/Project_Geo_Lab/GM/D/RSN_{GM_RSN}.txt"

load_factors = []

# Read and parse the file
with open(GM_input_file, "r") as f:
    lines = f.readlines()

# Extract time step from the line containing "Time Step"
for line in lines:
    if "Time Step" in line:
        dt = float(line.strip().split(":")[1].split()[0])
        break

# Skip lines until you reach the actual data
data_start_index = next(i for i, line in enumerate(lines) if "Time(sec)" in line) + 1

# Read acceleration values
for line in lines[data_start_index:]:
    if line.strip():  # skip empty lines
        parts = line.strip().split()
        if len(parts) >= 2:
            acc = float(parts[1])
            load_factors.append(acc)

tFinal = dt * len(load_factors) # Final time
print(f"RSN: {GM_RSN}, PGA: {pga}, g: {factor}, dt: {dt}, tFinal: {tFinal:.7f}, nPts: {len(load_factors)}")

# --------------------------------------------------------------
# Model
# --------------------------------------------------------------

from Gravity_Analysis import *
print("Gravity Analysis Done.") 

def EigenValues(nModes):
    lambdas = ops.eigen(nModes)  # returns a list of eigenvalues

    omega = []
    frequencies = []
    periods = []

    for lam in lambdas:
        sqrt_lam = lam ** 0.5
        omega.append(sqrt_lam)
        frequencies.append(sqrt_lam / (2 * np.pi))
        periods.append(round(((2 * np.pi) / sqrt_lam),5))
    
    return periods

# --------------------------------------------------------------
# RAYLEIGH damping (D = αM*M + βKcurr*Kcurrent + βKcomm*KlastCommit + βKinit*Kinitial)
# --------------------------------------------------------------

# Get first two structural modes (excluding convective modes)
modes = ops.eigen(6)
omegas = [lam**0.5 for lam in modes]
omega_i = omegas[2]   # first structural mode (≈ 3.53 rad/s)
omega_j = omegas[3]   # second structural mode (≈ same, orthogonal)

# Stiffness-proportional coefficient for 5% damping at omega_i and omega_j
zeta = 0.05
betaK = 2 * zeta / (omega_i + omega_j)   # no alphaM

# Define regions
# ops.region(1, '-ele', *all_elements)   # all staging elements
# ops.region(2, '-ele', 1112)            # convective spring

# Apply Rayleigh damping with ONLY betaK, restricted to staging region
# ops.rayleigh(0.0, 0.0, betaK, 0.0, '-region', 1)   # alphaM=0, betaKcurr=0, betaKinit=betaK, betaKcomm=0 
ops.rayleigh(0.0, 0.0, betaK, 0.0, '-ele', *all_elements)

# --------------------------------------------------------------
# Analysis by floor
# --------------------------------------------------------------

ops.wipeAnalysis()

ops.timeSeries('Path', 200, '-dt', dt, '-values', *load_factors, '-factor', factor)   # tag = 200
ops.pattern('UniformExcitation',  200,   direction,  '-accel', 200) 

ops.constraints('Transformation')
# ops.test('NormDispIncr', 1.0e-6, 50)
ops.test('EnergyIncr', 5.0e-4,  50 )
ops.algorithm('Newton')
ops.numberer('RCM')
ops.system('BandGen')
ops.integrator('Newmark',  0.5,  0.25 )
ops.analysis('Transient')

# Transient Analysis -----------------------------------------------------
# tFinal = nPts * dt
tCurrent = ops.getTime()
ok = 0

control_node = 9     # node where displacement is read (Master Node of top floor)
NBayZ = 8
nodes_for_IDR = master_nodes

time = []
baseshear = []
control_node_disp = []
drifts_all_floors = [[] for _ in range(NBayZ)]        # One list per floor

while ok == 0 and tCurrent < tFinal: 
    ok = ops.analyze(1, dt)

    if ok != 0:
        print("regular newton failed ... trying ModifiedNewton...")
        ops.test('NormDispIncr', 5.0e-4,  100, 0)
        ops.algorithm('ModifiedNewton')
        ok = ops.analyze( 1, 0.0005)
        if ok == 0:
            # print("ModifiedNewton worked .. back to regular newton")
            ops.test('EnergyIncr', 5.0e-4,  50 )
            ops.algorithm('Newton')
        else:
            # print("ModifiedNewton failed ... trying Broyden...")
            ops.algorithm('Broyden')
            ok = ops.analyze( 1, .0001)
        if ok == 0:
            # print("Broyden worked .. back to regular newton")
            ops.algorithm('Newton')
        else:
            # print("Broyden failed ... trying NewtonLineSearch...")
            ops.algorithm('NewtonLineSearch')
            ok = ops.analyze( 1, .0001)
        if ok == 0:
            # print("NewtonLineSearch worked .. back to regular newton")
            ops.algorithm('Newton')
        else:
            # print("NewtonLineSearch failed ... trying KrylovNewton...")
            ops.algorithm('KrylovNewton')
            ok = ops.analyze( 1, .0001)
        if ok == 0:
            # print("KrylovNewton worked .. back to regular newton")
            ops.algorithm('Newton')
        else:
            print('Analysis Not Successful..')

    tCurrent = ops.getTime()
    time.append(tCurrent)
    ops.reactions()
    basereac = sum(ops.nodeReaction(n, direction) for n in floor_1_nodes)
    baseshear.append(basereac / 1000)
    control_node_disp.append(ops.nodeDisp(control_node, direction))

    for temp_floor in range(NBayZ):
        base_node = nodes_for_IDR[temp_floor]   
        top_node = nodes_for_IDR[temp_floor + 1]    

        base_disp = ops.nodeDisp(base_node, direction)
        top_disp = ops.nodeDisp(top_node, direction)

        if temp_floor == 0:
            bay_width_Z = 4000.0
        elif temp_floor == 7:
            bay_width_Z = 3200.0
        else:
            bay_width_Z = 3500.0

        drift = abs(top_disp - base_disp) / bay_width_Z
        drifts_all_floors[temp_floor].append(drift)

# Eigenvalue analysis after earthquake -----------------------------------------------------
Final_TimePeriods = EigenValues(3)
print("Final Time Periods: ", [f"{p:.10f}" for p in Final_TimePeriods])

# Maximum Induced Base Shear -----------------------------------------------------
max_base_shear = max(np.abs(baseshear))
print(f"Maximum Induced Base Shear = {max_base_shear:.4f} kN")

max_control_node_disp = max(np.abs(control_node_disp))
print(f"Maximum Top Displacement = {max_control_node_disp:.4f} mm")

MIDRs = [max(drifts) for drifts in drifts_all_floors]

for i in range(NBayZ):
    print(f'MIDR for Floor {i+1} = {MIDRs[i] * 100:.4f} %')

MIDRall = max(MIDRs)
print(f'MIDR ALL = {MIDRall * 100:.4f} %')

ops.loadConst('-time', 0.0)
ops.remove('recorders') 