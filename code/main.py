import argparse
from datetime import datetime
import os
from scan_parse import build_cit_table
from plot_structure import plot_from_csv

def main():
    parser = argparse.ArgumentParser(description="Bioinformatics Code Dependency Tracker")
    parser.add_argument('--input_folder', required=True, help='Folder containing code files')
    parser.add_argument('--output_folder', required=True, help='Folder to save outputs (CSV + PNG)')
    args = parser.parse_args()
    
    input_folder = args.input_folder
    output_folder = args.output_folder
    os.makedirs(output_folder, exist_ok=True)
    
    # 时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. 生成 CSV
    df_cit = build_cit_table(input_folder)
    csv_path = os.path.join(output_folder, f"cit_table_{timestamp}.csv")
    df_cit.to_csv(csv_path, index=False)
    print(f"[INFO] CIT table saved to {csv_path}")
    
    # 2. 生成依赖关系图 PNG
    graph_path = os.path.join(output_folder, f"dependency_graph_{timestamp}.pdf")
    plot_from_csv(csv_path, graph_path)
    print(f"[INFO] Dependency graph saved to {graph_path}")

if __name__ == "__main__":
    main()
