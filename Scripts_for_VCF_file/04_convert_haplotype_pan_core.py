import sys

def classify_row(row, total_samples):
    non_minus_one_count = sum(1 for value in row[1:] if value != '-1')
    if non_minus_one_count == 0:
        return 'loss'
    elif non_minus_one_count == 1:
        return 'private'
    elif non_minus_one_count > 1 and non_minus_one_count < 0.7 * total_samples:
        return 'pan'
    elif non_minus_one_count >= 0.7 * total_samples and non_minus_one_count < total_samples:
        return 'near-core'
    else:
        return 'core'

def read_and_classify_data(input_file_path):
    with open(input_file_path, 'r') as file:
        headers = file.readline().strip().split('\t')
        total_samples = len(headers) - 1  
        data = [headers + ['type']]  
        for line in file:
            row = line.strip().split('\t')
            row_type = classify_row(row, total_samples)
            data.append(row + [row_type])  
    return data

def sort_and_output_data(data, output_file_path):
    sorting_order = ['core', 'near-core', 'pan', 'private', 'loss']
    sorted_data = sorted(data[1:], key=lambda x: (sorting_order.index(x[-1]), x[0]))
    sorted_data_with_headers = data[:1] + sorted_data 

    with open(output_file_path, 'w') as file:
        for row in sorted_data_with_headers:
            file.write('\t'.join(row) + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py [path_to_input_file] [path_to_output_file]")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    data = read_and_classify_data(input_file_path)
    sort_and_output_data(data, output_file_path)

