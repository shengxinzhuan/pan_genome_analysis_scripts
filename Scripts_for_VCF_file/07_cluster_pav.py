import argparse
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt

def sort_vcf_by_pca(input_file_path, output_file_path, cluster_file_path, output_plot_path):
    
    data = pd.read_csv(input_file_path, sep='\t', index_col=0)

    
    data_to_cluster = data.drop(columns=['type'])

    
    data_to_cluster_transposed = data_to_cluster.T

    
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data_to_cluster_transposed)

    
    kmeans = KMeans(n_clusters=2, random_state=0)
    clusters = kmeans.fit_predict(data_pca)

    
    clustered_data_transposed = data_to_cluster_transposed.copy()
    clustered_data_transposed['Cluster'] = clusters

    
    clustered_data_sorted_transposed = clustered_data_transposed.sort_values(by='Cluster')

    
    clustered_data_sorted = clustered_data_sorted_transposed.drop(columns=['Cluster']).T

    
    clustered_data_sorted['type'] = data['type']

    
    clustered_data_sorted.to_csv(output_file_path, sep='\t', index=True)

    # PCA result
    cluster_results = pd.DataFrame(data_pca, columns = ['PCA1','PCA2'])
    cluster_results['Cluster'] = clusters
    cluster_results['Sample'] = data_to_cluster_transposed.index
    cluster_results.to_csv(cluster_file_path, sep = '\t' ,index=False)
    
    
    # PCA plot
    plt.figure(figsize=(8, 6))
    plt.scatter(data_pca[:, 0], data_pca[:, 1], c=clusters, cmap='viridis', marker='o')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.title('PCA of VCF Data')
    plt.colorbar(label='Cluster')
    plt.savefig(output_plot_path)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sort VCF file by PCA and KMeans clustering.')
    parser.add_argument('input_file', type=str, help='Path to the input VCF file.')
    parser.add_argument('output_file', type=str, help='Path to the output sorted TSV file.')
    parser.add_argument('cluster_file', type=str, help='Path to the output cluster CSV file.')
    parser.add_argument('output_plot', type=str, help='Path to the output PCA plot PNG file.')
    args = parser.parse_args()

    sort_vcf_by_pca(args.input_file, args.output_file, args.cluster_file, args.output_plot)

