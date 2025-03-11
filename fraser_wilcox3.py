import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_fraser_wilcox3(num_rings=6, num_repeats=6, num_steps=100, 
                            figure_size_pixels=(800, 800), bg_luminance=30, 
                            max_lum_cd_m2=100, luminance_levels=None, 
                            rotation_direction='counterclockwise', save_path="fraser_wilcox3.png"):
    """
    Parameters:
    - num_rings: Number of concentric rings.
    - num_repeats: Number of repeats of the gradient sequence around the ring.
    - num_steps: Number of steps for the smooth gradient transition.
    - figure_size_pixels: Size of the figure in pixels (tuple: width, height).
    - bg_luminance: Background luminance in cd/m² (default 30 cd/m²).
    - max_lum_cd_m2: Maximum luminance of display in cd/m² (used for normalization).
    - luminance_levels: List of luminance levels (normalized), if not specified, default values are used.
    - rotation_direction: The direction of the gradient ('counterclockwise' or 'clockwise').
    - save_path: File path to save the generated PNG image.
    """
    
    # Normalize background luminance
    bg_luminance_norm = np.clip(bg_luminance / max_lum_cd_m2, 0, 1)
    
    # Set default luminance levels if not specified
    if luminance_levels is None:
        luminance_values = {
            "black": 1e-3 / max_lum_cd_m2,
            "dark_gray": 30 / max_lum_cd_m2,
            "light_gray": 40 / max_lum_cd_m2,
            "white": 70 / max_lum_cd_m2
        }
        luminance_sequence = [luminance_values["black"], luminance_values["dark_gray"], 
                              luminance_values["light_gray"], luminance_values["white"]]
    else:
        luminance_sequence = luminance_levels
    
    fig_size = (figure_size_pixels[0] / 100, figure_size_pixels[1] / 100)
    
    fig, ax = plt.subplots(figsize=fig_size, dpi=100)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor((bg_luminance_norm, bg_luminance_norm, bg_luminance_norm))  # Set background luminance

    # Loop through each ring
    for ring in range(num_rings):
        total_segments = num_repeats * num_steps
        angle_step = 360 / total_segments
        inner_radius = ring / num_rings
        outer_radius = (ring + 1) / num_rings
        
        for repeat in range(num_repeats):
            for i in range(num_steps):
                theta1 = (i + repeat * num_steps) * angle_step
                theta2 = (i + repeat * num_steps + 1) * angle_step
                
                # If clockwise rotation, reverse the angles
                if rotation_direction == 'clockwise':
                    theta1, theta2 = -theta2, -theta1
                
                if ring % 2 == 0:
                    color = (bg_luminance_norm, bg_luminance_norm, bg_luminance_norm)
                else:
                    grad = (i) / num_steps
                    color_value = luminance_sequence[0] + grad * (luminance_sequence[3] - luminance_sequence[0])
                    color = (color_value, color_value, color_value)
                
                # Create the wedge
                wedge = patches.Wedge(
                    (0, 0), outer_radius, theta1, theta2, width=outer_radius - inner_radius, color=color
                )
                ax.add_patch(wedge)

    # Save the generated figure as PNG
    plt.savefig(save_path, dpi=100, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
