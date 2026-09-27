# Explain the project in an interview

## A short introduction

> I am building a prototype that flags candidate building changes between two overhead images for analyst review. I started with an RGB-difference baseline to establish an interpretable reference before training a neural network. The synthetic test verifies that the pipeline works; real-data evaluation is the next step.

This is an independent learning project, not a Space42 product. A trained model and measured real-data performance have not yet been demonstrated.

## 1. Synthetic smoke test: `scripts/demo.py`

The script creates a 256 by 256 RGB image and copies it to create a second date. It adds a bright rectangle to the second image:

```python
a = np.full((256, 256, 3), 70, dtype=np.uint8)
a[30:90, 25:90] = 150
b = a.copy()
b[130:195, 140:220] = 230
```

The three array dimensions represent height, width, and colour channels. A reference mask records the exact changed region:

```python
truth = np.zeros((256, 256), dtype=np.uint8)
truth[130:195, 140:220] = 255
```

Black means unchanged and white means changed. The script runs the baseline and asserts that IoU equals 1.0. The observed synthetic check detected all 5,200 changed pixels with zero false positives and zero misses. This deliberately easy example checks software wiring; it is not satellite imagery or evidence of real-world accuracy.

Interview wording: "I use a synthetic example with a known answer to check the prediction and evaluation code before applying it to real data."

## 2. RGB-difference baseline: `scripts/baseline.py`

Images are converted to RGB arrays of floating-point numbers and divided by 255, placing values between zero and one. The script checks matching dimensions, although that does not establish geographic alignment. Corresponding pixels must represent the same ground location.

The main calculation is:

```python
score = np.abs(b - a).mean(axis=2)
pred = score > threshold
```

For each pixel, subtract the before and after channel values, take absolute differences, and average across red, green, and blue. Threshold that score to create a binary prediction mask. Absolute differences detect both brightening and darkening.

For example, channel differences of 0.3, 0.2, and 0.1 average to 0.2. Mathematically, a score exactly equal to a threshold of 0.2 is not flagged because the comparison is strictly greater than. Floating-point representation can affect comparisons close to a boundary.

The threshold is an operating choice. A lower threshold generally flags more pixels, potentially increasing both recall and false positives. Select it on validation data and freeze it before test evaluation. A score of 0.8 is not an 80% probability of building change.

Interview wording: "This method requires no training and is easy to interpret, but it measures appearance differences rather than understanding buildings."

## 3. Evaluation

`evaluate()` compares the predicted and reference masks pixel by pixel:

| Count | Meaning |
|---|---|
| TP | Changed pixel correctly detected |
| FP | Unchanged pixel incorrectly flagged |
| FN | Changed pixel missed |
| TN | Unchanged pixel correctly rejected |

| Metric | Formula | Interpretation |
|---|---|---|
| Precision | TP / (TP + FP) | How many flagged pixels were correct? |
| Recall | TP / (TP + FN) | How much labelled change was found? |
| F1 | 2TP / (2TP + FP + FN) | Balance between precision and recall |
| IoU | TP / (TP + FP + FN) | Intersection divided by union of the two change masks |

The code returns `None` for an undefined ratio with a zero denominator. These are pixel-level metrics, not building-count accuracy. Because changes can be sparse, predicting everything as unchanged may produce high accuracy while detecting no changes.

The current baseline supports optional single-pair metrics. A full dataset benchmark still needs aggregate TP, FP, and FN across images, plus per-image results.

## 4. Inspectable outputs

- `difference.png`: continuous difference scores rendered as an image.
- `prediction.png`: thresholded binary mask.
- `before_after_overlay.png`: before, after, and red predicted-change overlay.
- `metrics.json`: method, threshold, predicted changed-pixel fraction, and metrics when labels are supplied.

Interview wording: "Metrics summarize performance, while overlays let me investigate shadows, vegetation, misalignment, and missed buildings."

## 5. Dataset validator: `scripts/validate_dataset.py`

For train, validation, and test, the script checks matching PNG filenames in `A`, `B`, and `label`, matching dimensions within each triplet, and supported binary mask values (0, 1, 255). It does not verify alignment, label accuracy, duplicate leakage, or geographic independence. Those require further checks and visual inspection.

## 6. Download helper: `scripts/download_levir.py`

The helper uses Windows curl to download the original provider archives, resume partial transfers, and retry failures. It checks ZIP CRCs before extraction and verifies existing images against archive CRCs before reusing them. CRC checks detect accidental corruption; they are not independent cryptographic proof of provenance.

Files are arranged as `data/raw/levir_cd/{train,val,test}/{A,B,label}/filename.png`, preserving provider partitions. The script records the source and invokes the structural validator after all downloads complete. This is data preparation, not model training.

LEVIR-CD labels building additions and removals. Two RGB dates are temporal inputs, not by themselves multiple modalities. The provider restricts the dataset to academic use and prohibits commercial use: https://justchenhao.github.io/LEVIR/

## 7. Limitations and next steps

RGB differences can respond to lighting, shadows, vegetation, and misregistration even when no building changes. Next, inspect real pairs and masks, evaluate the baseline on validation data, select a threshold, and examine false positives and misses. Then implement and evaluate a learned change-segmentation model on the same partitions.

Keep crops from the same parent image in one split. Do not tune on test data. A future Siamese encoder-decoder could share an encoder across the two dates and compare their features, but that model is not implemented yet. ONNX export, anomaly ranking, multimodal fusion, and a web application are also future work.

## A concise closing statement

> The project currently demonstrates a reproducible baseline and evaluation pipeline. I verified the software with a synthetic test, and I am preparing the real dataset. The next evidence I need is measured validation performance and error analysis before claiming that a learned model improves the result.
