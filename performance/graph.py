import matplotlib.pyplot as plt
import numpy as np

# Data
file_sizes = [1, 10, 50]  # MB
approaches = ['memory', 'mapping', 'parallel', 'simple']

# Patch Creation Times
creation_times = np.array([
    [1.28, 25.31, 183.85],
    [1.00, 26.18, 179.78],
    [1.82, 30.90, 194.10],
    [1.20, 27.96, 207.15]
])

# Patch Application Times
application_times = np.array([
    [0.13, 1.16, 6.60],
    [0.11, 1.03, 5.61],
    [0.18, 1.26, 5.67],
    [0.11, 1.32, 6.26]
])

# Patch Sizes
patch_sizes = np.array([
    [1.00, 10.04, 50.22],
    [1.00, 10.04, 50.22],
    [1.00, 10.04, 50.22],
    [1.00, 10.04, 50.22]
])

# Colors for each approach
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# Create subplots
fig, axs = plt.subplots(3, 3, figsize=(18, 18))
fig.suptitle('Patch Metrics Comparison for Different File Sizes', fontsize=16)

metrics = ['Creation Time (s)', 'Application Time (s)', 'Patch Size (MB)']
data = [creation_times, application_times, patch_sizes]

for i, size in enumerate(file_sizes):
    for j, (metric, metric_data) in enumerate(zip(metrics, data)):
        ax = axs[i, j]
        x = np.arange(len(approaches))
        bars = ax.bar(x, metric_data[:, i], color=colors)
        
        ax.set_ylabel(metric)
        ax.set_title(f'{metric} - {size}MB')
        ax.set_xticks(x)
        ax.set_xticklabels(approaches, rotation=0, ha='center', fontsize=8)
        
        # Add value labels on the bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', rotation=0, fontsize=8)

        # Adjust y-axis for better visibility
        if j == 0:  # Creation Time
            ax.set_yscale('log')
        elif j == 1:  # Application Time
            ax.set_ylim(0, max(metric_data[:, i]) * 1.2)
        
        # Adjust bottom margin for x-labels
        ax.tick_params(axis='x', which='major', pad=10)

plt.tight_layout()
plt.subplots_adjust(hspace=0.4, bottom=0.1)  # Increase vertical space between plots
plt.show()