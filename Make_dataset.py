import openslide
import numpy as np
from PIL import Image

for folder_name in filtered_files:
    slide_path = r"/workspace/dataset/AI_DP/External/001-100/" + folder_name
    slide = openslide.OpenSlide(slide_path)

    level =  # define level externally or before use

    region_level = slide.read_region((0, 0), level, slide.level_dimensions[level])
    alpha_image = np.array(region_level)[:, :, 3]
    rgb_image = region_level.convert("RGB")
    gray_image = np.array(rgb_image.convert("L"))

    slide_width, slide_height = slide.level_dimensions[level]

    patch_size = 512
    step = patch_size

    for y in range(0, slide_height, step):
        for x in range(0, slide_width, step):
            if x + patch_size > slide_width or y + patch_size > slide_height:
                continue

            patch_alpha = alpha_image[y:y + patch_size, x:x + patch_size]
            patch_gray = gray_image[y:y + patch_size, x:x + patch_size]

            total_pixels = patch_alpha.size
            tissue_pixels = np.sum(patch_alpha == 255)
            tissue_ratio = (tissue_pixels / total_pixels) * 100

            white_pixels = np.sum(patch_gray > 240)
            white_ratio = (white_pixels / total_pixels) * 100

            if tissue_ratio == 100 and white_ratio < 50:
                patch = rgb_image.crop((x, y, x + patch_size, y + patch_size))
                patch.save(
                    r"/workspace/dataset/AI_DP/External_patches/"
                    + folder_name
                    + "/"
                    + folder_name
                    + "_"
                    + str(x)
                    + "_"
                    + str(y)
                    + ".png"
                )
