# pan_genome_analysis_scripts
This repository serves the purpose of documenting some statistical and plotting scripts used for pan-genome analysis, with updates made on an irregular basis.
Currently, the updated scripts have been mostly completed with the assistance of ChatGLM4.
# Ⅰpan and core gene family analysis (in Scripts_for_OrthoFinder_Result)
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
By the way, it will also generate a pieplot for statistic result of gene family 
The sorting is done in the order of core-private.
```
python 03_heatmap_pan_core.py orthogroups.pav.tsv
```
![heatmap_demo](https://github.com/shengxinzhuan/pan_genome_analysis_scripts/blob/main/1734604774771.jpg)<br>
![piplot_demo](https://github.com/shengxinzhuan/pan_genome_analysis_scripts/blob/main/pieplot_pan_core.png)<br>

The fourth script will count the number of pan and core gene families obtained from each combination, ranging from pairwise to all-species pairings.<br>
'Core' refers to gene families that are present in all paired species, while 'pan' refers to gene families that are not shared by all.
```
python 04_boxplot_pan_core.py orthogroups.pav.tsv

outputfile:
A_B_pan:3345
A_B_core: 1234
A_C_pan:6543
A_C_core: 1346
......
A_B_C_D_E_F_pan: 34567
A_B_C_D_E_F_core: 2678
```
![boxplot_demo](https://github.com/shengxinzhuan/pan_genome_analysis_scripts/blob/main/box_plot_pan_core.png) <br>

The fifth script serves a similar purpose to the fourth one, but its function is to count the specific quantities.<br>
Therefore, it is designed to work with the pan.tsv file produced by the first script.
```
python 05_box_plot_pan_core.gene_num.py orthogroups.pan.tsv
```
![boxplot_demo](https://github.com/shengxinzhuan/pan_genome_analysis_scripts/blob/main/boxplot_pan_core.gene_num.png)

# II VCF convert (in Scripts_for_VCF_file)
This series of scripts is for converting VCF files to facilitate some subsequent analysis
## 01. The format conversion of InDels' VCF file
It is well known that many population genetics software can only analyze biallelic SNPs, whereas in plants, InDels and large-scale structural variations (SVs) constitute a significant proportion and are more likely to impact the traits of species. <br>
Therefore, a script is provided here to convert the format of InDels (i.e., insertions and deletions less than 50bp in size) so that they can be used with software designed for SNPs for downstream analysis (such as PCA, Structure, NJ tree, etc.). <br>
Unlike conventional scripts that only perform A/T substitutions, this script sets up several types of substitutions:<br>
for insertions, it's an A/T type substitution (with insertions less than 10bp being A->T and those greater than 10bp being T->A),<br>
and for deletions, it's a G/C type substitution (with deletions less than 10bp being G->C and those greater than 10bp being C->G).<br> 
This setup is designed to facilitate rough homology comparisons. <br> 
When running this script, it will generate a processed file named sample_processed.vcf from the input sample.vcf, and it will also record the specific position, base, and type of the substitution to facilitate the use of subsequent researchers. <br>
Note that this script only processes Indel sequences less than 50bp in length and handles bi-allelic sites only (it is recommended to filter in advance using bcftools); <br>
if the VCF file contains sequences larger than 50bp or SNPs, they will be automatically filtered out;<br>
for tri-allelic sites, although there will be no error, they will be retained, but they may not be fully compatible with other scripts in subsequent analyses.
```
python 01_indel_replace.py input.vcf > replace.log

output log
chr1    931  TTT     T       G/C
chr1    9510  TATT    T       G/C
chr1    95208  GTCAGGTAACGGGGTTTGGG    G       C/G
chr1    902761  CCC     C       G/C
chr1    914948  AAACTCGATACT    A       C/G
chr1    934964  CACAAA  C       G/C
chr1    945000  AAACACATTAT     A       C/G
chr1    955154  AAA     A       G/C
chr1    955166  ACTTTTTGCCAAAAAAATGATT  A       C/G
chr1    955182  ATGATTCTTTTTAG  A       C/G
```
## 02. Convert vcf to tsv format
This script will perform a format conversion on the allele information in the VCF file, with the following specific rules: <br>
if there is a missing allele (./.), the site will be recorded as NaN; if an allele is present, it will be directly recorded as (1/1, 1|1, 0/1, 1|0, 0/0, 0|0), and finally converted into a TSV format. <br>
Sometimes, the absence of a site can also be a phylogenetic signal and should not be simply filtered out, especially in multi-species comparisons where the actual genetic distance might be underestimated. <br>
Converting it into a matrix signal and using some clustering algorithms may better reflect the true species differences. <br>
```
python 02_convert_vcf_tsv.py input.vcf > output.tsv

ouput tsv
chr_pos  A  B  C  D  E
Chr1_2  Nan  Nan  1|1  0|0  1|1
Chr1_5  1|1  Nan  1|1  Nan  1|0
Chr1_60  0|0  0|0  Nan  1|1  0|1
```
## 03. Convert genotype to haplotype format
This script converts the TSV file obtained from the previous script into a haplotype count format, with the following specific rules:<br>
if the type is NaN, it is recorded as -1; <br>
if it is 0/0 or 0|0, it is recorded as 0;<br>
for heterozygotes, i.e., 0/1, 0|1, 1|0, it is recorded as 0.5; <br>
and if it is 1/1 or 1|1, it is recorded as 1.<br>
The results converted with this script can be directly imported into Tbtools or Excel for haplotype drawing.
```
python 03_convert_haplotype.py input.tsv > output.haplotype.tsv

output haplotype
chr_pos  A  B  C  D  E
Chr1_2  -1  -1  1  0  1
Chr1_5  1  -1  1  0  0.5
Chr1_60  0  0  -1  1  0.5
```

## 04. Convert haplotye to pan and core statistic result
This script can convert the results from the previous script into a format similar to that obtained from counting Orthogroups, such as core, near-core, pan, and private, and the visualization script can be directly reused to visualize the results.<br>
core:100%<br>
near-core: 100% > x >= 70%<br>
pan: 70% > x > 1 sample <br>
private: only 1 sample <br>
loss: nothing
```
python 04_convert_haplotype_pan_core.py input.haplotype.tsv output.pav.tsv

output pav
chr_pos A  B  C  D  E  type
chrN_1  1  1  1  1  1  core
chrN_2  1  -1  1  1  1  near-core
chrN_3  1  -1  -1  -1  1  pan
chrN_4  1  -1  -1  -1  -1  private
chrN_5  -1  -1  -1  -1  -1  loss
```
