import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Simulated function to calculate intersection points
def calculate_intersection(gaze_vectors, user_position):
    intersections = []
    user_x, user_y, user_z = user_position
    
    for vector in gaze_vectors:
        # Intersection calculation assuming screen is at z=0
        t = -user_z
        x = user_x + vector[0] * t
        y = user_y + vector[1] * t
        intersections.append((x, y))
    
    return intersections

# Example gaze direction vectors (randomly generated for this example)
gaze_vectors = np.random.randn(1000, 2)*30
print(gaze_vectors)
screen_size = (2560, 1440)
user_position = (0, 0, -60)  # Example user position (600 units away from the screen)

# Calculate intersection points
intersections = calculate_intersection(gaze_vectors, user_position)

# Filter out intersections that are outside the screen bounds
filtered_intersections = [p for p in intersections if 0 <= p[0] <= screen_size[0] and 0 <= p[1] <= screen_size[1]]

# Convert intersections to a heatmap
heatmap, xedges, yedges = np.histogram2d(
    [p[0] for p in filtered_intersections],
    [p[1] for p in filtered_intersections],
    bins=(screen_size[0]//10, screen_size[1]//10)
)

# Apply Gaussian filter for smoothing
heatmap = gaussian_filter(heatmap, sigma=16)

# Plot the heatmap
plt.imshow(heatmap.T, extent=[0, screen_size[0], 0, screen_size[1]], origin='lower')
plt.colorbar()
plt.show()
