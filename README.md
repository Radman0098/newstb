# Ultra Max v2 - Trading AI System

## Overview
This project implements a high-frequency trading AI system designed with modular architecture and industrial-military standards. It leverages topological feature extraction and advanced machine learning models for market analysis.

## Structure
- `src/`: Core source code
  - `data/`: Data loading and preprocessing pipelines
  - `features/`: Feature extraction (Topological, Statistical)
  - `models/`: Machine learning model definitions
  - `strategies/`: Trading strategies and signal generation
  - `execution/`: Order management and simulation
  - `backtest/`: Backtesting engine
  - `utils/`: Shared utilities (logging, config)
- `data/`: Data storage
  - `raw/`: Raw market data (CSV)
  - `processed/`: Processed datasets
- `config/`: Configuration files
- `tests/`: Unit and integration tests
- `notebooks/`: Research and analysis notebooks

## Setup
### Python / venv
1. Create and activate venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install -U pip setuptools wheel
   ```

### Dependencies
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
   If `pip` is not available, install it first (e.g. `python3-pip` on Debian/Ubuntu).

### GPU Notes (RTX 50xx / sm_120)
- **PyTorch**: Stable CUDA wheels (مثلاً `cu124`) روی RTX 5080 (sm_120) ممکن است اجرا نشوند.
  اگر GPU شما sm_120 است، از nightly CUDA 13 استفاده کنید:
  ```bash
  python -m pip install --pre --upgrade torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/nightly/cu130
  ```

- **TensorFlow**: در حال حاضر `tensorflow==2.20.0` با GPU sm_120 ممکن است خطای runtime بدهد
  (وابسته به build و CUDA). اگر GPU TensorFlow مشکل داشت، موقتاً روی CPU اجرا کنید:
  ```bash
  CUDA_VISIBLE_DEVICES=-1 python -c "import tensorflow as tf; print(tf.__version__)"
  ```
  (برای LSTM/PatchTST این پروژه، مسیر اصلی روی PyTorch است.)

3. Configure settings in `config/settings.yaml`.
4. Run the system via `main.py`.

### Quick Health Check
برای چک سریع نصب Torch/TF/LSTM/PatchTST:
```bash
python scripts/check_ml_stack.py
```

## Principles
- **Modularity**: Components are loosely coupled.
- **Performance**: Optimized computations.
- **Reliability**: Strict error handling and logging.


