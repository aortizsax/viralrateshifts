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
conda create -n viralrateshifts python=3.9 pandas==1.4.2 matplotlib==3.5.1 numpy==1.21.5 scikit-learn dendropy==4.5.2
mv PATHTO/nextstrain_ncov_open_global_all-time_tree.nwk .
mv PATHTO/metadata.tsv .
```

### Run Analysis 

```bash
python3 viralrateshifts.py -diveregence-tree nextstrain_ncov_open_global_all-time_tree.nwk -metadata metadata.tsv
```

=======
### Prerequisites

If you wish to rerun this anaylsis please download the metadata from: 
https://nextstrain.org/ncov/open/global/6m
under the 'All sequences and metadata'


## Built with

* [![Dendropy][Dendropy.js]][Dendropy-url]
* [![Pandas][Pandas.js]][Pandas-url]
* [![matplotlib][matplotlib.js]][matplotlib-url]
* [![numpy][numpy.js]][numpy-url]
* [![sklearn][sklearn.js]][sklearn-url]
* [![piecewise_regression][piecewise_regression.js]][piecewise_regression-url]




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Dendropy.js]: https://dendropy.org/_static/dendropy_logo.png
[Dendropy-url]: https://nextjs.org/
[Pandas.js]: https://pandas.pydata.org/static/img/pandas_white.svg
[Pandas-url]: https://pandas.pydata.org/
[matplotlib.js]: https://matplotlib.org/_static/images/logo_dark.svg
[matplotlib-url]: https://matplotlib.org/
[numpy.js]: https://numpy.org/images/logo.svg
[numpy-url]: https://numpy.org/
[sklearn.js]: https://scikit-learn.org/stable/_static/scikit-learn-logo-small.png
[sklearn-url]: https://scikit-learn.org/stable/
[piecewise_regression.js]: https://numpy.org/images/logo.svg
[piecewise_regression-url]: https://numpy.org/
