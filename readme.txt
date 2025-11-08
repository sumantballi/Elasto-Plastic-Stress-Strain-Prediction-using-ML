[![Release](https://img.shields.io/github/v/release/sumantballi/Elasto-Plastic-Stress-Strain-Prediction-using-ML?sort=semver)](https://github.com/sumantballi/Elasto-Plastic-Stress-Strain-Prediction-using-ML/releases)

## Introduction

This mini-project explores if a data-driven model can learn to predict stresses and strains in a loaded structure and how well it generalizes to variations in geometry, load distribution, and mesh density.

The setup is intentionally simple: a 2D plate with a circular hole, several FE variants (load patterns, hole location, mesh density), and a neural-network–style surrogate mapping loads and coordinates to nodal stress/strain measures.

No new FE modelling is the focus here; the project is about **using** a curated FE database to test how far a relatively simple ML model can go.

## What to look for

- Plate-with-hole benchmark with:
  - Baseline vs off-centred holes.
  - Uniform vs linearly varying edge loads.
  - Fine vs coarse meshes.
- Node-wise ML predictions for:
  - Equivalent total strain `EPTOeqv`.
  - Equivalent elastic strain `EPELeqv`.
  - Equivalent plastic strain `EPPLeqv`.
  - Equivalent von Mises stress `Seqv`.
- Generalization checks:
  - Train on some cases, test on unseen load patterns / hole positions / mesh density.
- Typical questions:
  - Does the model capture stress concentration around the hole?
  - How sensitive is it to data imbalance (many “low-stress” points vs few “hot-spot” points)?
  - What happens when we change training strategy (epochs, weighting, sampling)?

## Folder map

> The project assumes access to an FE dataset with the following structure:

- `fea_database/` – Original FE simulations of a plate with a hole.
- `preprocessed/` – Data after running `preprocess.py` (ML-ready; main working folder).
- `fea_model/` – FE model used to generate the database (Ansys Workbench 2022 R2).

In this GitHub repo you currently find:

- `preprocess.py` – Script to convert FE text output into structured, ML-ready data.
- `Task_1 (2).ipynb` – First task / exploratory notebook on the dataset.
- `Task_2 (1).ipynb` – Follow-up analyses / experiments.
- `strain_stress_prediction.ipynb` – Main notebook for training and evaluating the surrogate.
- `strain_stress_prediction (1).ipynb` – Variant/backup of the main notebook.
- `stress-strain-prediction (2).pdf` – Slides/report summarizing the study.

`fea_database/`, `preprocessed/`, and `fea_model/` are part of the accompanying dataset folder (place them next to the notebooks when running the project).

## FE dataset (plate with a hole)

The FE database contains results from analyses of a 2D plate with a circular hole:

- Plate:
  - Width: 100 mm  
  - Height: 200 mm  
  - Thickness: 2 mm  
  - Hole diameter: 20 mm
- Loading:
  - Nodal forces applied in the vertical direction (y-direction) on the upper and bottom edges.
- Boundary conditions:
  - Symmetry along the horizontal symmetry line.
- Elements:
  - Linear quadrilateral elements (QUAD4).

### Cases

1. **Baseline**
   - Hole centred: 50 mm from the left edge.
   - Load: uniformly distributed along top/bottom edges.
   - Mesh: fine (936 elements, 1014 nodes).
   - 1000 simulations, loads from 70 N to 70 kN.

2. **Linear load**
   - Same geometry as baseline.
   - Load: non-uniform; linearly increasing from left to right (starting at zero).
   - 500 simulations, loads from 70 N to 70 kN.

3. **Off center 1**
   - Hole center: 40 mm from left edge.
   - Other settings: as baseline.
   - 500 simulations, loads from 70 N to 70 kN.

4. **Off center 2**
   - Hole center: 30 mm from left edge.
   - Other settings: as baseline.
   - 500 simulations, loads from 70 N to 70 kN.

5. **Off center 3**
   - Hole center: 20 mm from left edge.
   - Other settings: as baseline.
   - 500 simulations, loads from 70 N to 70 kN.

6. **Coarse mesh**
   - Same geometry/load as baseline.
   - Coarser mesh: 352 elements, 402 nodes.
   - 500 simulations, loads from 70 N to 70 kN.

## Data blocks: INPUT vs OUTPUT

Each FE result file has two blocks: `INPUT` and `OUTPUT`.

### INPUT block

Nodal loading:

- `X`, `Y` – coordinates of nodes where forces are applied (mm).
- `FX`, `FY` – force components in x- and y-directions (N).

This defines the load state used for that simulation.

### OUTPUT block

Nodal responses:

- `X`, `Y` – nodal coordinates (mm).
- `EPTOeqv` – equivalent total strain (mm/mm).
- `EPELeqv` – equivalent elastic strain (mm/mm).
- `EPPLeqv` – equivalent plastic strain (mm/mm).
- `Seqv` – equivalent von Mises stress (MPa).

These are the targets for the ML model.

## FE model & data generation

A reference FE model is provided in `fea_model/`:

- Built in Ansys Workbench 2022 R2 (openable in that or later versions).
- Loads are applied via APDL:
  - `ARG1` – total x-component of applied force (N).
  - `ARG2` – total y-component of applied force (N).
- The total forces are converted to line loads (N/mm) over the edges:
  - `ARG2` (y-force): positive on upper edge, negative on bottom edge (symmetric).
  - `ARG1` (x-force): positive on upper edge, negative on bottom edge (antisymmetric).

An APDL script under **Solution** writes results to:

- `fea_results.txt` (text format).
- Typical path: `.../dp0/SYS-#/MECH/fea_results.txt` where `# = 1, 2, 3, ...` is the internal system ID.

You can regenerate or extend the database by running additional load cases with this model.

## Key Methods & Model

At a high level, the surrogate learns a mapping of the form

\[
(X, Y, FX, FY, \text{case features}) \;\longrightarrow\; 
\big[\mathrm{EPTOeqv}, \mathrm{EPELeqv}, \mathrm{EPPLeqv}, \mathrm{Seqv}\big]
\]

- Inputs:
  - Node coordinates and applied forces; optionally case tags (baseline / linear load / off-center / coarse).
- Outputs:
  - Node-wise equivalent strains and stress from the FE analysis.
- Typical model:
  - Fully connected neural network / regression model.
  - Multi-output regression (all four quantities predicted jointly).
- Training:
  - Use `preprocess.py` to build a single consolidated dataset.
  - Split into train / validation / test (e.g. by cases or by simulations).
  - Train and evaluate in `strain_stress_prediction.ipynb`.

The focus is on:

- Generalization across **physics-related variations** (geometry, loading, mesh).
- Handling **imbalanced data** (many low-stress nodes vs few high-gradient nodes around the hole).
- Comparing different training strategies (plain MSE vs weighted losses, varying epochs, etc.).

## Results (quick look)

For quick insight:

- Open `strain_stress_prediction.ipynb` and:
  - Plot predicted vs FE `Seqv` and `EPTOeqv` across the plate.
  - Compare error distributions in high-stress vs low-stress regions.
- See `stress-strain-prediction (2).pdf` for:
  - Project motivation and setup.
  - Sample contour plots from FE vs ML.
  - Observations on generalization and limitations.

(Exact figures depend on the current state of the notebooks; re-run them to regenerate plots.)

## Future-Scope

- **Better training strategies**
  - Systematic hyperparameter tuning (learning rate, depth, width, regularization).
  - Sample weighting or resampling for underrepresented high-stress regions.
- **Richer model classes**
  - Graph/mesh-aware models (GNNs, message-passing on FE nodes/elements).
  - Physics-informed neural networks (PINNs) with equilibrium/compatibility regularization.
- **Extended datasets**
  - Additional load paths (biaxial, shear).
  - Different geometries (multiple holes, notches, fillets).
  - 3D extensions and elasto-plastic hardening laws.
- **Solver integration**
  - Use the trained surrogate as a fast proxy in optimization or uncertainty studies.

## About

The aim of this project is to figure out if a model can be learned to predict stresses and strains in a loaded structure and to see if the model can generalize in terms of variation in geometry, load distribution, and mesh density.

Suggestions, issues, or ideas for extensions are welcome via GitHub Issues.
