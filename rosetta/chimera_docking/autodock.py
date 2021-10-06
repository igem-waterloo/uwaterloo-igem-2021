import chimera
from chimera import runCommand as rc
import os
import numpy as np

os.chdir("/Users/kelliechong/documents/iGEM2021/uwaterloo-igem-2021/rosetta/1UTM_renum_HETATM_res171")
file_names = [fn for fn in os.listdir(".") if fn.endswith('.pdb')]
vina_split = "/Users/kelliechong/Documents/iGEM2021/autodock_vina_1_1_2/bin/vina_split.exe"
location = "/Users/kelliechong/Documents/iGEM2021/autodock_vina_1_1_2/bin/vina"
energy_file = open('energyScores.txt', 'w')

for fn in file_names:
    os.chdir("/Users/kelliechong/documents/iGEM2021/uwaterloo-igem-2021/rosetta/1UTM_renum_HETATM_res171")
    outFileName = fn.replace(".pdb", "").replace("1UTM_renumbered_ignorechain_HETATM_no_Ca.A-", "")+"_docked" 
    os.mkdir(os.path.join("/Users/kelliechong/Documents/iGEM2021/1UTM/rosetta/ligand_docking/docking/out/", outFileName))
    chimera.openModels.open(fn, type = "PDB")
    rc("delete #0:PEA.a")
    chimera.openModels.open("/Users/kelliechong/Documents/iGEM2021/1UTM/rosetta/ligand_docking/ligand_prep/PEA.pdb", type = "PDB")
    os.chdir("/Users/kelliechong//Documents/iGEM2021/1UTM/rosetta/ligand_docking/docking/out/" + outFileName)
    rc("vina docking receptor #0 ligand #1 output " + outFileName + " num_modes 1 wait true backend local location " + location )
    
    single_energy = open(outFileName, 'r').read()
    open(outFileName, 'r').close()

    os.chdir("../")
   
    energy_file.write('\n***\n\n')
    energy_file.write(outFileName+'\n')
    energy_file.write('\n'+single_energy)

energy_file.close()
# check for saving autodock vina results: https://www.researchgate.net/post/How_to_save_both_receptor_and_ligand_in_same_file
# save array as txt or csv file
# fin :) 

''' Run these two on the Python IDLE:
os.chdir("/Users/kelliechong/documents/iGEM2021/uwaterloo-igem-2021/rosetta/chimera_docking")
execfile('autodock.py')'''
