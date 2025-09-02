import os
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from datetime import datetime
import argparse

def draw_edges_with_offset(G, pos, ax, offset_ratio=0.002):
    """
    绘制带箭头的边，并偏离节点，避免箭头压在节点上
    """
    for u, v, d in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        dx = x1 - x0
        dy = y1 - y0
        length = np.sqrt(dx**2 + dy**2)
        if length == 0:
            continue
        # 偏移量
        offset = offset_ratio * length
        x_start = x0 + offset * dx / length
        y_start = y0 + offset * dy / length
        x_end = x1 - offset * dx / length
        y_end = y1 - offset * dy / length

        color = "black" if d['etype'] == "input" else "red"

        ax.annotate(
            "",
            xy=(x_end, y_end),
            xytext=(x_start, y_start),
            arrowprops=dict(arrowstyle="->", color=color, lw=2, shrinkA=0, shrinkB=0),
        )

def plot_from_csv(csv_path, pdf_path):
    """
    根据 CSV 文件绘制依赖关系图，并保存为 PDF
    """
    # 读取 CSV
    df = pd.read_csv(csv_path)

    # 构建有向图
    G = nx.DiGraph()

    for _, row in df.iterrows():
        file_node = os.path.basename(row['file'])

        # input 节点
        inputs = eval(row['input']) if isinstance(row['input'], str) and row['input'].startswith("[") else []
        for inp in inputs:
            inp_node = os.path.basename(inp)
            G.add_node(inp_node, ntype="input")
            G.add_edge(inp_node, file_node, etype="input")

        # previous code 节点
        prevs = eval(row['previous code']) if isinstance(row['previous code'], str) and row['previous code'].startswith("[") else []
        for prev in prevs:
            prev_node = os.path.basename(prev)
            G.add_node(prev_node, ntype="code")
            G.add_edge(prev_node, file_node, etype="previous")

        # 文件节点
        G.add_node(file_node, ntype="code")

    # 布局
    pos = nx.spring_layout(G, seed=42)

    # 节点颜色
    node_colors = ["skyblue" if attr['ntype']=="input" else "lightgreen" for _, attr in G.nodes(data=True)]

    # 绘图
    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_colors, edgecolors="black", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

    # 绘制带偏移箭头的边
    draw_edges_with_offset(G, pos, ax, offset_ratio=0.12)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"[INFO] PDF saved to {pdf_path}")
