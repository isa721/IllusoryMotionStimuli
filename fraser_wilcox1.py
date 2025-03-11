def generate_fraser_wilcox1(num_rings=6, num_repeats=6, num_steps=100, 
                                               figure_size_pixels=(800, 800), bg_luminance=30, 
                                               max_lum_cd_m2=100, shift_per_ring=1,
                                               luminance_levels=[0, 0.3], 
                                               rotation_direction='counterclockwise', save_path="fraser_wilcox1.png"):  
    """
    
    Parameters:
    - num_rings: Number of concentric rings.
    - num_repeats: Number of repeats of the gradient sequence around the ring.
    - num_steps: Number of steps for the smooth gradient transition.
    - figure_size_pixels: Size of the figure in pixels (tuple: width, height).
    - bg_luminance: Background luminance in cd/m² (default 30 cd/m²).
    - max_lum_cd_m2: Maximum luminance of display in cd/m² (used for normalization).
    - shift_per_ring: How much to shift the color pattern for each ring.
    - luminance_levels: List of luminance levels to create the gradient (e.g., [0, 0.3] for black to dark gray)
    - rotation_direction: The direction of the gradient (counterclockwise or clockwise).
    - save_path: File path to save the generated PNG image.
    """
    
    # Normalize luminances
    bg_luminance_norm = np.clip(bg_luminance / max_lum_cd_m2, 0, 1)

    luminance_norm = [level for level in luminance_levels]
    

    fig, ax = plt.subplots(figsize=(figure_size_pixels[0] / 100, figure_size_pixels[1] / 100), dpi=100)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor((bg_luminance_norm, bg_luminance_norm, bg_luminance_norm))

    # Loop through each ring
    for ring in range(num_rings):
        # Total number of segments in the ring
        total_segments = num_repeats * num_steps
        angle_step = 360 / total_segments  # Angular span for each segment
        
        # Shift the color pattern for the current ring
        shift = (ring * shift_per_ring) % num_steps 
        
        # Loop through the repeats to create smooth gradient across the ring
        for repeat in range(num_repeats):
            for i in range(num_steps):
                # Define the angle for the gradient segment
                theta1 = (i + repeat * num_steps) * angle_step
                theta2 = (i + repeat * num_steps + 1) * angle_step

                #Reverse for clockwise motion
                if rotation_direction == 'clockwise':
                    theta1, theta2 = -theta2, -theta1

                # Define the radius for the segment
                inner_radius = ring / num_rings 
                outer_radius = (ring + 1) / num_rings

                if (ring + repeat) % 2 == 0:
                    # Smooth gradient from specified luminance levels
                    grad = (i + shift) / num_steps 
                    luminance_value = luminance_norm[0] + grad * (luminance_norm[1] - luminance_norm[0])
                    luminance_value = np.clip(luminance_value, 0, 1) 
                    color = (luminance_value, luminance_value, luminance_value)
                else:
                    # Solid color for the alternating wedge
                    color = (bg_luminance_norm, bg_luminance_norm, bg_luminance_norm)
                
                # Create the wedge
                wedge = patches.Wedge(
                    (0, 0), outer_radius, theta1, theta2, width=outer_radius - inner_radius, 
                    color=color
                )
                ax.add_patch(wedge)

    # Save the generated figure as PNG
    plt.savefig(save_path, dpi=100, bbox_inches="tight", pad_inches=0)
    plt.close(fig)