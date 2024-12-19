import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib.colors import ListedColormap

##### Usage #####
# python heatmap.py test.pav.tsv
# description: this script will generate a heatmap and pieplot for sort result
# input file: 1(present) -1 (absence)
# Orthogroups   A   B   C   D   E   type
# groups1   1   1   1   1   1   1   core
# groups2   1   -1  1   1   1   1   near-core
# groups3   1   -1  1   -1  -1  -1  pan
# groups4   1   -1  -1  -1  -1  -1  private
#################

df = pd.read_csv(sys.argv[1], sep = '\t', index_col = 0, header=0)

type_counts = df.iloc[:, -1].value_counts()

labels = type_counts.index
sizes = type_counts.values
labels_with_counts = [f"{label} ({count})" for label, count in zip(labels, sizes)]

plt.figure(figsize=(8, 8))
pieplot = plt.pie(sizes, labels=labels_with_counts, autopct='%1.1f%%', startangle=140)
plt.axis('equal')


plt.title('Pie Chart of Gene Family Types')

plt.savefig("pieplot_pan_core.pdf",bbox_inches='tight', dpi=300)
plt.show()

df = df.drop(columns=['type'])

colors = ['#a6e3e9','#f38181']
custom_cmap = ListedColormap(colors)
plt.figure(figsize=(15, 10))
hm = sns.heatmap(data=df,cmap=custom_cmap, yticklabels=False)
plt.savefig('heatmap_pan_core.pdf', bbox_inches='tight', dpi=300)

