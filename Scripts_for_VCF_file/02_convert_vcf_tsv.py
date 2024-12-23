import sys

def convert_vcf_format(vcf_file_path):
    with open(vcf_file_path, 'r') as vcf_file:
        sample_names = []
        for line in vcf_file:
            
            if line.startswith('#'):
                if line.split('\t')[0] == "#CHROM" :
                    sample_names = line.strip().split('\t')[9:]
                    headers = ['chr_pos']  + sample_names
                    print('\t'.join(headers))
                continue

            
            parts = line.strip().split('\t')
            
            
            samples = parts[9:]
            
            
            converted_samples = []
            for sample in samples:
                genotype = sample.split(':')[0] 
                if genotype == './.':
                    converted_samples.append('Nan')
                else:
                    converted_samples.append(genotype)
            
            
            chr_pos = f"{parts[0]}_{parts[1]}"
            
            
            
            
            output_parts = [chr_pos]  + converted_samples
            print('\t'.join(output_parts))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_vcf.py [path_to_vcf_file]")
        sys.exit(1)
    
    vcf_file_path = sys.argv[1]
    convert_vcf_format(vcf_file_path)

