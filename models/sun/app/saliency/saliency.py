import numpy as np
from .saliencyimage import saliencyimage

def make_saliency_map(img: np.ndarray) -> np.ndarray:
    if img.shape[-1] == 4:
        img = img[:, :, :3]  # Keep only RGB channels, drop alpha

    if len(img.shape) == 2:
        img = np.stack([img] * 3, axis=2)
    inimage = img.astype(np.float64) / 255.0
    print(f"Image shape after color conversion: {inimage.shape} | original: {img.shape}")

    infomap = saliencyimage(inimage, 1)

    # Normalize and convert to image
    output_image = (infomap - np.min(infomap)) / (np.max(infomap) - np.min(infomap))
    output_image = (output_image * 255).astype(np.uint8)

    return output_image