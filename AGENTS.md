# Codex project context: Space42 computer vision interview project

Read this file before making project changes. Treat it as the current project brief. Help the user learn as you build: explain each step in plain language, connect code to the underlying idea, and give commands that work in Windows PowerShell. Do not assume the user is already comfortable with Python or machine learning.

## Purpose

This is a hands-on portfolio project to prepare for a Space42 Data Scientist interview. The job description emphasizes large and multimodal data, computer vision, pattern and anomaly detection, statistical and machine-learning methods, data quality, communication with nontechnical stakeholders, production integration, documentation, and ONNX model formats.

The project idea is an analyst-facing system that compares two overhead images and flags candidate building changes for review. It should demonstrate a full reasoning chain: a real problem, data quality, a simple baseline, a measured learned model, error analysis, and an inference/deployment path. It is an independent learning project and is not affiliated with Space42. Do not imply the user has internal Space42 data or that this exact project is a Space42 product.

Space42 public materials describe geospatial intelligence as combining Earth-observation data with AI and other sources to support decisions. Use that context to motivate the project, without claiming knowledge about this vacancy's internal team or systems.

## Key problem framing

- The first dataset is LEVIR-CD: paired high-resolution optical images with binary building-change masks. Its labels include building additions and removals. They do not directly identify new construction alone.
- A before/after RGB pair is temporal data, not by itself multimodal data. A genuine multimodal extension could combine imagery with appropriately dated geospatial context, or optical with SAR, provided there are valid aligned data and labels.
- Sentinel-2 is a separate later domain experiment at substantially coarser resolution than LEVIR-CD. A model trained on LEVIR-CD must not be assumed to transfer. Do not present 10m imagery as building-level accuracy evidence.
- Anomaly ranking and supervised change detection are related but distinct. An unusual tile is not automatically a real building change. Do not claim anomaly detection is implemented until there is a real method and evaluation.
- The synthetic demo is only a software smoke test. It is not satellite data, a trained model, or evidence of real-world performance.

## Current status and next milestone

The starter project and Python environment are set up on the user's Windows laptop. The user reported the project root as:

`C:\Users\jovit\Downloads\space42-change-detection\space42-change-detection`

The user's environment folder is named `.venvv` (two v's at the end), because that is the name used when they created it. The README originally says `.venv`; those commands will fail unless the user renames the environment. Use `.venvv\Scripts\python.exe` in current Windows PowerShell instructions.

The user combined pip-install and demo commands on one line once, causing pip to parse `scripts/demo.py` as a package requirement. Give one command at a time and explicitly tell them to press Enter after each command.

Already included: a synthetic baseline demo, an RGB absolute-difference baseline, a structural dataset validator, project documentation and starter workspace configuration. Not yet implemented: the LEVIR-CD training pipeline, neural network, real-data benchmark, anomaly model, multimodal fusion, ONNX export, or web app. Do not imply these are already complete.

Immediate project milestone:
1. Confirm the demo runs from project root using `.venvv`.
2. Acquire LEVIR-CD following its current provider instructions and use terms.
3. Arrange files as `data/raw/levir_cd/{train,val,test}/{A,B,label}/filename.png` (adapt `val` if source uses another name, preserving the source split).
4. Run `scripts/validate_dataset.py`.
5. Visually inspect 10–20 paired images and masks and make a small data card: dimensions, partitions, label meaning, class balance, alignment/lighting issues, and limitations.
6. Run the RGB baseline on real validation pairs; inspect false positives and misses before writing a training loop.

Do not download or redistribute the LEVIR-CD imagery on the user's behalf without a clear request. The dataset provider states academic-use-only terms and prohibits commercial use; follow the source terms and do not bundle the imagery into a public commercial demo. Keep credentials and tokens out of the repository.

## Repository map

- `README.md`: Windows setup, run instructions, dataset layout, and project entry points.
- `docs/LEARNING_PATH.md`: curated learning sequence and exercises.
- `docs/DATA_SOURCES.md`: LEVIR-CD and later Sentinel-2 / optional OpenStreetMap sources, layout, quality issues, and restrictions.
- `docs/PROJECT_PLAN.md`: staged implementation and evaluation plan.
- `docs/INTERVIEW_PREP.md`: expected interview questions and model-card checklist.
- `scripts/demo.py`: creates a trivial synthetic pair and invokes the baseline as a smoke test.
- `scripts/baseline.py`: RGB mean absolute difference, thresholded mask, overlays, and optional single-image metrics. Difference score is not calibrated probability.
- `scripts/validate_dataset.py`: checks expected filenames, dimensions, and simple binary mask encoding; it does not verify registration, duplicate leakage, label quality, or geographic independence.
- `data/raw/`: immutable source data; never silently rewrite raw imagery.
- `data/processed/`: reproducible derived/cropped data.
- `outputs/`: metrics, plots, predictions, error examples, and reports.
- `models/`: learned checkpoints and exported models after they exist.
- `notebooks/`: exploratory work; move stable reusable code into scripts or modules.
- `requirements.txt`: baseline dependencies. `requirements-ml.txt`: optional later-stage packages. Install PyTorch separately according to machine hardware and the official PyTorch selector.
- `space42.code-workspace` and `.vscode/`: VS Code setup and debug configuration.
- `AGENTS.md`: this Codex-facing project context.

