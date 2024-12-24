import sys

def filter_biallelic_indels(vcf_file):
    with open(vcf_file, 'r') as file:
        for line in file:
            
            if line.startswith('#'):
                print(line, end='')
                continue
            
            
            parts = line.split()
            
            
            alt_field = parts[4]
            
            
            if ',' not in alt_field:
                print(line, end='')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python filter_biallelic_indels.py <input.vcf>")
        sys.exit(1)
    
    input_vcf = sys.argv[1]
    filter_biallelic_indels(input_vcf)

