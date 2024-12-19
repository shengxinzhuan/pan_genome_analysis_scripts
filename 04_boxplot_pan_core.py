import pandas as pd
from itertools import combinations
import sys
import matplotlib.pyplot as plt
import seaborn as sns

##### Usage #####
# python boxplot_pan_core.py test.pav.tsv
# description: this scripts will generate a boxplot for pan and core gene family,
# and a file for different groups count results (such as A_B_pan, A_B_core, A_B_C_pan, A_B_C_core)
#################

df = pd.read_csv(sys.argv[1], sep='\t',index_col=0)


df_values = df.iloc[:, :-1]


combination_counts = {}

for r in range(2, len(df_values.columns) + 1):
    for cols in combinations(df_values.columns, r):
        
        cols_list = list(cols)
        
        sub_df = df_values[cols_list]
        
        sub_df = sub_df[(sub_df != -1).any(axis=1)]
        
        core_count = (sub_df == 1).all(axis=1).sum()
        
        pan_count = len(sub_df) - core_count
        
        combination_key = '_'.join(cols_list)
        
        combination_counts[f"{combination_key}_core"] = core_count
        combination_counts[f"{combination_key}_pan"] = pan_count

with open('ortholog_counts_pan_core.combination.txt', 'w') as f:
        for combination, count in combination_counts.items():
                    f.write(f"{combination}: {count}\n")

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
plt.ylabel('Gene Family Count')
plt.legend(title='Gene Family Type')
plt.xticks(range(2, len(df_values.columns) + 1))
plt.tight_layout()
plt.savefig('boxplot_pan_core.pdf', bbox_inches='tight', dpi=300)
plt.show()

