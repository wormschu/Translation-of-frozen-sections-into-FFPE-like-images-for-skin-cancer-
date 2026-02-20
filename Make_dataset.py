import os
import openslide
import numpy as np
from PIL import Image


def extract_patches_from_wsi(
    wsi_path,
    output_dir,
    level=2,
    patch_size=512,
    white_threshold=240,
    white_ratio_limit=50
):
    """
    Extract non-overlapping tissue patches from a whole-slide image (WSI).

    Parameters
    ----------
    wsi_path : str
        Path to the WSI file.
    output_dir : str
        Directory where extracted patches will be saved.
    level : int
        OpenSlide pyramid level (default: 2).
    patch_size : int
        Size of square patches (default: 512).
    white_threshold : int
        Grayscale threshold for white detection.
    white_ratio_limit : float
        Maximum allowed percentage of white pixels.
    """

    slide = openslide.OpenSlide(wsi_path)

    # Read full image at specified level
    region = slide.read_region(
        (0, 0),
        level,
        slide.level_dimensions[level]
    )

    rgb_image = region.convert("RGB")
    alpha_channel = np.array(region)[:, :, 3]
    gray_image = np.array(rgb_image.convert("L"))

    width, height = slide.level_dimensions[level]

    os.makedirs(output_dir, exist_ok=True)

    for y in range(0, height, patch_size):
        for x in range(0, width, patch_size):

            if x + patch_size > width or y + patch_size > height:
                continue

            patch_alpha = alpha_channel[y:y + patch_size, x:x + patch_size]
            patch_gray = gray_image[y:y + patch_size, x:x + patch_size]

            total_pixels = patch_alpha.size

            tissue_ratio = (
                np.sum(patch_alpha == 255) / total_pixels
            ) * 100

            white_ratio = (
                np.sum(patch_gray > white_threshold) / total_pixels
            ) * 100

            if tissue_ratio == 100 and white_ratio < white_ratio_limit:
                patch = rgb_image.crop(
                    (x, y, x + patch_size, y + patch_size)
                )

                patch_name = (
                    f"{os.path.basename(wsi_path)}_{x}_{y}.png"
                )

                patch.save(os.path.join(output_dir, patch_name))


if __name__ == "__main__":

    input_root = "path_to_wsi_directory"
    output_root = "path_to_patch_directory"

    for wsi_file in os.listdir(input_root):

        wsi_path = os.path.join(input_root, wsi_file)

        if not wsi_file.lower().endswith((".svs", ".tiff", ".mrxs")):
            continue

        save_dir = os.path.join(
            output_root,
            os.path.splitext(wsi_file)[0]
        )

        extract_patches_from_wsi(
            wsi_path=wsi_path,
            output_dir=save_dir,
            level=2,
            patch_size=512
        )
