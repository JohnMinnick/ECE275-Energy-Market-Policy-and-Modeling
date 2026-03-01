"""
Generate separate network diagrams for HW2 Problems 1 and 2.
"""

import matplotlib.pyplot as plt
import numpy as np
import os


def draw_network(ax, title, edge_labels, node_annotations=None,
                 highlight_edge=None, highlight_label=None):
    """
    Draw a triangle network on the given axes.

    Args:
        ax: matplotlib axes
        title: plot title
        edge_labels: dict mapping (node1, node2) -> label string
        node_annotations: dict mapping node name -> annotation string
        highlight_edge: tuple (node1, node2) to draw in red
        highlight_label: label for the highlighted edge
    """
    positions = {
        'A': (0.5, 0.93),
        'B': (0.05, 0.15),
        'C': (0.95, 0.15),
    }

    # Draw edges
    for (n1, n2), label in edge_labels.items():
        p1, p2 = positions[n1], positions[n2]
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2

        is_highlighted = (highlight_edge == (n1, n2) or highlight_edge == (n2, n1))
        color = '#cc3333' if is_highlighted else '#555555'
        linewidth = 3.0 if is_highlighted else 2.0

        ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                color=color, linewidth=linewidth, zorder=1)

        center_x, center_y = 0.5, 0.41
        offset_x = (mid_x - center_x) * 0.35
        offset_y = (mid_y - center_y) * 0.35

        display_label = highlight_label if is_highlighted and highlight_label else label
        bbox_color = '#ffcccc' if is_highlighted else '#e8e8e8'
        ax.text(mid_x + offset_x, mid_y + offset_y, display_label,
                ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=bbox_color,
                          edgecolor='gray', alpha=0.9),
                zorder=3)

    # Draw nodes
    for name, (x, y) in positions.items():
        circle = plt.Circle((x, y), 0.06, color='#4488cc', ec='#224466',
                            linewidth=2, zorder=4)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center',
                fontsize=18, fontweight='bold', color='white', zorder=5)

        if node_annotations and name in node_annotations:
            ax.text(x, y - 0.12, node_annotations[name],
                    ha='center', va='top', fontsize=10,
                    color='#333333', style='italic', zorder=5)

    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.05, 1.1)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.axis('off')


def main():
    """Generate two separate network diagram PNGs."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Problem 1
    fig1, ax1 = plt.subplots(figsize=(7, 6))
    draw_network(
        ax1,
        title='Problem 1: Dispatch Network',
        edge_labels={
            ('A', 'B'): 'R = 6.0',
            ('B', 'C'): 'R = 6.0',
            ('A', 'C'): 'R = 4.8',
        },
        node_annotations={
            'A': '200 MW load\nNo generator',
            'B': '200 MW load\n250 MW @ $22',
            'C': '200 MW load\n500 MW @ $26',
        },
        highlight_edge=('A', 'B'),
        highlight_label='R = 6.0\n(45 MW limit)',
    )
    plt.tight_layout()
    path1 = os.path.join(script_dir, 'hw2_network_p1.png')
    fig1.savefig(path1, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {path1}")
    plt.close(fig1)

    # Problem 2
    fig2, ax2 = plt.subplots(figsize=(7, 6))
    draw_network(
        ax2,
        title='Problem 2: PTDF Network',
        edge_labels={
            ('A', 'B'): 'R = 1.7',
            ('B', 'C'): 'R = 1.7',
            ('A', 'C'): 'R = 1.4',
        },
        node_annotations={
            'A': 'Hub (ref)',
            'B': '',
            'C': '1 MW injection',
        },
    )
    plt.tight_layout()
    path2 = os.path.join(script_dir, 'hw2_network_p2.png')
    fig2.savefig(path2, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {path2}")
    plt.close(fig2)


if __name__ == "__main__":
    main()
