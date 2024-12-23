import sys

def process_vcf(vcf_file):
    with open(vcf_file, 'r') as file:
        with open(vcf_file.replace('.vcf', '_processed.vcf'), 'w') as outfile:
            for line in file:
                if line.startswith('#'):
                    outfile.write(line)
                    continue
                
                parts = line.strip().split('\t')
                chrom, pos, id, ref, alt, qual, filter, info = parts[:8]
                
               
                if (len(ref) > 1 or len(alt) > 1) and 1 < len(ref) - len(alt) <= 50:
                    replacement_type = None
                   
                    if len(ref) < len(alt):
                        insertion_length = len(alt) - len(ref)
                        if insertion_length < 10:
                            new_ref, new_alt = 'A', 'T'
                            replacement_type = 'A/T'
                        else:
                            new_ref, new_alt = 'T', 'A'
                            replacement_type = 'T/A'
                    else:  
                        deletion_length = len(ref) - len(alt)
                        if deletion_length < 10:
                            new_ref, new_alt = 'G', 'C'
                            replacement_type = 'G/C'
                        else:
                            new_ref, new_alt = 'C', 'G'
                            replacement_type = 'C/G'
                    
                    
                    print(f"{chrom}\t{pos}\t{ref}\t{alt}\t{replacement_type}")
                    
                    
                    parts[3] = new_ref
                    parts[4] = new_alt
                    outfile.write('\t'.join(parts) + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.vcf")
        sys.exit(1)
    
    vcf_file = sys.argv[1]
    process_vcf(vcf_file)

