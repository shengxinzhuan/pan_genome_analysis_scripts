import pandas as pd
import sys

##### Usage #####
# python count_orthogroups.py Orthogroups.GeneCount.tsv Output.pan_core_count.tsv
#################

df = pd.read_csv(sys.argv[1], sep='\t')
df = df.drop(columns=['Total'])
non_zero_counts = (df.iloc[:, 1:] > 0).sum(axis=1)

total_columns = df.shape[1] - 1

def determine_type(row):
    non_zero_ratio = (row > 0).sum() / total_columns
    if non_zero_ratio == 1:
        return 'core'
    elif non_zero_ratio >= 0.7:
        return 'near-core'
    elif non_zero_ratio >= 0.2:
        return 'pan'
    else:
        return 'private'

df['type'] = df.iloc[:, 1:].apply(determine_type, axis=1)

df.to_csv(sys.argv[2], sep='\t', index=False)

