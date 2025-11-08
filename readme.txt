# Elasto-Plastic Stress–Strain Prediction Using Machine Learning

The aim of this project is to investigate whether a machine learning model can be trained to predict stresses and strains in a loaded structure and to evaluate how well the model generalizes to variations in geometry, load distribution, and mesh density. :contentReference[oaicite:0]{index=0}

## Repository Structure

- `fea_database/` – Original finite element (FE) simulation results for a plate with a hole.
- `preprocessed/` – Preprocessed data generated using `preprocess.py`. This is the main dataset used for training and evaluating the ML models.
- `fea_model/` – The FE model used to generate the database (Ansys Workbench 2022 R2).
- `preprocess.py` – Script to convert raw FE output into a machine-learning-ready format. :contentReference[oaicite:1]{index=1}
- `Task_1 (2).ipynb`, `Task_2 (1).ipynb` – Notebooks for exploratory tasks and intermediate experiments.
- `strain_stress_prediction.ipynb` – Main notebook for training and evaluating stress–strain prediction models. :contentReference[oaicite:2]{index=2}
- `stress-strain-prediction (2).pdf` – Report/summary of the project (slides or written report).

> **Note:** Folder names such as `fea_database/`, `preprocessed/`, and `fea_model/` refer to the dataset package accompanying this repository.

---

## Finite Element Database

The `fea_database` folder contains FE results for a 2D plate with a circular hole under various loading and geometric configurations.

### Common Model Setup

The following settings are common to all cases:

- Plate dimensions:
  - Width: 100 mm  
  - Height: 200 mm  
  - Thickness: 2 mm  
  - Hole diameter: 20 mm
- Loading:
  - Nodal forces applied in the vertical (y) direction on the upper and bottom edges.
- Boundary conditions:
  - Symmetry boundary conditions along the horizontal symmetry line.
- Mesh:
  - Linear quadrilateral elements (QUAD4).

### Load and Geometry Cases

1. **Baseline**
   - Hole centered: 50 mm from the left edge.
   - Load: Uniformly distributed along the edge.
   - Mesh: Fine mesh (936 elements, 1014 nodes).
   - Simulations: 1000 FE analyses with applied loads ranging from 70 N to 70 kN.

2. **Linear Load**
   - Geometry: Same as Baseline.
   - Load: Non-uniform; linearly increasing from left to right (starting from zero).
   - Simulations: 500 FE analyses with applied loads from 70 N to 70 kN.

3. **Off-Center 1**
   - Hole center: 40 mm from the left edge.
   - Other settings: As in Baseline.
   - Simulations: 500 FE analyses (70 N to 70 kN).

4. **Off-Center 2**
   - Hole center: 30 mm from the left edge.
   - Other settings: As in Baseline.
   - Simulations: 500 FE analyses (70 N to 70 kN).

5. **Off-Center 3**
   - Hole center: 20 mm from the left edge.
   - Other settings: As in Baseline.
   - Simulations: 500 FE analyses (70 N to 70 kN).

6. **Coarse Mesh**
   - Geometry and loading: Same as Baseline.
   - Mesh: Coarser mesh (352 elements, 402 nodes).
   - Simulations: 500 FE analyses (70 N to 70 kN).

---

## Data Format

Each FE result file contains two blocks: `INPUT` and `OUTPUT`.

### INPUT Block

For each node where forces are applied:

- `X`, `Y` – Nodal coordinates (mm).
- `FX`, `FY` – Force components in the x and y directions (N).

This block describes the applied loading state for the simulation.

### OUTPUT Block

For each node in the FE model:

- `X`, `Y` – Nodal coordinates (mm).
- `EPTOeqv` – Equivalent total strain (mm/mm).
- `EPELeqv` – Equivalent elastic strain (mm/mm).
- `EPPLeqv` – Equivalent plastic strain (mm/mm).
- `Seqv` – Equivalent (von Mises) stress (MPa).

These quantities are the targets for the machine learning models.

---

## FE Model and Data Generation

An FE model is provided in the `fea_model` folder for generating additional data:

- Software: Ansys Workbench 2022 R2 (or later).
- Loading is applied using an APDL script:
  - `ARG1` – x-component of the total applied force (N).
  - `ARG2` – y-component of the total applied force (N).
- The total applied force is interpreted as the line integral over the edge, and is internally converted to a line load (N/mm).
- Application of loads:
  - `ARG2` (y-force) is applied:
    - Positive on the upper edge.
    - Negative on the bottom edge (symmetric loading).
  - `ARG1` (x-force) is applied:
    - Positive on the upper edge.
    - Negative on the bottom edge (antisymmetric loading).

An APDL script under the **Solution** branch writes the FE results to a file:

- Output file name: `fea_results.txt`
- Typical file path:  
  `.../dp0/SYS-#/MECH/fea_results.txt`  
  where `# = 1, 2, 3, ...` is the internal system index within Ansys.

---

## Preprocessing

Use `preprocess.py` to convert raw FE output files into preprocessed datasets suitable for ML:

```bash
python preprocess.py
