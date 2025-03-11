import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def scale_luminance(rgb, luminance_target, max_luminance=100):
    """
    Scales the RGB values to match the target luminance using the formula:
    L = 0.299R + 0.587G + 0.114B
    """
    # Calculate current luminance
    current_luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    
    # Prevent division by zero for black color (current_luminance = 0)
    if current_luminance == 0:
        return rgb  # No scaling needed for black (0 luminance)
    
    # Scale factor to match target luminance
    scale_factor = luminance_target / current_luminance
    return np.clip(np.array(rgb) * scale_factor, 0, 1)

def generate_rotating_snake(num_rings=6, num_repeats=24, shift_per_ring=2, 
                            bg_luminance=50, max_lum_cd_m2=100, image_size=(800, 800), 
                            color_mode="grayscale", element_order=None, luminance_values=None,
                            rotation_direction="counter_clockwise", save_path="rotating_snake.png"):
    """
    Parameters:
    - num_rings: Number of concentric rings.
    - num_repeats: Number of times the pattern repeats around the ring.
    - shift_per_ring: Phase shift per ring (shifts color sequence).
    - bg_luminance: Background luminance in cd/m².
    - max_lum_cd_m2: Maximum luminance of display in cd/m² (for normalization).
    - image_size: (width, height) in pixels.
    - color_mode: "grayscale", "blue_yellow", or "red_green".
    - element_order: List specifying the order of colors (overrides color_mode default).
    - luminance_values: Dict mapping colors to custom luminance levels.
    - rotation_direction: "counter_clockwise" (default) or "clockwise".
    - save_path: File path to save the generated PNG image.
    """

    # Normalize background luminance
    bg_luminance_norm = np.clip(bg_luminance / max_lum_cd_m2, 0, 1)

    # Normalize element luminances
    default_luminance = {
        "white": 70 / max_lum_cd_m2,
        "light_gray": 40 / max_lum_cd_m2,
        "dark_gray": 30 / max_lum_cd_m2,
        "black": 0 / max_lum_cd_m2
    }

    if luminance_values:
        default_luminance.update({k: v / max_lum_cd_m2 for k, v in luminance_values.items()})

    # Define RGB values for each color
    color_map = {
        "white": [1, 1, 1],
        "light_gray": [0.6, 0.6, 0.6],
        "dark_gray": [0.3, 0.3, 0.3],
        "black": [0, 0, 0],
        "blue": [15.3 / 255, 16.575 / 255, 255 / 255],
        "yellow": [183.6 / 255, 188.7 / 255, 0],
        "red": [216.75 / 255, 0, 0],
        "green": [0, 255 / 255, 0]
    }

    # Apply custom luminance scaling to colors
    for color, luminance in default_luminance.items():
        if color in color_map:
            color_map[color] = scale_luminance(color_map[color], luminance)

    # Set default element order if none is provided
    if element_order is None:
        if color_mode == "blue_yellow":
            element_order = ["black", "blue", "white", "yellow"]
        elif color_mode == "red_green":
            element_order = ["black", "red", "white", "green"]
        else:  # Default grayscale
            element_order = ["black", "dark_gray", "white", "light_gray"]

    # Reverse order for clockwise
    if rotation_direction == "clockwise":
        element_order = element_order[::-1]

    fig, ax = plt.subplots(figsize=(image_size[0] / 100, image_size[1] / 100), dpi=100)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor((bg_luminance_norm, bg_luminance_norm, bg_luminance_norm))

    # Loop through each ring
    for ring in range(num_rings):
        num_segments = len(element_order) * num_repeats
        angle_step = 360 / num_segments
        inner_radius = ring / num_rings
        outer_radius = (ring + 1) / num_rings

        # Shift the sequence per ring
        shifted_sequence = element_order[ring * shift_per_ring % len(element_order):] + \
                           element_order[:ring * shift_per_ring % len(element_order)]

        # Create wedges
        for i in range(num_segments):
            color = color_map[shifted_sequence[i % len(shifted_sequence)]]
            theta1 = i * angle_step
            theta2 = (i + 1) * angle_step

            wedge = patches.Wedge(
                (0, 0), outer_radius, theta1, theta2, width=1/num_rings, color=color
            )
            ax.add_patch(wedge)

    # Save as PNG
    plt.savefig(save_path, dpi=100, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
