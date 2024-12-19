import pandas as pd
import sys

#### Usage ####
# python ortho_count_2_pav.sort.py Orthogroups.GeneCount.tsv ortho_pav.sort.tsv
# description: this scripts is use to count orthogroups to gene_present_absent.
#              the level of output: core, near-core, pan, private, undefined
#              core: both genome own
#              near-core: >= 70% genome within
#              pan: < 70% but > 1 genome within
#              private: only 1 genome own
#              undefined: both genome not own
##############

df = pd.read_csv(sys.argv[1], sep='\t')
df = df.drop(columns=['Total'])
df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: 1 if x > 0 else -1)

non_zero_counts = (df.iloc[:, 1:] == 1).sum(axis=1)

total_columns = df.shape[1] - 1

def determine_type(row):
    non_zero_count = (row == 1).sum()
    if non_zero_count == total_columns:
        return 'core'
    elif non_zero_count >= 0.7 * total_columns:
        return 'near-core'
    elif non_zero_count > 1:
        return 'pan'
    elif non_zero_count == 1:
        return 'private'
    else:
        return 'undefined'

df['type'] = df.iloc[:, 1:].apply(determine_type, axis=1)

type_order = {'core': 1, 'near-core': 2, 'pan': 3, 'private': 4, 'undefined': 5}
df['type_order'] = df['type'].map(type_order)

df = df.sort_values(by='type_order').drop(columns=['type_order'])

df.to_csv(sys.argv[2], sep='\t', index=False)

