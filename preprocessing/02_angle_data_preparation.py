#!/usr/bin/env python
# coding: utf-8

# # PREPARE THE DATA
# The data here prepared will be used to train the model.

# In[1]:


""" The dataset here prepared will contain N proteins in one-hot 21-dimensional
    20 dimensions for one-hot encoding + the Van der Waals radius of the AA.
    Plus 21 dimensions more for the PSSM (Position Specific Scoring Matrix)
    Input prepraed will be a Nx34x34x(21+21) tensor and will have 2 angles as output. 
"""

# import libraries
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


# Helper functions to extract numeric data from text
def parse_lines(raw):
    return np.array([[float(x) for x in line.split(" ") if x != ""] for line in raw])

def parse_line(line):
    return np.array([float(x) for x in line.split(" ") if x != ""])


# In[3]:


path = "../data/angles/full_angles_under_200.txt"
# Opn file and read text
with open(path, "r") as f:
    lines = f.read().split('\n')


# In[4]:


# Scan first n proteins
names = []
seqs = []
psis = []
phis = []
pssms = []

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
        pssms.append(parse_lines(lines[i+1:i+22]))
    elif lines[i] == "[PHI]":
        phis.append(parse_line(lines[i+1]))
    elif lines[i] == "[PSI]":
        psis.append(parse_line(lines[i+1]))
        # Progress control
        if len(names)%50 == 0:
            print("Currently @ ", len(names), " out of n")


# In[5]:


# Length of masking - 17x2 AAs
def onehotter_aa(seq, pos):
    pad = 17
    # Pad sequence
    key = "HRKDENQSYTCPAVLIGFWM"
    # Van der Waals radius
    vdw_radius = {"H": 118, "R": 148, "K": 135, "D": 91, "E": 109, "N": 96, "Q": 114,
                  "S": 73, "Y": 141, "T": 93, "C": 86, "P": 90, "A": 67, "V": 105,
                  "L": 124, "I": 124, "G": 48, "F": 135, "W": 163, "M": 124}
    radius_rel = vdw_radius.values()
    basis = min(radius_rel)/max(radius_rel)
    # Surface exposure 
    surface = {"H": 151, "R": 196, "K": 167, "D": 106, "E": 138, "N": 113, "Q": 144,
                  "S": 80, "Y": 187, "T": 102, "C": 104, "P": 105, "A": 67, "V": 117,
                  "L": 137, "I": 140, "G": 0, "F": 175, "W": 217, "M": 160}
    surface_rel = surface.values()
    surface_basis = min(surface_rel)/max(surface_rel)
    # One-hot encoding
    one_hot = []
    for i in range(pos-pad, pos+pad): # alponer los guiones ya tiramos la seq para un lado
        vec = [0 for i in range(22)]
        # mark as 1 the corresponding indexes
        for j in range(len(key)):
            if seq[i] == key[j]:
                vec[j] = 1
                # Add Van der Waals relative radius
                vec[-2] = vdw_radius[key[j]]/max(radius_rel)-basis
                vec[-1] = surface[key[j]]/max(surface_rel)-surface_basis
        
        one_hot.append(vec) 
    
    return np.array(one_hot)


# In[6]:


#Crops the PSSM matrix
def pssm_cropper(pssm, pos):
    pssm_out = []
    pad = 17
    for i,row in enumerate(pssm):
        pssm_out.append(row[pos-pad:pos+pad])
    # PSSM is Lx21 - solution: transpose
    return np.array(pssm_out)


# In[7]:


# Ensure all features have same n. prots
print("Names: ", len(names))
print("Seqs: ", len(seqs))
print("PSSMs: ", len(pssms))
print("Phis: ", len(phis))
print("Psis: ", len(psis))


# In[8]:


input_aa = []
input_pssm = []
outputs = []


# In[9]:


long = 0 # Counter to ensure everythings fine

for i in range(len(seqs)): 
    if len(seqs[i])>17*2:
        long += len(seqs[i])-17*2
        for j in range(17,len(seqs[i])-17):
        # Padd sequence
            input_aa.append(onehotter_aa(seqs[i], j))
            input_pssm.append(pssm_cropper(pssms[i], j))
            outputs.append([phis[i][j], psis[i][j]])
            # break
        # print(i, "Added: ", len(seqs[i])-34,"total for now:  ", long)
print("TOTAL:", long, len(input_aa))


# In[10]:


#Check everything's fine
print("Outputs: ", len(outputs))
print("Inputs AAs: ", len(input_aa))
print("Inputs PSSMs: ", len(input_pssm))


# #### Reshape the inputs

# In[11]:


input_aa = np.array(input_aa).reshape(len(input_aa), 17*2, 22)
input_aa.shape


# In[12]:


input_pssm = np.array(input_pssm).reshape(len(input_pssm), 17*2, 21)
input_pssm.shape


# In[13]:


# Helper function to save data to a .txt file
def stringify(vec):
    return "".join(str(v)+" " for v in vec)


# In[14]:


# Save outputs to txt file
with open("../data/angles/outputs.txt", "a") as f:
    for o in outputs:
        f.write(stringify(o)+"\n")


# In[15]:


# Save AAs & PSSMs data to different files (together makes a 3dims tensor)
# Will concat later
with open("../data/angles/input_aa.txt", "a") as f:
    for aas in input_aa:
        f.write("\nNEW\n")
        for j in range(len(aas)):
            f.write(stringify(aas[j])+"\n")


# In[16]:


with open("../data/angles/input_pssm.txt", "a") as f:
    for k in range(len(input_pssm)):
        f.write("\nNEW\n")
        for j in range(len(input_pssm[k])):
            f.write(stringify(input_pssm[k][j])+"\n")


# # Done!
