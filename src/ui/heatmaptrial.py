import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os

# Define specific gaze points for each region with wider spread
np.random.seed(42)  # Ensure reproducibility

gaze_points = {
    'road': [(1280 + np.random.randn()*400, 720 + np.random.randn()*200) for _ in range(800)],
    'rearview_mirror': [(1280 + np.random.randn()*150, 1300 + np.random.randn()*150) for _ in range(200)],
    'dashboard': [(1280 + np.random.randn()*300, 100 + np.random.randn()*150) for _ in range(300)],
    'left_mirror': [(400 + np.random.randn()*150, 720 + np.random.randn()*150) for _ in range(200)],
    'right_mirror': [(2160 + np.random.randn()*150, 720 + np.random.randn()*150) for _ in range(200)],
    'random': [(np.random.rand()*2560, np.random.rand()*1440) for _ in range(1000)]
}

# Combine all gaze points into a single list
all_points = []
for region, points in gaze_points.items():
    all_points.extend(points)

# Convert gaze points to a numpy array
all_points = np.array(all_points)

# Filter out intersections that are outside the screen bounds
screen_size = (2560, 1440)
filtered_intersections = [p for p in all_points if 0 <= p[0] <= screen_size[0] and 0 <= p[1] <= screen_size[1]]

# Convert intersections to a heatmap
heatmap, xedges, yedges = np.histogram2d(
    [p[0] for p in filtered_intersections],
    [p[1] for p in filtered_intersections],
    bins=(screen_size[0]//10, screen_size[1]//10)
)

# Apply Gaussian filter for smoothing
heatmap = gaussian_filter(heatmap, sigma=8)

# Plot the heatmap
plt.figure(figsize=(12, 6))
plt.imshow(heatmap.T, extent=[0, screen_size[0], 0, screen_size[1]], origin='lower', cmap='jet')
plt.colorbar(label='Gaze Intensity')
plt.xlabel('Horizontal Position (pixels)')
plt.ylabel('Vertical Position (pixels)')

# Add labels for regions
plt.text(1280, 720, 'Road', color='white', fontsize=12, ha='center')
plt.text(1280, 1300, 'Rearview Mirror', color='white', fontsize=12, ha='center')
plt.text(1280, 100, 'Dashboard', color='white', fontsize=12, ha='center')
plt.text(400, 720, 'Left Mirror', color='white', fontsize=12, ha='center')
plt.text(2160, 720, 'Right Mirror', color='white', fontsize=12, ha='center')

plt.title('Driver Gaze Heatmap')

