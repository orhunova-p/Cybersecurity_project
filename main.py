"""
Adversarial Patches
Author: Polina Orhunova
This code generates stop sign using base_mask.txt and text_mask.txt, then apply three different attack strategies.
"""
import numpy as np
from PIL import Image, ImageDraw
import os

mask_dir = "details/attack/adversarial_yolo_master/masks"
base_mask = np.loadtxt(f"{mask_dir}/base_mask.txt")
text_mask = np.loadtxt(f"{mask_dir}/text_mask.txt")

size = 416

base_mask = np.array(Image.fromarray(base_mask).resize((size, size))).clip(0,1)
text_mask = np.array(Image.fromarray(text_mask).resize((size, size))).clip(0,1)

def create_base_stop_sign(size, base_mask, text_mask):

    img = np.zeros((size, size, 3), dtype=np.float32)
    
    img[:,:,0] = base_mask * 200
    img[:,:,1] = base_mask * 0
    img[:,:,2] = base_mask * 0
    
    # STOP text
    img[:,:,0] = np.maximum(img[:,:,0], text_mask * 255)
    img[:,:,1] = np.maximum(img[:,:,1], text_mask * 255)
    img[:,:,2] = np.maximum(img[:,:,2], text_mask * 255)
    
    alpha = np.clip(base_mask + text_mask, 0, 1) * 255
    
    rgba = np.dstack((img, alpha)).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')

base_sign = create_base_stop_sign(size, base_mask, text_mask)
base_sign.save("data/base_stop_sign.png")

# Subtle texture overlay - keeps red/white appearance but adds fine patterns
def create_patch1(base, size, base_mask, text_mask):
    arr = np.array(base.copy(), dtype=np.float32)

    np.random.seed(0)

    xx, yy = np.meshgrid(np.arange(size), np.arange(size))

    tile = size // 20
    pattern = ((xx // tile) + (yy // tile)) % 2
    red_variation = np.where(pattern == 0, 30, -20).astype(np.float32)

    noise = np.random.normal(0, 10, (size, size)).astype(np.float32)

    sign_only = (base_mask > 0) & (text_mask == 0)

    arr[:,:,0] = np.where(sign_only, np.clip(arr[:,:,0] + red_variation + noise, 0, 255), arr[:,:,0])
    arr[:,:,1] = np.where(sign_only, np.clip(arr[:,:,1] + noise * 0.3, 0, 255), arr[:,:,1])
    arr[:,:,2] = np.where(sign_only, np.clip(arr[:,:,2] + noise * 0.3, 0, 255), arr[:,:,2])

    # Restore STOP text in white
    arr[:,:,0] = np.where(text_mask > 0, 255, arr[:,:,0])
    arr[:,:,1] = np.where(text_mask > 0, 255, arr[:,:,1])
    arr[:,:,2] = np.where(text_mask > 0, 255, arr[:,:,2])

    return Image.fromarray(arr.astype(np.uint8), 'RGBA')

patch1 = create_patch1(base_sign, size, base_mask, text_mask)
patch1.save("data/My_Patch_1.png")


# Generate random colored shapes
def create_patch2(base, size, base_mask, text_mask):
    patch = base.copy()
    draw = ImageDraw.Draw(patch)

    np.random.seed(42)

    # Draw circles
    for _ in range(15):
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)
        r = np.random.randint(15, 50)

        color = (
            np.random.randint(0, 255),
            np.random.randint(0, 255),
            np.random.randint(0, 255),
            255
        )

        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

    # Draw lines
    for _ in range(8):
        x1, y1 = np.random.randint(0, size), np.random.randint(0, size)
        x2, y2 = np.random.randint(0, size), np.random.randint(0, size)

        color = (
            np.random.randint(0,255),
            np.random.randint(0,255),
            np.random.randint(0,255),
            255
        )

        draw.line([x1, y1, x2, y2], fill=color, width=10)

    arr = np.array(patch, dtype=np.float32)
    
    # Extract alpha channel from original
    base_arr = np.array(base, dtype=np.float32)
    alpha = base_arr[:,:,3]
    
    # Remove graffiti outside sign by zeroing RGB BUT keeping alpha
    for c in range(3):
        arr[:,:,c] = np.where((base_mask + text_mask) > 0, arr[:,:,c], 0)
    
    # Restore STOP text
    arr[:,:,0] = np.where(text_mask > 0, 255, arr[:,:,0])
    arr[:,:,1] = np.where(text_mask > 0, 255, arr[:,:,1])
    arr[:,:,2] = np.where(text_mask > 0, 255, arr[:,:,2])
    
    # Reattach correct alpha channel
    rgba = np.dstack((arr[:,:,:3], alpha))
    
    return Image.fromarray(rgba.astype(np.uint8), 'RGBA')

patch2 = create_patch2(base_sign, size, base_mask, text_mask)
patch2.save("data/My_Patch_2.png")

# Add sun reflection/glare on sign

def create_patch3(base, size, base_mask, text_mask):
    arr = np.array(base, dtype=np.float32)

    glare_centers = [
        (size//4, size//4),
        (3*size//4, size//3),
        (size//2, 2*size//3)
    ]

    for cx, cy in glare_centers:
        for x in range(size):
            for y in range(size):
                if base_mask[y, x] > 0:
                    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
                    glare = np.exp(-dist**2 / (2*(size//8)**2)) * 220

                    arr[y, x, 0] = np.clip(arr[y, x, 0] + glare, 0, 255)
                    arr[y, x, 1] = np.clip(arr[y, x, 1] + glare, 0, 255)
                    arr[y, x, 2] = np.clip(arr[y, x, 2] + glare, 0, 255)

    # Restore STOP text
    arr[:,:,0] = np.where(text_mask > 0, 255, arr[:,:,0])
    arr[:,:,1] = np.where(text_mask > 0, 255, arr[:,:,1])
    arr[:,:,2] = np.where(text_mask > 0, 255, arr[:,:,2])

    return Image.fromarray(arr.astype(np.uint8), 'RGBA')

patch3 = create_patch3(base_sign, size, base_mask, text_mask)
patch3.save("data/My_Patch_3.png")
