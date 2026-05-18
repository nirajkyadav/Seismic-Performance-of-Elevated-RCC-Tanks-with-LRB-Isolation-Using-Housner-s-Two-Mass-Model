import openseespy.opensees as ops
import matplotlib.pyplot as plt
import csv

# ops.wipe()

from Gravity_Analysis import *

print("---------------------------")
print("Gravity Analysis Done.")
print("---------------------------")

refLoad = 1000.0  # N

ops.timeSeries('Linear', 11)
ops.pattern('Plain', 11, 11)

push_direction = 2   # 1, 2 for Pushover in X and Y Direction Respectively
control_node = 9     # node where displacement is read

if push_direction == 2:
    print("Starting Pushover Analysis In Y Direction....")
    control_DOF = 2
elif push_direction == 1:
    print("Starting Pushover Analysis In X Direction....")
    control_DOF = 1
else:
    print("ERROR Pushover Direction.")

if push_direction == 2:
    for tag in master_nodes:
        ops.load(tag, 0.0, refLoad, 0.0, 0.0, 0.0, 0.0)
else:
    for tag in master_nodes:
        ops.load(tag, refLoad, 0.0, 0.0, 0.0, 0.0, 0.0)

#integrator('DisplacementControl', nodeTag, dof, incr, numIter=1, dUmin=incr, dUmax=incr)
dU = 0.05
ops.integrator('DisplacementControl', control_node, control_DOF, dU, 1, dU, dU)

if LRB_inclusion == 1:
    maxDisp = 0.04 * (28200.0 + h_LRB)
else:
    maxDisp = 0.04 * 28200.0
    
currentDisp = 0.0
controlNode_disp = []  
base_shear = []           # Base Shear is sum of reactions at base in control DOF
ok = 0

ops.test('NormDispIncr', 1.0e-6, 1000)
ops.algorithm('Newton')

temp = 1

while ok == 0 and currentDisp < maxDisp:

    ok = ops.analyze(1)

    if ok != 0:
        print("Newton failed. Trying different algorithms...")
        algorithms = [
            ('ModifiedNewton', ['-initial']),
            ('NewtonLineSearch', []),
            ('KrylovNewton', []),
            ('BFGS', [])
        ]
        for alg, args in algorithms:
            ops.algorithm(alg, *args)
            if ops.analyze(1) == 0:
                print(f"Succeeded with {alg}. Back to regular Newton.")
                ok = 0
                break
        ops.algorithm('Newton')

    currentDisp = ops.nodeDisp(control_node, control_DOF)
    controlNode_disp.append(currentDisp)

    ops.reactions()
    bShear = 0.0

    for node in Base_nodes:
        reaction =  -ops.nodeReaction(node, control_DOF)
        bShear += reaction
        ops.nodeResponse(node, control_DOF, 6)
    base_shear.append(bShear / 1.0e3)

    if temp % 20 == 0:
        print(f"Disp : Node {control_node} : {currentDisp:.3f} mm, Base Shear : {(bShear / 1000):.3f} kN")
    temp += 1

print(f"Maximum Base Shear = {(max(base_shear)):.2f} kN")
max_index = base_shear.index(max(base_shear))
disp_at_max_base_shear = controlNode_disp[max_index]
print(f"Displacement at Maximum Base Shear = {disp_at_max_base_shear:.2f} mm")
drift = ( disp_at_max_base_shear / (maxDisp/0.04) ) * 100
print(f"Drift at Maximum Base Shear = {drift:.2f} %")

drift = [(d / (maxDisp/0.04)) * 100 for d in controlNode_disp]

csv_filename = "Bare Pushover.csv"           # Write to CSV file

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Drift (%)", "Base Shear (kN)"])   # Header (Column Names)
    for d, bs in zip(drift, base_shear):                # Write row-wise data
        writer.writerow([d, bs])

plt.plot(drift, base_shear, label='Control Node')
plt.title("Pushover Curve")

plt.xlabel("Drift (%)")
plt.xlim(-0.05, 4.05)
plt.ylim(-5, 1.1 * max(base_shear))

plt.ylabel("Base Shear (kN)")
plt.tick_params(direction='in', top=True, right=True)
plt.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()