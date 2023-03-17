# viralrateshifts

Python scripts and instruction to collect metadata information and Sample SARS-CoV-2 divergence data used in the open analysis to reanalyze the mutatation rate analyis using peicewise linear analysis.

## *** version
The scripts in this repo parse and manipulate data (metadata and diveregence data) downloaded form Nextstrain's open ____ and reanalyze the mutation rate analysis. To run you need:

FLOWCHART

### Collect data
First collect the data. Go to the latest global analysis provided by Nextstrain https://nextstrain.org/ncov/open/global/all-time), expand the window or click the menu bottom in the top right of the page and under 'Tree Options'&'Branch Length' click 'Clock'. Next, scroll to the bottom of the page, select 'DOWNLOAD DATA' and then 'TREE (NEWICK)'.  You will get a file named: nextstrain_ncov_open_global_all-time_tree.nwk . Finally, scroll to the bottom of the page, find 'ALL SEQUENCES AND METADATA'. Decompress this in the directory. You will get a file named: metadata.tsv. 

### install locally
```bash
gh repo clone aortizsax/viralrateshifts
```

```bash
cd viralrateshifts
```

```bash
conda create -n viralrateshifts python=3.9 pandas matplotlib numpy scikit-learn mv PATHTO/nextstrain_ncov_open_global_all-time_tree.nwk . 
mv PATHTO/metadata metadata.tsv .
```

### Run Analysis 

```bash
python3 viralrateshifts.py -diveregence-tree nextstrain_ncov_open_global_all-time_tree.nwk -metadata metadata.tsv
```



