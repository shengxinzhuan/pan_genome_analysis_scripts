# pan_genome_analysis_scripts
This repository serves the purpose of documenting some statistical and plotting scripts used for pan-genome analysis, with updates made on an irregular basis.
Currently, the updated scripts have been mostly completed with the assistance of ChatGLM4.
# Ⅰpan and core gene family analysis
The initial analysis file within this folder is the Orthogroups.GeneCount.tsv obtained from running Orthofinder. All subsequent analyses are based on this file. Of course, if you also organize TEs, SNPs, InDels, SVs, etc., into a similar format, you can use the scripts provided in this folder for statistical analysis and plotting.
## 01. File preprocessing
You can directly use the Orthogroups.GeneCount.tsv file as is (there is no need to delete the ‘Total’ row at the end, as the script has already handled it).<br>
In this script, I have set five standards: core, near-core, pan, private, and undefined. <br>
The 'core' indicates that all genomes contain this orthogroup. <br>
'near-core' is set to a range greater than 70% but not all species.<br>
'pan' refers to two or more species having the orthogroup but less than 70%.<br>
'private' means only one species has it. <br>
'undefined' is when no species has the orthogroup (because some people may test with partial species information, this type is included to ensure the script runs normally).<br>
As you can see, the first script will remove the last line of the input file, then perform the statistics, and output the gene family type for each line.
```
python 01_orthogroups_counts.py Orthogroups.GeneCount.tsv orthogroups.pan.tsv

output file:
Orthogroup      A       B       C       D       E       F       G       H       type
OG0000000       54      35      31      3       39      46      48      49      core
OG0000001       0       2       414     0       0       0       0       0       pan
OG0000002       40      46      37      15      17      71      30      53      core
OG0000003       35      28      29      21      39      20      30      20      core
OG0000004       0       0       0       3       37      0       0       0       pan
OG0000005       41      0       41      1       22      28      19      37      near-core
OG0000006       36      11      39      6       24      59      41      59      core
OG0000007       58      40      37      7       46      11      12      14      core
OG0000008       39      53      8       0       8       40      36      43      near-core
OG0000009       21      21      30      20      7       40      36      49      core
OG0000010       28      3       30      0       20      54      63      47      near-core
OG0000011       30      27      31      2       17      48      32      38      core
```
The second script functions similarly to the first one, but the output file is sorted and the values are replaced, where '1' represents the presence of the gene family and '-1' indicates the absence of the gene family.<br>
It is important to note that a gene family is not the same as a gene. <br>
If you need to view each orthologous gene, you would use the collinearity summary results to obtain a gene table for all species, and then compile it into a similar table for use.<br>
```
python 02_ortho_count_pav.sort.py Orthogroups.GeneCount.tsv orthogroups.pav.tsv

output file:
Orthogroup      A       B       C       D       E       F       G       H       type
OG0000000       1       1       1       1       1       1       1       1       core
OG0006858       1       1       1       1       1       1       1       1       core
OG0006859       1       1       1       1       1       1       1       1       core
OG0006860       1       1       1       1       1       1       1       1       core
OG0006861       1       1       1       1       1       1       1       1       core
OG0006862       1       1       1       1       1       1       1       1       core
OG0006864       1       1       1       1       1       1       1       1       core
OG0006857       1       1       1       1       1       1       1       1       core
OG0006865       1       1       1       1       1       1       1       1       core
OG0006867       1       1       1       1       1       1       1       1       core
OG0006868       1       1       1       1       1       1       1       1       core
OG0006869       1       1       1       1       1       1       1       1       core
OG0006870       1       1       1       1       1       1       1       1       core
OG0006871       1       1       1       1       1       1       1       1       core
OG0006872       1       1       1       1       1       1       1       1       core
OG0006866       1       1       1       1       1       1       1       1       core
OG0006855       1       1       1       1       1       1       1       1       core
OG0006854       1       1       1       1       1       1       1       1       core
OG0006853       1       1       1       1       1       1       1       1       core
OG0006835       1       1       1       1       1       1       1       1       core
```
The third script's purpose is to convert the TSV file obtained from the second script into a heatmap, which is commonly referred to as PAV in articles. Red represents presence, while blue indicates absence.<br>
The sorting is done in the order of core-private.
```
python 03_heatmap_pan_core.py orthogroups.pav.tsv
```
![heatmap_demo]()
