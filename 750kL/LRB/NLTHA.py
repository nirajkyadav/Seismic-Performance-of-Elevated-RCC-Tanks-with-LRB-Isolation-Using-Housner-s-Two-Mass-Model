import csv
import os

print("=====================================================")
print("=====================================================")

# --------------------------------------------------------------
# CSV Output Setup – "Without LRB NLTHA.csv"
# --------------------------------------------------------------

DATA_DIR = r"/Users/niraj/Downloads/Projects/Project_Geo_Lab/Elevated_Tank/750kL/LRB/Data"
# os.makedirs(DATA_DIR, exist_ok=True)
CSV_FILE = os.path.join(DATA_DIR, "With LRB NLTHA D.csv")

# Header row (row 1 – names, row 2 – units)
CSV_HEADERS = [
    "RSN",
    "PGA (g)",
    "Maximum Base Shear (kN)",
    "Maximum Overturning Moment (kN·m)",
    "ISD Floor 1 (%)", "ISD Floor 2 (%)", "ISD Floor 3 (%)", "ISD Floor 4 (%)",
    "ISD Floor 5 (%)", "ISD Floor 6 (%)", "ISD Floor 7 (%)", "ISD Floor 8 (%)",
    "Maximum ISD (%)",
    "Maximum Global Drift (%)",
    "PFA Node 1 (g)",
    "PFA Node 5 (g)",
    "PFA Node 9 (g)",
    "PFA Node 12 (g)",
    "Maximum LRB Displacement (Node 1) (mm)",
    "Maximum Top Displacement (Node 9) (mm)"
]

# Create the file with headers only if it does not already exist
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as _csv_f:
        _writer = csv.writer(_csv_f)
        _writer.writerow(CSV_HEADERS)
    print(f"Created CSV file: {CSV_FILE}")
else:
    print(f"CSV file already exists - results will be appended")

# --------------------------------------------------------------
# Ground Motion
# --------------------------------------------------------------

GM_RSN = 5676

pga = 0.32

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

direction = 2    # 1, 2 in X and Y Direction respectively

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
omegas = [lam**0.5 for lam in lambdas]
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

control_node = master_nodes[-1]     # node where displacement is read (Master Node of top floor)
NBayZ = 8
nodes_for_IDR = master_nodes

time = []
baseshear = []
overturning_moment = []                                # Base overturning moment (OTM)
control_node_disp = []
LRB_disp = []
drifts_all_floors = [[] for _ in range(NBayZ)]        # One list per floor
global_drifts = []

# Over Turning Moment DOF: for X-excitation (direction=1) → My = DOF 5
#                          for Y-excitation (direction=2) → Mx = DOF 4
otm_dof = 5 if direction == 1 else 4

floor_accels = {node: [] for node in vertical_nodes}    # Initialize acceleration storage

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
    basereac = sum(ops.nodeReaction(n, direction) for n in Base_nodes)
    baseshear.append(basereac / 1000)

    # Overturning moment: sum of moment reactions (DOF 4 or 5) at base nodes
    otm_reac = sum(ops.nodeReaction(n, otm_dof) for n in Base_nodes)
    overturning_moment.append(otm_reac / 1.0e6)  # Convert N·mm → kN·m

    control_node_disp.append(ops.nodeDisp(control_node, direction))
    LRB_disp.append(ops.nodeDisp(master_nodes[0], direction))

    # Record absolute floor acceleration at each master node
    # nodeAccel() returns relative acceleration; add ground acceleration to get absolute
    ground_acc = load_factors[min(round(tCurrent / dt), len(load_factors) - 1)] * factor  # mm/s²
    for node in vertical_nodes:
        rel_acc = ops.nodeAccel(node, direction)          # relative accel (mm/s²)
        abs_acc = (rel_acc + ground_acc) / g              # convert to g
        floor_accels[node].append(abs_acc)

    top_node_disp = ops.nodeDisp(control_node, direction)

    if LRB_inclusion == 1:
        total_height = 28200.0 + h_LRB
    else:
        total_height = 28200.0

    top_node_drift = abs(top_node_disp) / total_height
    global_drifts.append(top_node_drift)

    for temp_floor in range(NBayZ):
        bottom_node = nodes_for_IDR[temp_floor]   
        top_node = nodes_for_IDR[temp_floor + 1]    

        bottom_disp = ops.nodeDisp(bottom_node, direction)
        top_disp = ops.nodeDisp(top_node, direction)

        if temp_floor == 0:
            bay_width_Z = 4000.0
        elif temp_floor == 7:
            bay_width_Z = 3200.0
        else:
            bay_width_Z = 3500.0

        drift = abs(top_disp - bottom_disp) / bay_width_Z
        drifts_all_floors[temp_floor].append(drift)

# Eigenvalue analysis after earthquake -----------------------------------------------------
# Final_TimePeriods = EigenValues(3)
# print("Final Time Periods: ", [f"{p:.10f}" for p in Final_TimePeriods])

# Maximum Induced Base Shear -----------------------------------------------------
max_base_shear = max(np.abs(baseshear))
print(f"Maximum Induced Base Shear = {max_base_shear:.4f} kN")

# ── Print maximum absolute floor accelerations ──────────────────────────────
print("\n--- Maximum Absolute Floor Accelerations ---")
max_floor_accels = {}
for node in vertical_nodes:
    max_acc = max(np.abs(floor_accels[node]))
    max_floor_accels[node] = max_acc
    print(f"Node {node}: Peak Acceleration = {max_acc:.6f} g")

# Maximum Overturning Moment (OTM) ------------------------------------------------
max_otm = max(np.abs(overturning_moment))
print(f"Maximum Overturning Moment = {max_otm:.4f} kN·m")

max_control_node_disp = max(np.abs(control_node_disp))
max_LRB_disp = max(np.abs(LRB_disp))
print(f"Maximum Top Displacement = {max_control_node_disp:.4f} mm")
print(f"Maximum LRB Displacement = {max_LRB_disp:.4f} mm")

MIDRs = [max(drifts) for drifts in drifts_all_floors]

for i in range(NBayZ):
    print(f'MIDR for Floor {i+1} = {MIDRs[i] * 100:.4f} %')

MIDRall = max(MIDRs)
print(f'MIDR ALL = {MIDRall * 100:.4f} %')

max_global_drift = max(global_drifts) * 100
print("Maximum Global Drift = ", max_global_drift, "%")

# --------------------------------------------------------------
# Append results to CSV
# --------------------------------------------------------------

# Peak Floor Accelerations for nodes 1, 5, 9, 12
pfa_nodes = [1, 5, 9, 12]
pfa_values = [max_floor_accels.get(n, float('nan')) for n in pfa_nodes]

# Build the result row
result_row = [
    GM_RSN,
    pga,
    round(max_base_shear, 4),
    round(max_otm, 4),
    *[round(MIDRs[i] * 100, 6) for i in range(NBayZ)],   # ISD Floor 1-8 (%)
    round(MIDRall * 100, 6),                             # Maximum ISD (%)
    round(max_global_drift, 6),                          # Maximum Global Drift (%)
    *[round(v, 6) for v in pfa_values],                  # PFA Node bottom, mid, top, far-top (g)
    round(max_LRB_disp, 4),                              # Maximum LRB Displacement (mm)
    round(max_control_node_disp, 4)                      # Maximum Top Displacement (mm)
]

with open(CSV_FILE, "a", newline="") as _csv_f:
    _writer = csv.writer(_csv_f)
    _writer.writerow(result_row)

print(f"Results appended to: {CSV_FILE}")

ops.loadConst('-time', 0.0)
ops.remove('recorders') 