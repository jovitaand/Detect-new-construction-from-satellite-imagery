# Explain these decisions in the interview

- Why paired-image segmentation instead of single-image classification? It locates changes and supports review of the same location across time.
- Why a simple baseline? It establishes whether learned features add measurable value.
- What is leakage here? Overlapping crops/nearby scenes across splits, tuning on test, or contextual data from after the decision date.
- Why precision/recall rather than accuracy? Change is often sparse; accuracy can reward predicting no change everywhere.
- How is anomaly detection different? It ranks unusual observations; unusual does not necessarily mean construction or a labelled change.
- What makes data multimodal? Different kinds of information, such as imagery and dated geospatial attributes. Two RGB dates alone are temporal inputs.
- Why ONNX? A portable inference graph with runtime-specific execution; verify numerical parity and benchmark the actual target hardware.
- What fails in a UAE deployment? Resolution, sensor, climate, material, season and label-distribution shifts. Validate before claiming transfer.
- What if labels are limited? Begin with manual review and a baseline, prioritize uncertain or diverse examples for annotation, track agreement and hold out evaluation data.
- What changes at scale? Windowed reading, tiled inference with overlap, batching, queues, versioned data/models, idempotent jobs, monitoring and a human review loop. Spark is optional, not required for the small prototype.

Model card checklist: purpose; dataset/terms; split method; preprocessing; architecture; training settings; measured metrics; subgroup/domain errors; inference environment; limitations; model/version identifiers.

Prepare a 5-minute story: user problem (30 sec), data and labels (60 sec), baseline/model comparison (90 sec), error example (60 sec), deployment and next steps (60 sec). Use actual measured results only.
