import sys

def convert_data(input_file_path):
    with open(input_file_path, 'r') as file:
        
        headers = file.readline().strip().split('\t')
        
        
        print('\t'.join(headers))
        
        
        for line in file:
            parts = line.strip().split('\t')
            
            converted_parts = [parts[0]]
            for part in parts[1:]:
                if part == 'Nan':
                    converted_parts.append('-1')
                elif part in ['1|1', '1/1']:
                    converted_parts.append('1')
                elif part in ['0/0', '0|0']:
                    converted_parts.append('0')
                elif part in ['0/1', '0|1', '1|0','1/0']:
                    converted_parts.append('0.5')
                else:
                    
                    converted_parts.append(part)
            
            print('\t'.join(converted_parts))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_data.py [path_to_input_file]")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    convert_data(input_file_path)

