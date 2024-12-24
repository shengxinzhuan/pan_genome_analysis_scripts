import argparse
import sys

def is_snp(ref, alt):
    return len(ref) == 1 and len(alt) == 1

def is_indel(ref, alt):
    return len(ref) != len(alt) and all(len(x) < 50 for x in (ref, alt))

def is_sv(ref, alt):
    return len(ref) >= 50 or len(alt) >= 50

def filter_vcf(input_vcf, snp, indel, sv):
    with open(input_vcf, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue  # Skip header lines
            
            parts = line.strip().split('\t')
            ref = parts[3]
            alts = parts[4].split(',')
            
            # Determine the type of variant and write to the appropriate file
            for alt in alts:
                if is_snp(ref, alt):
                    with open(snp, 'a') as snp_file:
                        snp_file.write(line)
                elif is_indel(ref, alt):
                    with open(indel, 'a') as indel_file:
                        indel_file.write(line)
                elif is_sv(ref, alt):
                    with open(sv, 'a') as sv_file:
                        sv_file.write(line)

def main():
    parser = argparse.ArgumentParser(description='Filter VCF file into SNP, Indel, and SV.')
    parser.add_argument('input_vcf', help='Input VCF file')
    parser.add_argument('--snp', default='output.snp.vcf', help='Output SNP VCF file')
    parser.add_argument('--indel', default='output.indel.vcf', help='Output Indel VCF file')
    parser.add_argument('--sv', default='output.sv.vcf', help='Output SV VCF file')
    
    args = parser.parse_args()
    
    # Open output files and write headers
    with open(args.input_vcf, 'r') as file:
        for line in file:
            if line.startswith('#'):
                with open(args.snp, 'w') as snp_file:
                    snp_file.write(line)
                with open(args.indel, 'w') as indel_file:
                    indel_file.write(line)
                with open(args.sv, 'w') as sv_file:
                    sv_file.write(line)
            else:
                break
    
    # Filter the VCF file
    filter_vcf(args.input_vcf, args.snp, args.indel, args.sv)

if __name__ == '__main__':
    main()

