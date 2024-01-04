# WFCC
Code for the algorithm Weight-Filtration Comparison Curve (WFCC) to compare weighted graphs with equal labelled vertices and edges, but different weightings. The algorithm takes as inputs the transition matrices, and outputs a curve visualising the number of non-common edges over an edge-filtration. 

## Description of files
The WFCC algorithm and auxiliary code are found in `main_Functions.py`. An example of how to use the algorithm is in `Example_WFCC.ipynb`.
The synthetic hypercubes we considered, with probability and flux weightings, are obtained in `diff-cubes.R`. The file `main.ipynb` contains the code explained, and it reproduces all the figures and computations in the main text of the paper, except for the MDS. The MDS are produced in `mds.R`. 

The folder `Data_files_hypercubes` contains all the data files needed. `Klebsiella_clinical_data` is the original real data to run HyperHMM. `Klebsiella` is the folder with the HyperHMM outputs of the continents. `Klebsiella_subsampled` contains the HyperHMM outputs from subsampled clinical data. `Synthetic_data_to_run_HMM_TraPS` contains the synthetic data mimicking clinical data, to be run on HyperHMM and HyperTraPS, and the corresponding outputs are found in `results_synthetic_data` for HyperHMM and `hypertrapsTransMatrices` for HyperTraPS. `Synthetic_data_all_zeros_to_run_HMM_TraPS` is synthetic data mimicking clinical where all samples are the string of all zeros, to be run on HyperHMM and HyperTraPS, and the corresponding outputs are `Hyperhmm_sample_zero` and `Hypertraps_sample_zero`. Lastly, `Outputs_github` is an empty folder to direct there the plots in png form and the data files in csv form that are generated in the Jupyter Notebook.

HyperTraPS was run using https://github.com/StochasticBiology/hypertraps-simple.

### References 
The clinical data in `Klebsiella_clinical_data` was obtained from the following publications:
1.
