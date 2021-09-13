import chimera
import runCommand as rc
import os

os.chdir("/Users/kelliechong/documents/iGEM 2021/uwaterloo-igem-2021/rosetta/1UTM_renum_HETATM_res171")
file_names = [fn for fn in os.listdir(".") if fn.endswith('.pdb')]
for fn in file_names:
    outFileName = fn.replace(".pdb").replace("1UTM_renumbered_ignorechain_HETATM_no_Ca.A-")+"_docked" 
    os.mkdir(os.path.join("/Users/kelliechong/Documents/iGEM 2021/1UTM/rosetta/ligand_docking/docking/out/", outFileName))
    chimera.openModels.open(fn, type = "PDB")
    rc("delete #0:PEA.a")
    chimera.openModels.open("/Users/kelliechong/Documents/iGEM 2021/1UTM/rosetta/ligand_docking/ligand_prep/PEA.pdb", type = "PDB")
    location = "/Users/kelliechong/Documents/iGEM 2021/autodock_vina_1_1_2/bin/vina"
    rc("vina docking receptor #0 ligand #1 output '/Users/kelliechong/Documents/iGEM 2021/1UTM/rosetta/ligand_docking/docking/out/'" + outFileName + " wait true backend local location " + location )

# check for saving autodock vina results: https://www.researchgate.net/post/How_to_save_both_receptor_and_ligand_in_same_file