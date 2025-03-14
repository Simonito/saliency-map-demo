import numpy as np
from scipy import io
import cv2
import os

def saliencyimage(img, scale):
    original_height, original_width = img.shape[:2]

    # Load ICA basis functions, filters are zero summed
    stats_mat_file = os.path.join(os.path.dirname(__file__), "stats.mat")
    print(stats_mat_file)
    stats = io.loadmat(stats_mat_file)
    B1 = stats['B1']
    sigmas = stats['sigmas'].flatten()
    thetas = stats['thetas'].flatten()
    
    d = B1.shape[0]  # number of filters
    D = B1.shape[1]  # color filter streched length
    fsize = D // 3   # length of filter at each channel
    psize = int(np.sqrt(fsize))  # square filter
    
    # preprocess image
    if scale != 1:
        # img = resize(img, (round(img.shape[0] * scale), round(img.shape[1] * scale)),
        #             mode='constant', anti_aliasing=True)
        img = cv2.resize(img, (round(img.shape[1] * scale), round(img.shape[0] * scale)),
                         interpolation=cv2.INTER_LINEAR)
    
    img = img.astype(np.float64)
    img = img / np.std(img.flatten())
    height = img.shape[0]
    width = img.shape[1]
    
    # take image patches
    N = (height - psize + 1) * (width - psize + 1)
    patches = np.zeros((D, N))
    i = 0
    
    # Exactly match MATLAB's reshape behavior
    for r in range(height - psize + 1):
        for c in range(width - psize + 1):
            patch = img[r:r+psize, c:c+psize, :]
            patches[:, i] = np.reshape(patch, (D,), order='F')
            i += 1
    
    # filter responses
    S = B1 @ patches
    
    # saliency map
    smap = np.zeros((1, S.shape[1]))
    for i in range(d):
        smap = smap + (np.abs(S[i:i+1, :]) / sigmas[i]) ** thetas[i]
    
    # Match MATLAB's reshape behavior
    smap = np.reshape(smap, (width - psize + 1, height - psize + 1), order='F').T
    
    if smap.shape != (original_height, original_width):
        # smap = resize(smap, (original_height, original_width),
        #               mode='constant', anti_aliasing=True)
        smap = cv2.resize(smap, (original_width, original_height), interpolation=cv2.INTER_LINEAR)

    return smap