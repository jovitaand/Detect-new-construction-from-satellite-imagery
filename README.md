# Space42 interview project: Building Change Review

A learning prototype to flag building-related changes in paired overhead images for analyst review. Independent portfolio project; not affiliated with Space42.

## What is ready
- VS Code workspace and Python environment instructions.
- Runnable RGB change baseline, dataset structural validator and synthetic demo.
- Detailed implementation outline, curated reading, data acquisition guide and interview prompts.

## What is not built yet
A trained neural model, real-data benchmark, anomaly model, multimodal fusion, ONNX export and web interface. These are learning milestones in docs/PROJECT_PLAN.md. No satellite dataset or model weights are bundled. Synthetic results are software checks only.

## Start on Windows (VS Code)
1. Extract the entire ZIP into a folder such as Documents/Projects. Open space42.code-workspace in VS Code. If using full Visual Studio instead, use Open Folder; workspace settings are for VS Code.
2. Install Python 3.11 or 3.12 and the Microsoft Python extension. Open Terminal > New Terminal at the project root.
3. Run the commands below. Explicit interpreter paths avoid PowerShell activation-policy changes.

```powershell
py -3.11 -m venv .venvv
.\.venvv\Scripts\python.exe -m pip install -r requirements.txt
.\.venvv\Scripts\python.exe scripts/demo.py
```

If you installed Python 3.12, replace `-3.11` with `-3.12`. In VS Code use Ctrl+Shift+P > Python: Select Interpreter > .venvv/Scripts/python.exe.

On macOS/Linux:
```bash
python3 -m venv .venvv
.venvv/bin/python -m pip install -r requirements.txt
.venvv/bin/python scripts/demo.py
```
Open outputs/synthetic_demo/before_after_overlay.png. Panels are before, after, predicted-change overlay. This deliberately easy synthetic example validates wiring only.

## Run on a real pair
Download LEVIR-CD following docs/DATA_SOURCES.md and arrange it as documented. Then:
```powershell
.\.venvv\Scripts\python.exe scripts/validate_dataset.py data/raw/levir_cd
.\.venvv\Scripts\python.exe scripts/baseline.py --before data/raw/levir_cd/val/A/example.png --after data/raw/levir_cd/val/B/example.png --label data/raw/levir_cd/val/label/example.png --out outputs/real_pair --threshold 0.2
```
Replace example.png with an actual matching filename. The threshold is illustrative: select it on validation data, then freeze it for test evaluation. A difference score is not confidence or a calibrated probability.

## Read next
1. docs/LEARNING_PATH.md
2. docs/DATA_SOURCES.md
3. docs/PROJECT_PLAN.md
4. docs/INTERVIEW_PREP.md

Base dependencies use broad compatibility ranges. After a successful local install save your actual environment with `python -m pip freeze > requirements-lock.txt` using the environment interpreter. GPU packages are deliberately deferred until your hardware is known; use https://pytorch.org/get-started/locally/ for the correct installation command. A CPU is sufficient for the baseline; GPU access is useful for training.

## Explain the code in an interview
Read [the code walkthrough](docs/CODE_WALKTHROUGH.md) for the pipeline, metrics, limitations, and interview wording.
