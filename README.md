To use this repo in 2025, use 
`mamba env create -f env.yaml` (tested on mac m2)

Based on https://github.com/chemprop/chemprop

# Property Prediction
This repository contains message passing neural networks for Abraham solute parameters (SoluteML), solvation free 
energy and solvation enthalpy (DirectML) prediction.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  * [Option 1: Conda](#option-1-conda)
  * [Option 2: Installing from source](#option-2-installing-from-source)
  * [Notes](#notes)
- [Sample Code](#sample-code)
- [Web Interface](#web-interface)
- [How to Cite](#how-to-cite)
- [License Information](#license-information)
- [Data](#data)
- [Training](#training)
  * [Train/Validation/Test Splits](#train-validation-test-splits)
  * [Cross validation](#cross-validation)
  * [Ensembling](#ensembling)
  * [Hyperparameter Optimization](#hyperparameter-optimization)
  * [Additional Features](#additional-features)
    * [RDKit 2D Features](#rdkit-2d-features)
    * [Custom Features](#custom-features)
- [Predicting](#predicting)
- [TensorBoard](#tensorboard)
- [Results](#results)
- [Adjustments for solvation / dual molecular representation](#adjustments-for-solvation--dual-molecular-representation)

## Requirements

While it is possible to run all of the code on a CPU-only machine, GPUs make training significantly faster. To run with GPUs, you will need:
 * cuda >= 8.0
 * cuDNN

Chemprop_solvation supports Windows, Mac, and Linux OS.

## Installation

Chemprop_solvation can be installed either via conda or from source (i.e., directly from this git repo).

**Both options require conda, so first install Miniconda from [https://conda.io/miniconda.html](https://conda.io/miniconda.html).**

Follow the instruction by typing the shaded code block on a command prompt / terminal.

### Option 1: Conda

The easiest way to install the `chemprop_solvation` dependencies is to install as a conda package. Here are the steps
to follow on the command line:

1. `conda create -n chemprop_solvation` (create a new conda environment)
2. `conda activate chemprop_solvation` (activate the conda environment)
3. `conda install -c fhvermei -c conda-forge chemprop_solvation` (install the package)
4. `conda install -c anaconda git`  (install git if it is not installed)
5. `pip install git+https://github.com/bp-kelley/descriptastorus` (install a required dependency)

### Option 2: Installing from source

1. `conda install -c anaconda git`  (install git if it is not installed)
2. `git clone https://github.com/fhvermei/chemprop_solvation.git`  (clone a repository)
3. `cd chemprop_solvation` (go to a directory to which the git repository is cloned)
4. `conda env create -f environment.yml` (create a new conda environment)
5. `conda activate chemprop_solvation` (activate the conda environment)
6. `pip install git+https://github.com/bp-kelley/descriptastorus` (install a required dependency)
7. `pip install -e .` (install the chemprop_solvation project in editable mode)
8. Download the machine learning model files ("ML_model_files.zip") from [here](https://zenodo.org/record/5792296) and extract it.
9. Copy the "SoluteML", "DirectML_Gsolv", and "DirectML_Hsolv" folders from the extracted "ML_model_files" folder and place them under `chemprop_solvation/chemprop_solvation/final_models/`.


### Notes

If you get warning messages about `kyotocabinet` not being installed, it's safe to ignore them.


## Sample Code

Sample python code is located at `chemprop_solvation/examples/sample_ML_estimator_calc.py`.

Sample jupyter notebook is also available at `chemprop_solvation/examples/sample_jupyter_notebook_ML_estimator_calc.ipynb`.
To open the jupyter notebook:
1. `conda activate chemprop_solvation` (activate the conda environment)
2. `pip install notebook` (install a jupyter notebook)
3. `jupyter notebook` (jupyter notebook interface will appear in a new browser window )

## Web Interface
A user-friendly online webtool is available on [here](https://rmg.mit.edu/database/solvation/search/).

## How to Cite
If you use this software for research, please cite our work as follows:

Chung, Y.; Vermeire, F. H.; Wu, H.; Walker, P. J.; Abraham, M. H.; Green, W. H. Group contribution and
machine learning approaches to predict Abraham solute parameters, solvation free energy, and solvation enthalpy.
<i>J. Chem. Inf. Model.</i> 2022. 62, 3, 433-446. doi: 10.1021/acs.jcim.1c01103. [Link](https://pubs.acs.org/doi/10.1021/acs.jcim.1c01103)

The preprint of our manuscript is also available at [10.33774/chemrxiv-2021-djd3d-v2](https://chemrxiv.org/engage/chemrxiv/article-details/613b96efac321950af77ae13)

## License Information
Chemprop_solvation is a free, open-source software package distributed under the 
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode).

## Data

In order to train a model, you must provide training data containing molecules (as SMILES strings) and known target values. Targets can either be real numbers, if performing regression, or binary (i.e. 0s and 1s), if performing classification. Target values which are unknown can be left as blanks.

Our model can either train on a single target ("single tasking") or on multiple targets simultaneously ("multi-tasking").

The data file must be be a **CSV file with a header row**. For example:
```
smiles,NR-AR,NR-AR-LBD,NR-AhR,NR-Aromatase,NR-ER,NR-ER-LBD,NR-PPAR-gamma,SR-ARE,SR-ATAD5,SR-HSE,SR-MMP,SR-p53
CCOc1ccc2nc(S(N)(=O)=O)sc2c1,0,0,1,,,0,0,1,0,0,0,0
CCN1C(=O)NC(c2ccccc2)C1=O,0,0,0,0,0,0,0,,0,,0,0
...
```
Datasets from [MoleculeNet](http://moleculenet.ai/) and a 450K subset of ChEMBL from [http://www.bioinf.jku.at/research/lsc/index.html](http://www.bioinf.jku.at/research/lsc/index.html) have been preprocessed and are available in `data.tar.gz`. To uncompress them, run `tar xvzf data.tar.gz`.

## Training

To train a model, run:
```
python train.py --data_path <path> --dataset_type <type> --save_dir <dir>
```
where `<path>` is the path to a CSV file containing a dataset, `<type>` is either "classification" or "regression" depending on the type of the dataset, and `<dir>` is the directory where model checkpoints will be saved.

For example:
```
python train.py --data_path data/tox21.csv --dataset_type classification --save_dir tox21_checkpoints
```

Notes:
* The default metric for classification is AUC and the default metric for regression is RMSE. Other metrics may be specified with `--metric <metric>`.
* `--save_dir` may be left out if you don't want to save model checkpoints.
* `--quiet` can be added to reduce the amount of debugging information printed to the console. Both a quiet and verbose version of the logs are saved in the `save_dir`.

### Train/Validation/Test Splits

Our code supports several methods of splitting data into train, validation, and test sets.

**Random:** By default, the data will be split randomly into train, validation, and test sets.

**Scaffold:** Alternatively, the data can be split by molecular scaffold so that the same scaffold never appears in more than one split. This can be specified by adding `--split_type scaffold_balanced`.

**Separate val/test:** If you have separate data files you would like to use as the validation or test set, you can specify them with `--separate_val_path <val_path>` and/or `--separate_test_path <test_path>`.

Note: By default, both random and scaffold split the data into 80% train, 10% validation, and 10% test. This can be changed with `--split_sizes <train_frac> <val_frac> <test_frac>`. For example, the default setting is `--split_sizes 0.8 0.1 0.1`. Both also involve a random component and can be seeded with `--seed <seed>`. The default setting is `--seed 0`.

### Cross validation

k-fold cross-validation can be run by specifying `--num_folds <k>`. The default is `--num_folds 1`.

### Ensembling

To train an ensemble, specify the number of models in the ensemble with `--ensemble_size <n>`. The default is `--ensemble_size 1`.

### Hyperparameter Optimization

Although the default message passing architecture works quite well on a variety of datasets, optimizing the hyperparameters for a particular dataset often leads to marked improvement in predictive performance. We have automated hyperparameter optimization via Bayesian optimization (using the [hyperopt](https://github.com/hyperopt/hyperopt) package) in `hyperparameter_optimization.py`. This script finds the optimal hidden size, depth, dropout, and number of feed-forward layers for our model. Optimization can be run as follows:
```
python hyperparameter_optimization.py --data_path <data_path> --dataset_type <type> --num_iters <n> --config_save_path <config_path>
```
where `<n>` is the number of hyperparameter settings to try and `<config_path>` is the path to a `.json` file where the optimal hyperparameters will be saved. Once hyperparameter optimization is complete, the optimal hyperparameters can be applied during training by specifying the config path as follows:
```
python train.py --data_path <data_path> --dataset_type <type> --config_path <config_path>
```

### Additional Features

While the model works very well on its own, especially after hyperparameter optimization, we have seen that adding computed molecule-level features can further improve performance on certain datasets. Features can be added to the model using the `--features_generator <generator>` flag.

#### RDKit 2D Features

As a starting point, we recommend using pre-normalized RDKit features by using the `--features_generator rdkit_2d_normalized --no_features_scaling` flags. In general, we recommend NOT using the `--no_features_scaling` flag (i.e. allow the code to automatically perform feature scaling), but in the case of `rdkit_2d_normalized`, those features have been pre-normalized and don't require further scaling.

Note: In order to use the `rdkit_2d_normalized` features, you must have `descriptastorus` installed. If you installed via conda, you can install `descriptastorus` by running `pip install git+https://github.com/bp-kelley/descriptastorus`. If you installed via Docker, `descriptastorus` should already be installed.

The full list of available features for `--feagrtures_generator` is as follows. 

`morgan` is binary Morgan fingerprints, radius 2 and 2048 bits.
`morgan_count` is count-based Morgan, radius 2 and 2048 bits.
`rdkit_2d` is an unnormalized version of 200 assorted rdkit descriptors. Full list can be found at the bottom of our paper: https://arxiv.org/pdf/1904.01561.pdf
`rdkit_2d_normalized` is the CDF-normalized version of the 200 rdkit descriptors.

#### Custom Features

If you would like to load custom features, you can do so in two ways:

1. **Generate features:** If you want to generate features in code, you can write a custom features generator function in `chemprop/features/features_generators.py`. Scroll down to the bottom of that file to see a features generator code template.
2. **Load features:** If you have features saved as a numpy `.npy` file or as a `.csv` file, you can load the features by using `--features_path /path/to/features`. Note that the features must be in the same order as the SMILES strings in your data file. Also note that `.csv` files must have a header row and the features should be comma-separated with one line per molecule.
 
## Predicting

To load a trained model and make predictions, run `predict.py` and specify:
* `--test_path <path>` Path to the data to predict on.
* A checkpoint by using either:
  * `--checkpoint_dir <dir>` Directory where the model checkpoint(s) are saved (i.e. `--save_dir` during training). This will walk the directory, load all `.pt` files it finds, and treat the models as an ensemble.
  * `--checkpoint_path <path>` Path to a model checkpoint file (`.pt` file).
* `--preds_path` Path where a CSV file containing the predictions will be saved.

For example:
```
python predict.py --test_path data/tox21.csv --checkpoint_dir tox21_checkpoints --preds_path tox21_preds.csv
```
or
```
python predict.py --test_path data/tox21.csv --checkpoint_path tox21_checkpoints/fold_0/model_0/model.pt --preds_path tox21_preds.csv
```

## TensorBoard

During training, TensorBoard logs are automatically saved to the same directory as the model checkpoints. To view TensorBoard logs, run `tensorboard --logdir=<dir>` where `<dir>` is the path to the checkpoint directory. Then navigate to [http://localhost:6006](http://localhost:6006).

## Results

We compared our model against MolNet by Wu et al. on all of the MolNet datasets for which we could reproduce their splits (all but Bace, Toxcast, and qm7). When there was only one fold provided (scaffold split for BBBP and HIV), we ran our model multiple times and reported average performance. In each case we optimize hyperparameters on separate folds, use rdkit_2d_normalized features when useful, and compare to the best-performing model in MolNet as reported by Wu et al. We did not ensemble our model in these results.

Results on classification datasets (AUC score, the higher the better)

| Dataset | Size |	Ours |	MolNet Best Model |
| :---: | :---: | :---: | :---: |
| BBBP | 2,039 | 0.735 ± 0.0064	| 0.729 |
| Tox21 | 7,831 | 0.855 ± 0.0052	| 0.829 ± 0.006 |
| Sider | 1,427 |	0.678 ± 0.019	| 0.648 ± 0.009 |
| clintox | 1,478 | 0.9 ± 0.0089	| 0.832 ± 0.037 |
| MUV | 93,087 | 0.0897 ± 0.015 | 0.184 ± 0.02 |
| HIV | 41,127 |	0.793 ± 0.0012 |	0.792 |
| PCBA | 437,928 | 0.397 ± .00075 | 	0.136 ± 0.004 | 

Results on regression datasets (score, the lower the better)

Dataset | Size | Ours | GraphConv/MPNN (deepchem) |
| :---: | :---: | :---: | :---: |
delaney	| 1,128 | 0.567 ± 0.026 | 0.58 ± 0.03 |
Freesolv | 642 |	1.11 ± 0.035 | 1.15 ± 0.12 |
Lipo | 4,200 |	0.542 ± 0.02 |	0.655 ± 0.036 |
qm8 | 21,786 |	0.0082 ± 0.00019 | 0.0143 ± 0.0011 |
qm9 | 133,884 |	2.03 ± 0.021	| 2.4 ± 1.1 |

Lastly, you can find the code to our original repo at https://github.com/wengong-jin/chemprop and for the Mayr et al. baseline at https://github.com/yangkevin2/lsc_experiments . 

## Adjustments for solvation / dual molecular representation
The atom, bond and molecular features used by default are different from those used in standard chemprop. They are adjusted to include more solvation specific featurization. Retraining a model on old data will give other results compared to the original version of chemprop.
The keyword `--solvation` triggers the reading of 2 molecules from the csv file (the first two columns of the csv file), while the targets are given starting from the third column.

Compared to the previous version of chemprop you can now also use InChI molecular identifiers instead of SMILES. `--detailed_results` will make some plots for you and give csv files with predicted values.

