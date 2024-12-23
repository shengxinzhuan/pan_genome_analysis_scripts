import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
import sys

##### Usage #####
# python boxplot_pan_core.gene_num.py test.pan.tsv (not test.pav.tsv)
# description: this scripts will generate a boxplot for pan and core gene numbers,
# and a file for different groups count results (such as A_B_pan, A_B_core, A_B_C_pan, A_B_C_core)
#################


df = pd.read_csv(sys.argv[1], sep='\t', index_col=0)


df_values = df.iloc[:, :-1]

combination_counts = {}


for r in range(2, len(df_values.columns) + 1):
    for cols in combinations(df_values.columns, r):
        
        cols_list = list(cols)
        
        sub_df = df_values[cols_list]
        
        
        sub_df = sub_df[sub_df.sum(axis=1) > 0]
        
        
        core_count = sub_df.sum().sum()
        
        
        pan_count = sub_df.isin([0]).sum().sum()
        
        
        combination_key = '_'.join(cols_list)
        
        
        combination_counts[f"{combination_key}_core"] = core_count
        combination_counts[f"{combination_key}_pan"] = pan_count


data = {
    'Combination Size': [],
    'Count': [],
    'Type': []
}
for key, value in combination_counts.items():
    parts = key.split('_')
    combination_size = len(parts) - 1
    gene_type = parts[-1]
    data['Combination Size'].append(combination_size)
    data['Count'].append(value)
    data['Type'].append(gene_type)


boxplot_df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))
bx = sns.boxplot(x='Combination Size', y='Count', hue='Type', data=boxplot_df)
plt.title('Boxplot of Core and Pan Counts by Combination Size')
plt.xlabel('Combination Size')
plt.ylabel('Gene Count')
plt.legend(title='Gene Type')
plt.xticks(range(2, len(df_values.columns) + 1))
plt.tight_layout()
plt.savefig('boxplot_pan_core.gene_num.png', bbox_inches='tight', dpi=300)

plt.show()

