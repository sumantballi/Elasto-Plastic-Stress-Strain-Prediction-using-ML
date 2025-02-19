This folder contains the original data (fea_database), the preprocessed data (preprocessed) when using the script preprocess.py, as well as the FE model that was used to create the data (fea_model). The preprocessed data folder is most relevant when working on the project.

The following describes the data in the fea_database folder:

This database contains results from FE analyses of a plate with a hole.

The following apply for all cases:
Plated dimensions: 100 mm wide, 200 mm high, 2 mm thick, 20 mm diameter of hole.
Load is applied as nodal forces in the vertical direction (y-direction) on the upper and bottom edge.
Symmetry boundary conditions are applied on the horizontal symmetry line.
The mesh consists of linear quadrilateral elements (QUAD4).

The following apply to specific cases:
1) Baseline: The hole is positioned in the center of the plate (50 mm from the left edge). Load is applied as uniformly distributed. The mesh density is high (936 elements, 1014 nodes). Contains 1000 FE simulations of different applied loads from 70 N to 70 kN.
2) Linear load: The load is not uniform; it increases linearly (starting at zero) from left to right. Otherwise as the baseline case. Contains 500 FE simulations of different applied loads from 70 N to 70 kN.
3) Off center 1: The center of the hole is positioned 40 mm from the left edge. Otherwise as the baseline case. Contains 500 FE simulations of different applied loads from 70 N to 70 kN.
4) Off center 2: The center of the hole is positioned 30 mm from the left edge. Otherwise as the baseline case. Contains 500 FE simulations of different applied loads from 70 N to 70 kN.
5) Off center 3: The center of the hole is positioned 20 mm from the left edge. Otherwise as the baseline case. Contains 500 FE simulations of different applied loads from 70 N to 70 kN.
6) Coarse mesh: Same as the baseline case but with a coarser mesh (352 elements, 402 nodes). Contains 500 FE simulations of different applied loads from 70 N to 70 kN.

The data files should be interpreted the following way:
The files contains two blocks: INPUT and OUTPUT
INPUT: Gives the x- and y-coordinates of the nodes (X and Y) where nodal forces are applied and their corresponding force components in N in the x- and y-direction (FX and FY).
OUTPUT: Gives the results from the FE analysis at each node. For each node is given: x- and y-coordinates (X and Y), equivalent total strain in mm/mm (EPTOeqv), equivalent elastic strain in mm/mm (EPELeqv), equivalent plastic strain in mm/mm (EPPLeqv) and equivalent (von Mises) stress in MPa (Seqv).

An FE model is also supplied in case you would like to generate additional data. The model is generated in Ansys Workbench 2022 R2 and can be opened in that or later versions.
In its current form, loads are applied using an APDL script. It works like this: the x-component of the total applied force in N is given as ARG1 and the y-component of the total applied force in N is given as ARG2. The total applied force is the integral over the line load (i.e. the total applied force you give will be recalculated into a corresponding line load in N/mm). The given y-component (ARG2) will be applied positive on the upper edge and negative on the bottom edge (i.e. symmetrically) and the x-component (ARG1) will be applied positive on the upper edge and negative on the bottom edge (i.e. antisymmetrically).
An APDL script under "Solution" writes data to file. The resulting file is called "fea_results.txt" and ends up in the current working directory; typically something like ".../dp0/SYS-#/MECH/fea_results.txt" where # = 1, 2, 3, ... is the internal numbering of the analysis system.

Q how to improve prediction, only epoch changed. is there a systematic practical method?
Q Per sample, the values are not equally distributed: add weights for loss calculation or sample in different sizes. How to implement any of the methods