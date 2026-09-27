# Implementation outline

## Goal and success criteria
Produce a review queue of likely building changes from paired images. The first deliverable is a measured LEVIR-CD learning prototype. New construction is a subset of building change, not interchangeable with the dataset's label. Operational value is fewer irrelevant alerts for a given review budget. No target performance is claimed before evaluation.

Suggested pace: 4-6 weeks at 8-12 hours/week if Python fundamentals are comfortable; allow longer if PyTorch is new. These are planning estimates, not a training-runtime promise.

## Stage 1 — Understand the data (week 1)
Run the demo, download the benchmark, validate structure and inspect 20 paired samples with masks. Record class imbalance, acquisition differences and label ambiguities. Preserve source partitions and parent-image identity before making any crops. Deliver a data card and illustrated error hypotheses.

## Stage 2 — Establish a baseline (week 2)
Use scripts/baseline.py on real validation pairs. Extend evaluation to aggregate TP/FP/FN over all images, calculate global metrics and also report per-image distributions. Compare several thresholds on validation only. Freeze one and evaluate test once. RGB differences will flag lighting and vegetation; these failures justify learning semantic features. Save 5 correct detections, 5 false positives and 5 missed changes.

## Stage 3 — Train and fine tune (weeks 3-4)
Implement a PyTorch Dataset yielding paired normalized RGB tensors and binary masks. Crop to 256x256 to start, preserving parent split; apply the same geometric augmentation to BOTH images and mask. Use nearest-neighbour resizing for masks. Build a shared pretrained encoder for before/after images, combine corresponding features by concatenation or absolute difference, and decode to a single-channel change logit map (a small Siamese encoder-decoder).

First freeze the encoder, then unfreeze with a lower learning rate. Train with binary cross entropy with logits; consider Dice loss after the basic run works. Match normalization to pretrained weights. Check predictions on a tiny training subset before a full run. Log seeds, transforms, learning rate, batch size, validation loss and GPU memory. Save the checkpoint selected on validation, not test. Compare against the baseline using exactly the same held-out data.

Deliver training code, checkpoint, learning curves, prediction overlays and measured F1/IoU/precision/recall. No checkpoint is included in this starter.

## Stage 4 — Anomaly detection and multimodal extension (optional, week 5)
Extract tile embeddings from the trained encoder or engineered change features. Fit Isolation Forest on training data representing the selected reference population. If using nominal unchanged reference tiles, use only training labels to select them. Evaluate the top-K unusual tiles through labels and manual review; compare ranking to the baseline. Explain that anomaly scores are not construction probabilities and that change detection does not by itself satisfy an anomaly-detection claim.

For multimodal fusion add trustworthy, dated geospatial context at the tile level. Compare imagery-only and imagery-plus-context on identical geographic splits. Use a simple late-fusion model before a complex network. Quantify whether context helps; exclude future information. If unavailable, leave this stage explicitly unimplemented.

## Stage 5 — Export and analyst demo (week 6)
Export the trained network to ONNX. Test numerical closeness and thresholded segmentation metrics on representative held-out inputs; document tolerances, supported shapes and any discrepant masks. Measure preprocessing, inference and postprocessing separately, report hardware, warmup and batch size. Avoid a speed claim based on one run.

Create a Streamlit interface with paired image upload, overlay, score threshold and review status. Use an image viewer for benchmark PNGs; do not invent map coordinates. Add a geographic map only after real georeferencing is available. Separate model score, calibrated probability (if implemented) and anomaly score. Provide model card and reproducible inference instructions.

## Stage 6 — UAE / Sentinel-2 (stretch)
Follow DATA_SOURCES.md. Build a separate area-level workflow, prepare local labels and validate domain transfer. Discuss SAR as an additional future modality; it needs sensor-specific preprocessing and training. Do not promise that an optical model will work on radar.

## Statistical and operational evaluation
Compare baseline and model per parent image. Bootstrap paired differences at parent-image or region level, not independent pixels; describe small-sample limitations. Tune thresholds on validation according to review capacity or costs. Precision@K measures how useful a daily review queue is. False alerts per square kilometre need reliable physical area, a defined alert object (connected component or tile) and valid coverage; pixel false-positive rate is not the same metric. Benchmark change labels cannot establish a production anomaly ground truth.

## Final interview evidence
A reproducible repository, one-page architecture overview, experiment table, three error case studies, model card, short demo and five-slide presentation. Explain what you actually implemented, what failed and what remains a proposal. A notebook alone is insufficient evidence of deployment.
