#!/usr/bin/env python
# coding: utf-8

# #  Calculate Dihedral Angles from Coordinates

# In[1]:


# Import libraries - LOAD THE DATA
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


def parse_line(raw):
    return np.array([[float(x) for x in line.split("\t") if x != ""] for line in raw])


# In[3]:


names = []
seqs = []
psis = []
phis = []
pssms = []
coords = []

path = "../data/full_under_200.txt"
# Opn file and read text
with open(path, "r") as f:
    lines = f.read().split('\n')


# In[4]:


# Extract numeric data from text
for i,line in enumerate(lines):
    if len(names) == 601:
        break
    # Read each protein separately
    if line == "[ID]":
        names.append(lines[i+1])
    elif line == "[PRIMARY]":
        seqs.append(lines[i+1])
    elif line == "[EVOLUTIONARY]":
        pssms.append(parse_line(lines[i+1:i+22]))
    elif line == "[TERTIARY]":
        coords.append(parse_line(lines[i+1:i+3+1]))
        # Progress control
        if len(names)%50 == 0:
            print("Currently @ ", len(names), " out of n")


# In[5]:


#Get the coordinates for 1 atom type
def separate_coords(full_coords, pos): # pos can be either 0(n_term), 1(calpha), 2(cterm)
    res = []
    for i in range(len(full_coords[1])):
        if i%3 == pos:
            res.append([full_coords[j][i] for j in range(3)])

    return np.array(res)


# In[6]:


# Organize by atom type
coords_nterm = [separate_coords(full_coords, 0) for full_coords in coords]
coords_calpha = [separate_coords(full_coords, 1) for full_coords in coords]
coords_cterm = [separate_coords(full_coords, 2) for full_coords in coords]


# In[7]:


# Check everything's ok
print("Length coords_calpha: ", len(coords_cterm))
print("Length coords_calpha[1]: ", len(coords_cterm[1]))
print("Length coords_calpha[1][1]: ", len(coords_cterm[1][1]))


# In[8]:


# Helper functions
def get_dihedral(coords1, coords2, coords3, coords4):
    """Returns the dihedral angle in degrees."""

    a1 = coords2 - coords1
    a2 = coords3 - coords2
    a3 = coords4 - coords3

    v1 = np.cross(a1, a2)
    v1 = v1 / (v1 * v1).sum(-1)**0.5
    v2 = np.cross(a2, a3)
    v2 = v2 / (v2 * v2).sum(-1)**0.5
    porm = np.sign((v1 * a3).sum(-1))
    rad = np.arccos((v1*v2).sum(-1) / ((v1**2).sum(-1) * (v2**2).sum(-1))**0.5)
    if not porm == 0:
        rad = rad * porm

    return rad


# In[9]:


# Compute angles for a protein
phis, psis = [], [] # phi always starts with a 0 and psi ends with a 0
ph_angle_dists, ps_angle_dists = [], []
for k in range(len(coords)):
    phi, psi = [0.0], []
    # Use our own functions inspired from bioPython
    for i in range(len(coords_calpha[k])):
        # Calculate phi, psi
        # CALCULATE PHI - Can't calculate for first residue
        if i>0:
            phi.append(get_dihedral(coords_cterm[k][i-1], coords_nterm[k][i], coords_calpha[k][i], coords_cterm[k][i])) # my_calc
            
        # CALCULATE PSI - Can't calculate for last residue
        if i<len(coords_calpha[k])-1: 
            psi.append(get_dihedral(coords_nterm[k][i], coords_calpha[k][i], coords_cterm[k][i], coords_nterm[k][i+1])) # my_calc
        
    # Add an extra 0 to psi (unable to claculate angle with next aa)
    psi.append(0)
    # Add protein info to register
    phis.append(phi)
    psis.append(psi)


# In[10]:


def stringify(vec):
    """ Helper function to save data to .txt file. """
    line = ""
    for v in vec:
        line = line+str(v)+" "
    return line

# Test function
print([stringify([1,2,3,4,5,6])])


# In[11]:


# Check angles distribution is a Ramachandran Plot (2nd and 3rd quads. dense)
n = 100
test_phi = []
for i in range(n):
    for test in phis[i]:
        test_phi.append(test)
test_phi = np.array(test_phi)

test_psi = []
for i in range(n):
    for test in psis[i]:
        test_psi.append(test)
test_psi = np.array(test_psi)

# For quadrants following trigonometry positions
quads = [0,0,0,0]
for i in range(len(test_phi)):
    if test_phi[i] >= 0 and test_psi[i] >= 0:
        quads[0] += 1
    elif test_phi[i] < 0 and test_psi[i] >= 0:
        quads[1] += 1
    elif test_phi[i] < 0 and test_psi[i] < 0:
        quads[2] += 1
    else:
        quads[3] += 1
        
print("Quadrants: ", quads, " from ", len(test_phi))


# In[12]:


# Visualize data. Check it matches the Ramachandran Plot distribution
# (Ergo check if angles are well computed)
plt.scatter(test_phi, test_psi, marker=".")
plt.xlim(-np.pi, np.pi)
plt.xlabel("Phi")
plt.ylabel("Psi")
plt.ylim(-np.pi, np.pi)
plt.show()


# In[13]:


# Data is OK. Can save it to file.
with open("../data/angles/full_angles_under_200.txt", "a") as f:
    for k in range(len(names)-1):
        # ID
        f.write("\n[ID]\n")
        f.write(names[k])
        # Seq
        f.write("\n[PRIMARY]\n")
        f.write(seqs[k])
        # PSSMS
        f.write("\n[EVOLUTIONARY]\n")
        for j in range(len(pssms[k])):
            f.write(stringify(pssms[k][j])+"\n")
        # PHI
        f.write("\n[PHI]\n")
        f.write(stringify(phis[k]))
        # PSI
        f.write("\n[PSI]\n")
        f.write(stringify(psis[k]))


# # Done!
