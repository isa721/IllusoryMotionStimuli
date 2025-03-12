import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def adjust_luminance(color, luminance_factor):
    """
    Adjust the luminance of an RGB color by multiplying each component with the luminance factor.
    """
    return tuple(c * luminance_factor for c in color)

def generate_rotating_snake(num_rings=6, num_repeats=24, shift_per_ring=2, 
                            bg_luminance=50, max_lum_cd_m2=100, image_size=(800, 800), 
                            color_mode="grayscale", element_order=None, luminance_values=None,
                            rotation_direction="counter_clockwise", save_path="rotating_snake.png"):
    """
    Generates a customizable rotating snake illusion.

    Parameters:
    - num_rings: Number of concentric rings.
    - num_repeats: Number of times the pattern repeats around the ring.
    - shift_per_ring: Phase shift per ring (shifts color sequence).
    - bg_luminance: Background luminance in cd/m².
    - max_lum_cd_m2: Maximum luminance of display in cd/m² (for normalization).
    - image_size: (width, height) in pixels.
    - color_mode: "grayscale", "blue_yellow", or "red_green".
    - element_order: List specifying the order of colors (overrides color_mode default).
    - luminance_values: List of custom luminance levels for colors.
    - rotation_direction: "counter_clockwise" (default) or "clockwise".
    - save_path: File path to save the generated PNG image.
    """

    # Normalize background luminance
    bg_luminance_norm = np.clip(bg_luminance / max_lum_cd_m2, 0, 1)

    # Define base RGB colors for blue-yellow and red-green modes
    custom_colors = {
        "blue": (15.3 / 255, 16.575 / 255, 1),  # Matches dark gray luminance
        "yellow": (183.6 / 255, 188.7 / 255, 0),  # Matches light gray luminance
        "red": (216.75 / 255, 0, 0),  # Matches dark gray luminance
        "green": (0, 1, 0)  # Matches light gray luminance
    }

    # Default luminance levels (used if no custom values provided)
    default_luminance_levels = [1, 2/3, 0, 1/3]

    # Use user-specified luminance values if provided
    luminance_levels = luminance_values if luminance_values else default_luminance_levels

    # Color mappings for grayscale and color modes
    color_mappings = {
        "grayscale": {
            1: (1, 1, 1),  # White
            2/3: (0.8, 0.8, 0.8),  # Light gray
            0: (0, 0, 0),  # Black
            1/3: (0.33, 0.33, 0.33)  # Dim gray
        },
        "blue_yellow": {
            1: (1, 1, 1),  # White
            2/3: custom_colors["yellow"],  # Yellow mapped to light gray luminance
            0: (0, 0, 0),  # Black
            1/3: custom_colors["blue"]  # Blue mapped to dark gray luminance
        },
        "red_green": {
            1: (1, 1, 1),  # White
            2/3: custom_colors["green"],  # Green mapped to light gray luminance
            0: (0, 0, 0),  # Black
            1/3: custom_colors["red"]  # Red mapped to dark gray luminance
        }
    }

    # Check if color_mode is valid
    if color_mode not in color_mappings:
        raise ValueError(f"Invalid color mode: {color_mode}. Choose from {list(color_mappings.keys())}")

    # Map luminance levels to colors with scaling for color modes
    color_sequence = []
    for level in luminance_levels:
        if color_mode == "grayscale":
            # For grayscale, we directly adjust luminance by scaling RGB values
            if level == 1:
                color_sequence.append(color_mappings["grayscale"][1])
            elif level == 2/3:
                color_sequence.append(color_mappings["grayscale"][2/3])
            elif level == 0:
                color_sequence.append(color_mappings["grayscale"][0])
            elif level == 1/3:
                color_sequence.append(color_mappings["grayscale"][1/3])
            else:
                # Custom luminance scaling for any other values
                color_sequence.append(adjust_luminance((0.5, 0.5, 0.5), level))  # Example custom scaling
        else:
            # For blue-yellow or red-green, apply luminance scaling
            base_color = color_mappings[color_mode][level]
            scaled_color = adjust_luminance(base_color, level)  # Scaling RGB values by luminance factor
            color_sequence.append(scaled_color)

    # Set default element order if none is provided
    if element_order is None:
        element_order = color_sequence

    # Reverse order for clockwise rotation
    if rotation_direction == "clockwise":
        element_order = element_order[::-1]

    # Create figure
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

        # Shift sequence per ring
        shifted_sequence = element_order[ring * shift_per_ring % len(element_order):] + \
                           element_order[:ring * shift_per_ring % len(element_order)]

        # Create wedges
        for i in range(num_segments):
            color = shifted_sequence[i % len(shifted_sequence)]
            theta1 = i * angle_step
            theta2 = (i + 1) * angle_step

            wedge = patches.Wedge(
                (0, 0), outer_radius, theta1, theta2, width=1 / num_rings, color=color
            )
            ax.add_patch(wedge)

    # Save as PNG
    plt.savefig(save_path, dpi=100, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
