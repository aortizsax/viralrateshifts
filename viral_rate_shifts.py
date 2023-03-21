#! /usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
## Copyright (c) 2023 Adrian Ortiz-Velez.
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
##
##     * Redistributions of source code must retain the above copyright
##       notice, this list of conditions and the following disclaimer.
##     * Redistributions in binary form must reproduce the above copyright
##       notice, this list of conditions and the following disclaimer in the
##       documentation and/or other materials provided with the distribution.
##     * The names of its contributors may not be used to endorse or promote
##       products derived from this software without specific prior written
##       permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
## ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
## DISCLAIMED. IN NO EVENT SHALL ADRIAN ORTIZ-VELEZ BE LIABLE FOR ANY DIRECT,
## INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
## BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
## OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
##############################################################################


#import packages
import argparse
import dendropy
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from sklearn.linear_model import LinearRegression
import piecewise_regression
np.random.seed(1380649)


def datetime_to_float(d):
    return d.timestamp()

def main():
    parser = argparse.ArgumentParser(description=None)

    parser.add_argument(
        "-t",
        "--divergence-tree",
        action="store",
        default="FILE",
        help="Divergence tree from Nextstrain [default=%(default)s].",
    )
    parser.add_argument(
        "-m",
        "--metadata",
        action="store",
        default="FILE",
        help="Metadata from Nextstrain [default=%(default)s].",
    )
    parser.add_argument(
        "-N",
        "--n-boot",
        action="store",
        default="200",
        help="Number of bootstrap replicates for piecewise analysis[default=%(default)s].",
    )
    parser.add_argument(
        "-M",
        "--max-breakpoints",
        action="store",
        default="6",
        help="Max breakpoints [default=%(default)s].",
    )
    
    parser.add_argument(
        "-o",
        "--output-prefix",
        action="store",
        default="output",
        help="Prefix for output files [default=%(default)s].",
    )
    
    args = parser.parse_args()
    
    tree_file = args.divergence_tree
    metadata_file = args.metadata
    pw_n_boot = int(args.n_boot)
    pw_max_breakpoints = int(args.max_breakpoints)
    
    print("Reading tree")
    
    tree = dendropy.Tree.get(
                            path=tree_file,
                            schema="newick",
                            )
    pdm = tree.phylogenetic_distance_matrix()
    
    print("Parsing metadata")
    
    metadata = pd.read_csv('11-02_bmetadata.tsv','\t', low_memory=False)
    
    print("Done parsing data files.")
    
    metadata.index = metadata['strain']

    #dist every taxa to Wuhan-Hu-1/2019
    taxa1 = tree.taxon_namespace[0]
    #Keys: taxa, Values: divergence tree dist to roo
    divergence_dict = {}
    #Keys: taxa, Values: dates from meta data
    date_dict = {}

    #get data
    for taxa in tree.taxon_namespace[1:]:
        taxa.label=taxa.label.replace(' ','_')
        divergence_dict[taxa.label] = pdm.distance(taxa1,taxa)
        date_dict[taxa.label] = metadata['date'][taxa.label]


    #change date to python format and plot
    dates = [pd.to_datetime(d) for d in date_dict.values()]
    divergence = [d for d in divergence_dict.values()]
    taxa = [d for d in divergence_dict.keys()]
    plt.scatter(dates,divergence)
    plt.show()

    
    adj = 2.850029e-8
    
    dates = [(datetime_to_float(d)-datetime_to_float(dates[0]))*adj for d in dates]
    plt.scatter(dates,divergence)
    plt.show()


        
    #Rerun linear analysis from Nextstrain
    x = np.array(dates).reshape((-1, 1))
    y = np.array(divergence)
    model = LinearRegression()
    model.fit(x, y)
    r_sq = model.score(x, y)
    print("Re-do Nextstrain Linear Analysis")
    print(f"coefficient of determination: {r_sq}")
    #plt.scatter(x,y)
    #plt.show()

    new_model = LinearRegression().fit(x, y.reshape((-1, 1)))
    print(f"intercept: {new_model.intercept_}")


    print(f"slope: {new_model.coef_}")
    
    
    #set x array as dates 
    x = np.array(dates)
    
    #Scan increasing number of breakpoints and score
    ms = piecewise_regression.ModelSelection(x, y,
                                            max_breakpoints=pw_max_breakpoints, 
                                            n_boot = pw_n_boot)

    var = input("Please enter the model you like to analyze further (model number or ALL to choose Biologically simple model): ")
    print("You entered: " + var)

    if var.isnumeric():
        var = int(var)
        print('Analyzing',var,'number of breakpoints')
        #Fit selected model
        pw_fit = piecewise_regression.Fit(x, y, n_breakpoints=var,n_boot=25)
        print(pw_fit.summary()[0])
        
        # Plot the data, fit, breakpoints and confidence intervals
        pw_fit.plot_data(color="grey", s=20)
        # Pass in standard matplotlib keywords to control any of the plots
        pw_fit.plot_fit(color="red", linewidth=2)
        pw_fit.plot_breakpoints()
        pw_fit.plot_breakpoint_confidence_intervals()
        plt.xlabel("Years since start")
        plt.ylabel("Divergence")
        plt.show()
        plt.close()
        
    else:
        print("Analyzing all for user")
        for i in range(pw_max_breakpoints):
            i+=1#fix python index 
            #Fit selected model
            pw_fit = piecewise_regression.Fit(x, y, n_breakpoints=i,n_boot=25)
            print(pw_fit.summary()[0])
            
            # Plot the data, fit, breakpoints and confidence intervals
            pw_fit.plot_data(color="grey", s=20)
            # Pass in standard matplotlib keywords to control any of the plots
            pw_fit.plot_fit(color="red", linewidth=2)
            pw_fit.plot_breakpoints()
            pw_fit.plot_breakpoint_confidence_intervals()
            plt.xlabel("Years since start")
            plt.ylabel("Divergence")
            plt.show()
            plt.close()
        

if __name__ == "__main__":
    main()
