import torch
import numpy as np
import PIL.Image
import dnnlib
import legacy
import os
import imageio

def load_generator(network_pkl):
    device = torch.device('cuda')
    with dnnlib.util.open_url(network_pkl) as f:
        G = legacy.load_network_pkl(f)['G_ema'].to(device)  # type: ignore
    return G

def interpolate(z1, z2, num_steps, easing_fn):
    """Interpolate between z1 and z2 with a custom easing function."""
    for i in range(num_steps):
        alpha = i / (num_steps - 1)
        alpha = easing_fn(alpha)  # Apply easing function
        z = (1 - alpha) * z1 + alpha * z2
        yield z

def ease_in_out(alpha):
    """Ease-in-out function: slow at start and end, fast in the middle."""
    return alpha ** 2 * (3 - 2 * alpha)

def generate_smooth_transitions(G, outdir, n=20, num_steps=200, fps=30):
    os.makedirs(outdir, exist_ok=True)
    video_path = f'{outdir}/full_transition.mp4'
    writer = imageio.get_writer(video_path, fps=fps)

    current_seed = 420  # Start with seed 0
    z1 = torch.from_numpy(np.random.RandomState(current_seed).randn(1, G.z_dim)).to(device)

    # Handle conditional vs. unconditional models
    if G.c_dim > 0:
        # Conditional model: create a dummy label (e.g., class 0)
        label = torch.zeros([1, G.c_dim], device=device)
    else:
        # Unconditional model: pass None
        label = None

    for i in range(n):
        # Generate a new random seed (not equal to current_seed)
        new_seed = np.random.randint(0, 1000000)
        while new_seed == current_seed:
            new_seed = np.random.randint(0, 1000000)

        # Generate latent vector for the new seed
        z2 = torch.from_numpy(np.random.RandomState(new_seed).randn(1, G.z_dim)).to(device)

        # Generate transition frames with easing
        frames = []
        for z in interpolate(z1, z2, num_steps, ease_in_out):
            img = G(z, label, truncation_psi=1.0, noise_mode='const')  # Pass label here
            img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
            img = img[0].cpu().numpy()
            frames.append(img)

        # Append frames to the video
        for frame in frames:
            writer.append_data(frame)

        # Update current_seed and z1 for the next interpolation
        current_seed = new_seed
        z1 = z2  # Start next interpolation from the end of the current one
        print(f'Appended transition {i + 1}/{n}: seed {current_seed}')

    # Finalize and save the video
    writer.close()
    print(f'Saved full video to {video_path}')
# Parameters
network_pkl = "../../drive/MyDrive/Colab Notebooks/network-snapshot-008657.pkl"
outdir = "out/"
n = 20  # Number of seeds
num_steps = 350  # Frames per transition
fps = 60  # Frames per second for the video

# Load the generator
device = torch.device('cuda')
G = load_generator(network_pkl)

# Create the full video
generate_smooth_transitions(G, outdir, n=n, num_steps=num_steps, fps=fps)