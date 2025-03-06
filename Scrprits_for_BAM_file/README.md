# PAV in linear reference genome by bam
This series of scripts is to process the gff file with bam file, and ultimately get the coverage of each CDS inside the bam file, as well as the possible gains and losses of each mRNA
## 01 Genrate a bed file for MOSdepth
The script generates a bed file for mosdepth to use as an input file for depth-of-coverage statistics.
```
python 01_gff_to_cds.py input.gff3 > generate.log
```
The input file is in the conventional gff format, and the principle is to extract the ‘CDS’ characters in the third column by trying to identify them.<br>
The output name : all_cds.bed <br>
The input and output file formats are as follows: <br>
```
# input_gff:

LG01A   maker   gene    8487    9108    .       -       .       ID=XX01AG000001
LG01A   maker   mRNA    8487    9108    .       -       .       ID=XX01AG000001.mRNA1;Parent=XX01AG000001
LG01A   maker   CDS     8487    8519    .       -       0       ID=XX01AG000001.cds1;Parent=XX01AG000001.mRNA1
LG01A   maker   exon    8487    8519    .       -       .       ID=XX01AG000001.exon1;Parent=XX01AG000001.mRNA1
LG01A   maker   CDS     8905    9108    .       -       0       ID=XX01AG000001.cds2;Parent=XX01AG000001.mRNA1
LG01A   maker   exon    8905    9108    .       -       .       ID=XX01AG000001.exon2;Parent=XX01AG000001.mRNA1

# output_bed:

LG01A   CDS     8487    8519   XX01AG000001.mRNA1_CDS1
LG01A   CDS     8905    9108   XX01AG000001.mRNA1_CDS2

```
## 02 Calculation of CDS coverage depth using MOSdepth
If you haven't installed mosdepth yet, you can do a quick install with conda<br>
```
mosdepth -t 8 --by all_cds.bed output_prefix input.bam
```
The output_prefix.region.bed.gz file is what we need for the next step.
The file formats are as follows:<br>
```
LG01A   CDS     8487    8519   XX01AG000001.mRNA1_CDS1   25.3
LG01A   CDS     8905    9108   XX01AG000001.mRNA1_CDS2   24.2
......
```
## 03 Determining whether CDS is missing using a decision threshold and depth information
The script takes a gff file with region.bed.gz and a threshold, uses the threshold to determine if the exon is missing, and ultimately aggregates the two tables for subsequent use by the user.<br>
For diploid species, it is recommended that the threshold be set at 0.3 or lower, as a 0.5-fold depth of coverage is at least evidence of the presence of at least one copy in the diploid; other ploidies can set the threshold based on their own experience.
```
python 02_cds_depth_analyzer.py input.gff3 test.regions.bed.gz --threshold-ratio 0.3 -o output_prefix
```
There will be two files inside the result, one that records the depth of the cds and the determination of whether they are missing or not; the other is how many CDSs in each mRNA are intact with depth information.

```
# cds_detail.csv/tsv
cds_id  depth   IsMissing       length
XX01AG000001.mRNA1_CDS1 25.97   False   34
XX01AG000001.mRNA1_CDS2 25.48   False   332
XX01AG000001.mRNA1_CDS3 28.42   False   213
XX01AG000001.mRNA1_CDS4 31.64   False   149
XX01AG000001.mRNA1_CDS5 35.18   False   169
XX01AG000001.mRNA1_CDS6 24.89   False   93

# mRNA_summary.csv/tsv
mRNA_ID Total_CDS       Valid_CDS       Total_Length    Weighted_Depth  Integrity
XX01AG000001.mRNA1      8       8       1230    29.8559 1.0000
XX01AG000002.mRNA1      2       1       303     24.2195 0.5000
XX01AG000003.mRNA1      7       7       2277    30.0604 1.0000
XX01AG000004.mRNA1      7       7       1479    32.6165 1.0000
XX01AG000005.mRNA1      2       2       321     26.1198 1.0000
```
After obtaining the table, we can filter the genes with high cds completeness to get the target gene sequence names for subsequent analysis<br>
```
awk '{if ($5 >= 0.7) print $1}' mRNA_summary.tsv > mRNA_summary.high_reliability.gene.list
```
