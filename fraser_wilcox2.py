def generate_fraser_wilcox2(num_rings=6, num_repeats=6, num_steps=100, 
                                   figure_size_pixels=(800, 800), bg_luminance=30, 
                                   max_lum_cd_m2=100, shift_per_ring=1,
                                   luminance_levels=[1, 2/3, 0, 1/3], 
                                   rotation_direction='counterclockwise', save_path="fraser_wilcox2.png"):
    """
    
    Parameters:
    - num_rings: Number of concentric rings.
    - num_repeats: Number of repeats of the gradient sequence around the ring.
    - num_steps: Number of steps for the smooth gradient transition.
    - figure_size_pixels: Size of the figure in pixels (tuple: width, height).
    - bg_luminance: Background luminance in cd/m² (default 30 cd/m²).
    - max_lum_cd_m2: Maximum luminance of display in cd/m² (used for normalization).
    - shift_per_ring: How much to shift the color pattern for each ring.
    - luminance_levels: List of luminance levels (normalized), where [1, 2/3, 0, 1/3] are the default values corresponding to white, light gray, black, and dark gray.
    - rotation_direction: The direction of the gradient (counterclockwise or clockwise).
    - save_path: File path to save the generated PNG image.
    """
    # Convert cm to inches for matplotlib 
    CM_TO_INCHES = 0.3937
    fig_size = (figure_size_pixels[0] / 100, figure_size_pixels[1] / 100)
    
    fig, ax = plt.subplots(figsize=fig_size, dpi=100)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor((bg_luminance / max_lum_cd_m2, bg_luminance / max_lum_cd_m2, bg_luminance / max_lum_cd_m2)) 

    # Loop through each ring
    for ring in range(num_rings):
        total_segments = num_repeats * num_steps
        angle_step = 360 / total_segments
        shift = (ring * shift_per_ring * num_steps // 2) % num_steps  # Adjust shift for proper alignment

        for repeat in range(num_repeats):
            for i in range(num_steps):
                theta1 = (i + repeat * num_steps) * angle_step
                theta2 = (i + repeat * num_steps + 1) * angle_step
                inner_radius = ring / num_rings
                outer_radius = (ring + 1) / num_rings
                
                # for clockwise rotation
                if rotation_direction == 'clockwise':
                    theta1, theta2 = -theta2, -theta1

                # Alternating wedge pattern based on luminance levels
                if ((repeat + ring) % 2) == 0:
                    grad = (i + shift) / num_steps  # 0 to 1 progression
                    color_value = luminance_levels[2] + grad * (luminance_levels[3] - luminance_levels[2])  # Black to Dim Gray
                else:
                    grad = (i + shift) / num_steps  # 0 to 1 progression
                    color_value = luminance_levels[0] - grad * (luminance_levels[0] - luminance_levels[1])  # White to Light Gray
                
                wedge = patches.Wedge(
                    (0, 0), outer_radius, theta1, theta2, width=outer_radius - inner_radius, 
                    color=(color_value, color_value, color_value)
                )
                ax.add_patch(wedge)

    # Save the generated figure as PNG
    plt.savefig(save_path, dpi=100, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