A separate `PyTorch_Basics_Learning_Guide.docx` was created for the user. It covers tensors, model building, loss, autograd, training loops, data loaders, CPU/GPU, evaluation, saving weights, and a small learning exercise. It is a companion learning resource, not currently known to be inside the project folder. Use it when the user asks about PyTorch fundamentals.

## Project stages

### Stage 1 — Data understanding
Follow the existing data guide, inspect pairs/masks and document data limitations. Keep parent image and geography identity when making crops. Never randomly split crops from the same parent scene across train and test.

### Stage 2 — Baseline and evaluation
Run the simple RGB-difference baseline. For the full validation/test comparison, aggregate TP, FP, FN across images and also report per-image metrics. Tune thresholds only on validation; freeze choices before test. Report precision, recall, F1, and IoU. Accuracy alone is misleading under sparse change labels. Save representative correct, false-positive, and missed examples.

### Stage 3 — Neural change segmentation
Once the user understands the data and baseline, implement a PyTorch Dataset for paired images and masks, then a compact Siamese encoder-decoder (shared encoder for both dates, feature comparison, decoder to a pixel mask). Start with small reproducible batches/crops. Apply identical geometric transforms to both dates and the mask; use nearest-neighbor interpolation for masks. Begin with a tiny overfit check, then train/validate. Record seed, partitions, transforms, optimizer, losses, package versions and hardware. Select checkpoints on validation data, never test. Explain each new code file before asking the user to run it.

### Stage 4 — Optional anomaly ranking and multimodal extension
Only after the supervised baseline/model is measured. Define what “normal” means; use training data for fitting and validation/test for assessment. Make clear anomaly scores are rankings, not probabilities or labels. If adding dated geospatial features or SAR, compare against imagery-only on the same geographic split. Do not use future context that leaks the answer. If appropriate aligned data are unavailable, document the extension as future work.

### Stage 5 — Inference/deployment
Export an implemented model to ONNX, compare ONNX Runtime output with PyTorch on held-out examples, record any numerical difference, and benchmark on actual hardware with repeated runs. Then build a simple analyst demo with before/after, mask overlay, threshold and review status. Do not display a map without real georeferencing. Distinguish model score, calibrated probability (only if calibration was measured), and anomaly score.

### Stage 6 — UAE extension (stretch goal)
Use Sentinel-2 L2A only as a separate experiment. Document dates, AOI, item IDs, bands, CRS, grid, resolution, nodata and cloud-mask handling. Align the images correctly; use nearest-neighbor for categorical masks. Obtain suitable local labels before making accuracy claims. Treat SAR as a distinct modality requiring its own data and preprocessing.

## Learning and communication preferences

The user is building interview skills and benefits from a beginner-friendly, sequential explanation. Avoid dumping a large codebase or multiple commands at once. For each task:
1. State what the next step accomplishes.
2. Explain the key concept with a concrete analogy or small example when helpful.
3. Give the exact PowerShell command(s), one per line, using the user's current `.venvv` environment.
4. Tell the user what output to expect and how to interpret it.
5. Troubleshoot from the actual error text; do not repeat commands with the wrong environment folder or working directory.

Prefer measured evidence over impressive claims. Separate completed work, observed results, assumptions and proposed future work.

## Source links

- LEVIR-CD project/download page: https://justchenhao.github.io/LEVIR/
- LEVIR-CD repository and use terms: https://github.com/justchenhao/LEVIR
- LEVIR-CD original paper: https://levir.buaa.edu.cn/publications/remotesensing-798405-eng.pdf
- Copernicus Browser: https://browser.dataspace.copernicus.eu/
- Copernicus STAC docs: https://documentation.dataspace.copernicus.eu/APIs/STAC.html
- Sentinel-2 L2A details: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S2L2A.html
- PyTorch fundamentals: https://docs.pytorch.org/tutorials/beginner/basics/intro.html
- PyTorch transfer learning: https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial
- ONNX Runtime Python: https://onnxruntime.ai/docs/get-started/with-python.html
- Space42 public GIQ viewpoint: https://space42.ai/en/foresight-viewpoint/articles/2025/giq---from-manual-analysis-to-ai-driven-insight/

## Interview-ready final evidence

Aim to finish with a reproducible code repository, experiment table comparing baseline and trained model on the same held-out split, honest metrics, several error case studies, an architecture diagram, a concise model card, a working inference demo, and a short presentation. Clearly say what you built versus what is only proposed. Explain how a review queue reduces analyst workload and how you chose its threshold based on review capacity or error costs.

## Starter prompt for a new Codex session

“Read `AGENTS.md` and the project docs before changing files. Continue the Space42 building-change project from its current status. My immediate goal is to [state the current step]. Explain the concept first, then make only the changes needed for this step. Use my Windows PowerShell environment `.venvv`, provide one command at a time, and tell me how to verify its output. Do not claim results that I have not measured.”
