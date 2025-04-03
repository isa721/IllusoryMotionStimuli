import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_rotating_snake(num_rings=6, num_repeats=24, shift_per_ring=2, 
                            max_lum_cd_m2=100, image_size=(800, 800), 
                            color_mode="grayscale", element_order=None, luminance_values=None,
                            rotation_direction="counter_clockwise", save_path="rotating_snake.png",
                            min_inner_radius=0.00005):
    """
    Generates a customizable rotating snake illusion without a background.
    
    Parameters:
    -----------
    num_rings : int
        Number of concentric rings in the pattern
    num_repeats : int
        Number of pattern repetitions around each ring
    shift_per_ring : int
        Number of elements to shift the pattern between consecutive rings
    max_lum_cd_m2 : float
        Maximum luminance in cd/m²
    image_size : tuple
        Size of the output image in pixels (width, height)
    color_mode : str
        Color scheme to use ("grayscale", "blue_yellow", or "red_green")
    element_order : list
        Custom ordering of elements (overrides default if provided)
    luminance_values : list
        Custom luminance values (overrides default if provided)
    rotation_direction : str
        Direction of apparent rotation ("clockwise" or "counter_clockwise")
    save_path : str
        Path to save the generated image
    min_inner_radius : float
        Minimum radius for the innermost circle (prevents center distortion)
    """
    custom_colors = {
        "blue": (15.3 / 255, 16.575 / 255, 1),
        "yellow": (183.6 / 255, 188.7 / 255, 0),
        "red": (216.75 / 255, 0, 0),
        "green": (0, 1, 0)
    }

    default_luminance_levels = [1, 2/3, 0, 1/3]
    luminance_levels = luminance_values if luminance_values else default_luminance_levels

    color_mappings = {
        "grayscale": {
            1: (1, 1, 1),
            2/3: (0.8, 0.8, 0.8),
            0: (0, 0, 0),
            1/3: (0.33, 0.33, 0.33)
        },
        "blue_yellow": {
            1: (1, 1, 1),
            2/3: custom_colors["yellow"],
            0: (0, 0, 0),
            1/3: custom_colors["blue"]
        },
        "red_green": {
            1: (1, 1, 1),
            2/3: custom_colors["green"],
            0: (0, 0, 0),
            1/3: custom_colors["red"]
        }
    }

    if color_mode not in color_mappings:
        raise ValueError(f"Invalid color mode: {color_mode}. Choose from {list(color_mappings.keys())}")

    color_sequence = [color_mappings[color_mode][level] for level in luminance_levels]

    if element_order is None:
        element_order = color_sequence

    if rotation_direction == "clockwise":
        element_order = element_order[::-1]

    # Create figure with higher DPI for better resolution
    fig, ax = plt.subplots(figsize=(image_size[0] / 100, image_size[1] / 100), dpi=300)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_alpha(0)
    
    # Calculate ring radii - ensure proper spacing
    ring_radii = np.linspace(min_inner_radius, 1.0, num_rings + 1)

    # Draw center circle if needed
    if min_inner_radius > 0:
        center_circle = patches.Circle((0, 0), min_inner_radius, color=(1, 1, 1))
        ax.add_patch(center_circle)

    # Draw rings from outer to inner
    for ring_idx in range(num_rings):
        outer_radius = ring_radii[ring_idx + 1]
        inner_radius = ring_radii[ring_idx]
        
        # Calculate number of segments in this ring
        num_segments = len(element_order) * num_repeats
        angle_step = 360 / num_segments
        
        # Calculate shift for this ring
        ring_shift = (num_rings - ring_idx - 1) * shift_per_ring % len(element_order)
        shifted_sequence = element_order[ring_shift:] + element_order[:ring_shift]
        
        # Draw segments
        for i in range(num_segments):
            color = shifted_sequence[i % len(shifted_sequence)]
            theta1 = i * angle_step
            theta2 = (i + 1) * angle_step
            
            # Use Wedge patch for consistent rendering
            wedge = patches.Wedge(
                (0, 0), outer_radius, theta1, theta2, 
                width=outer_radius - inner_radius, 
                color=color,
                linewidth=0
            )
            ax.add_patch(wedge)

    # Save high-quality image
    plt.savefig(save_path, dpi=300, bbox_inches="tight", pad_inches=0, transparent=True)
    plt.close(fig)
    
    return save_path
                              
def create_rotated_frames(img_path, base_name, output_dir, shift_pixels, num_frames, rotation_direction="counterclockwise"):
    """
    Create rotated frames of the image and save them to the specified directory.
    
    Args:
        img_path: Path to the original image
        base_name: Base name of the stimulus (without extension)
        output_dir: Directory to save rotated frames
        shift_pixels: Number of pixels to shift per frame
        num_frames: Number of frames to generate
        rotation_direction: "clockwise" or "counterclockwise"
    """
    # Load the image
    img = Image.open(img_path)
    width, height = img.size
    center = (width // 2, height // 2)
    
    # Determine direction multiplier
    direction_multiplier = 1 if rotation_direction == "counterclockwise" else -1
    
    # Create and save each rotated frame
    for frame in range(num_frames):
        # Calculate rotation angle based on pixel shift
        radius = min(width, height) / 2
        circumference = 2 * np.pi * radius
        angle = direction_multiplier * (frame * shift_pixels / circumference) * 360
        
        # Rotate the image
        rotated_img = img.rotate(angle, center=center, resample=Image.BICUBIC)
        
        # Define output path with proper folder structure
        frame_output_dir = os.path.join(output_dir, f"{shift_pixels}_px", base_name)
        os.makedirs(frame_output_dir, exist_ok=True)
        
        output_path = os.path.join(frame_output_dir, f"frame_{frame+1}.png")
        rotated_img.save(output_path)
        print(f"Saved: {output_path}")
