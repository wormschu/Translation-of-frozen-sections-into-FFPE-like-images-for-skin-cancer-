# Translation-of-frozen-sections-into-FFPE-like-images-for-skin-cancer-

This repository provides a description of the generative AI framework used for translating frozen section images into FFPE-like representations for accurate assessment of skin cancer resection margins. The objective of this study is to reduce interpretive variability caused by freezing artifacts and improve diagnostic consistency by generating FFPE-like images in real time during surgery.

The associated manuscript describing the methodology, experimental setup, and validation results is currently under peer review.

Models Used in the Study (Unpaired Image Translation)

🔹 CycleGAN
👉 https://github.com/aitorzip/PyTorch-CycleGAN

🔹 CUT (Contrastive Unpaired Translation)
👉 https://github.com/taesungp/contrastive-unpaired-translation

🔹 SANTA (Unpaired Image-to-Image Translation With Shortest Path Regularization)
👉 https://github.com/Mid-Push/santa

🔹 AI-FFPE
👉 https://github.com/DeepMIALab/AI-FFPE

### Patch Extraction from Whole-Slide Images

Whole-slide images (WSIs) were processed using OpenSlide.  
Patches were extracted at pyramid level 2 (≈10× equivalent resolution).

Patch extraction criteria:

- Patch size: 512 × 512 pixels
- Only fully tissue-covered patches were retained (alpha channel = 255)
- Non-overlapping extraction

This preprocessing pipeline was applied identically to both Frozen and FFPE WSIs.

## Repository Status
The full training and implementation code used in this study will be made publicly available upon acceptance of the associated manuscript.

The current repository provides a description of the model configuration and preprocessing pipeline to facilitate methodological transparency during peer review.


## Final Model
Among the evaluated architectures (CycleGAN, CUT, SANTA, and AI-FFPE), 
CUT demonstrated the best overall performance based on quantitative 
metrics, downstream task evaluation, and qualitative expert assessment.  
Therefore, CUT was selected as the final model for whole-slide generation 
and clinical validation.

## CUT Training Configuration
- Input: 512 × 512 RGB patches  
- Domain A: Frozen section images  
- Domain B: FFPE images  
- Training: Unpaired translation (A → B)

### Optimization
- Optimizer: Adam  
- β₁ = 0.5  
- β₂ = 0.999  
- Initial learning rate: 2 × 10⁻⁴  
- Learning rate schedule: Linear decay  
- GAN objective: Least-Squares GAN (LSGAN)  

### Architecture
- Generator: ResNet blocks  
- Discriminator: PatchGAN  
- Normalization: Instance normalization  
- Loss weights:
  - λ_GAN = 1.0  
  - λ_NCE = 1.0  

### Training
- Iterations: 100,000

## Data Availability

A preview dataset containing one representative de-identified Frozen–FFPE whole-slide image (WSI) pair per skin cancer subtype (EMPD, Bowen’s disease, SCC, BCC, and melanoma) is publicly available on Zenodo:

- DOI: 10.5281/zenodo.18780726
