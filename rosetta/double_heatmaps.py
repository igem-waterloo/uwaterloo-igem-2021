import os
import re
import numpy as np
import matplotlib.pyplot as plt

base = 'sept28'
direct = os.listdir(base)
energy = []
resnames = []

vals = dict()

for file in direct:
    if file.endswith('pdb'):
        path = os.path.join(base, file)
        pdb = open(path)
        beng = []
        bres = []
        intable = False
        for line in pdb:

            if line.startswith('TOTAL_SCORE: '):
                muts = file.split('.')[1]
                muts = '$' + muts
                muts = muts.replace('$A-', '')
                muts = muts.replace(',A-', '$')
                muts = muts.replace(',_A-', '$') #modify this based on file name suffix
                muts = muts.split('$')
                muts = muts[:2]
                print(muts)

                one_in = vals.get(muts[0], None)
                if len(muts) < 2:
                    muts.append(muts[0])
                if one_in is None:
                    vals[muts[0]] = dict()
                    vals[muts[0]][muts[1]] = float(line.replace('TOTAL_SCORE: ', ''))
                else:
                    vals[muts[0]][muts[1]] = float(line.replace('TOTAL_SCORE: ', ''))

all_muts = []

for v in vals:
    all_muts.append(v)

energy = []
b_eng = []
for mut in all_muts:
    for mut2 in all_muts.__reversed__():
        print(mut + "aaaa" + mut2)
        b_eng.append(vals[mut][mut2])
    energy.append(b_eng)
    b_eng = []

energy = np.array(energy)

figure, axis = plt.subplots()
im = axis.imshow(energy)

ylabels = []
for v in direct:
    if v.endswith('pdb'):
        ylabels.append(v.replace('HETATM_relaxed', ''))

axis.set_yticks(np.arange(len(all_muts)))
axis.set_yticklabels(all_muts)

all_muts.reverse()

axis.set_xticks(np.arange(len(all_muts)))
axis.set_xticklabels(all_muts)

axis.set_ylabel("Mutation 1")
axis.set_xlabel("Mutation 2")

plt.title('Double Mutant Overall Energy Scores')

cbar = plt.colorbar(im)
desc = ""
cbar.ax.set_ylabel("Overall Energy Score (Rosetta Energy Units)")

plt.setp(axis.get_xticklabels(), rotation=90, ha="right", va="center", rotation_mode="anchor")
plt.tight_layout()

plt.show()
