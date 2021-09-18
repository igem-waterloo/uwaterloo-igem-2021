import chimera
from chimera import runCommand as rc
import os

os.chdir("/Users/kelliechong/documents/iGEM 2021/uwaterloo-igem-2021/rosetta/1UTM_renum_HETATM_res171")
file_names = [fn for fn in os.listdir(".") if fn.endswith('.pdb')]
vina_split = "/Users/kelliechong/Documents/iGEM 2021/autodock_vina_1_1_2/bin/vina_split.exe"
location = "/Users/kelliechong/Documents/iGEM 2021/autodock_vina_1_1_2/bin/vina"
energy_scores = []
scores = None

for fn in file_names:
    outFileName = fn.replace(".pdb", "").replace("1UTM_renumbered_ignorechain_HETATM_no_Ca.A-", "")+"_docked" 
    os.mkdir(os.path.join("/Users/kelliechong/Documents/iGEM 2021/1UTM/rosetta/ligand_docking/docking/out/", outFileName))
    chimera.openModels.open(fn, type = "PDB")
    rc("delete #0:PEA.a")
    chimera.openModels.open("/Users/kelliechong/Documents/iGEM 2021/1UTM/rosetta/ligand_docking/ligand_prep/PEA.pdb", type = "PDB")
    rc("vina docking receptor #0 ligand #1 output '/Users/kelliechong/Documents/iGEM 2021/1UTM/rosetta/ligand_docking/docking/out/'" + outFileName + " wait true backend local location " + location )
    rc(vina_split + " --input " + outFileName + ".pdbqt")
    scores = np.loadtxt(outFileName)
    energy_scores.append(outFileName.replace("_docked", ""), #energy score here) #append energy score from line 2 of the output file from the autodock output
# check for saving autodock vina results: https://www.researchgate.net/post/How_to_save_both_receptor_and_ligand_in_same_file
# save array as txt or csv file
# fin :)