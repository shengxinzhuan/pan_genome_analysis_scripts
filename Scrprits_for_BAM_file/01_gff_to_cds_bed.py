import gzip
import sys
from collections import defaultdict

def parse_gff(gff_path):
    cds_dict = defaultdict(list)
    current_mrna = None
    
    with gzip.open(gff_path, 'rt') if gff_path.endswith('.gz') else open(gff_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            if len(fields) < 9:
                continue
            
            feature_type = fields[2]
            attrs = dict(item.split('=') for item in fields[8].split(';') if '=' in item)
            
            if feature_type == 'mRNA':
                current_mrna = attrs.get('ID', None)
            elif feature_type == 'CDS' and current_mrna:
                
                start = int(fields[3]) - 1 if fields[3].isdigit() else 0
                end = int(fields[4]) if fields[4].isdigit() else 0
                cds_dict[current_mrna].append( (fields[0], start, end) )
                
    return cds_dict

if __name__ == '__main__':
    cds_data = parse_gff(sys.argv[1])
    
    
    with open('all_cds.bed', 'w') as bed_f:
        for mrna_id, cds_list in cds_data.items():
            for idx, (chr_, start, end) in enumerate(cds_list, 1):
                bed_f.write(f"{chr_}\t{start}\t{end}\t{mrna_id}_CDS{idx}\n")


