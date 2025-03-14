import numpy as np

def ensure_image_is_color_image(img):
    if len(img.shape) == 2:
        new_img = np.ones((img.shape[0], img.shape[1], 3), dtype=img.dtype)
        new_img[:,:,0] = img
        new_img[:,:,1] = img
        new_img[:,:,2] = img
        return new_img
    return img