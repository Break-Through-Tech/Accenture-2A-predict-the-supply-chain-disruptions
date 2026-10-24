# How to Run This Project

A more detailed version of the quick start in the [README](README.md#-setup-and-installation). Follow the setup section for your OS, then go to [Running the notebooks](#running-the-notebooks).

Use Python 3.11–3.13. CatBoost may not have wheels for 3.14+ yet.

## macOS

**Prerequisites**

```bash
xcode-select --install        # command line tools, includes Git
```

1. Install [Homebrew](https://brew.sh/).
2. Install Python and `libomp`. LightGBM and XGBoost fail to load without `libomp`.

   ```bash
   brew install python@3.12 libomp
   ```

**Setup**

```bash
git clone https://github.com/Break-Through-Tech/Accenture-2A-predict-the-supply-chain-disruptions.git
cd Accenture-2A-predict-the-supply-chain-disruptions

python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Windows

**Prerequisites**

- Python 3.12 from [python.org](https://www.python.org/downloads/windows/). In the installer, tick **Add python.exe to PATH**.
- [Git for Windows](https://git-scm.com/download/win)
- [Microsoft Visual C++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe), which LightGBM, XGBoost and CatBoost need. Many machines already have it.

**Setup** (PowerShell)

```powershell
git clone https://github.com/Break-Through-Tech/Accenture-2A-predict-the-supply-chain-disruptions.git
cd Accenture-2A-predict-the-supply-chain-disruptions

py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If activation fails with "running scripts is disabled on this system", run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

In Command Prompt (cmd), activate with `.venv\Scripts\activate.bat` instead.

## Linux

**Prerequisites**

Ubuntu / Debian:

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip libgomp1
```

Fedora:

```bash
sudo dnf install git python3 python3-pip libgomp
```

`libgomp` is the OpenMP runtime LightGBM and XGBoost need. Most desktop installs already have it.

**Setup**

```bash
git clone https://github.com/Break-Through-Tech/Accenture-2A-predict-the-supply-chain-disruptions.git
cd Accenture-2A-predict-the-supply-chain-disruptions

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If your distro's `python3` is 3.14+, install 3.12 (e.g. `sudo apt install python3.12 python3.12-venv`) and use `python3.12 -m venv .venv`.

## Running the notebooks

With the venv active, run `jupyter notebook` from the repo root and open the `notebooks/` folder. In VS Code, open the repo folder, install the Python and Jupyter extensions, and select the `.venv` kernel.

Notebooks use relative paths (`../data/...`), so run them from inside `notebooks/`.

| Notebook | Purpose | Output |
|----------|---------|--------|
| `01_data_preparation` | Clean and merge raw CSVs | `data/preprocessed/supply_chain_disruption.csv` |
| `02_exploratory_analysis` | EDA | — |
| `02_1_correlation_tests` | Feature/target correlation checks | — |
| `02_2_feature_selection` | Feature selection, train/test split | `data/preprocessed/model_ready.csv` |
| `03_baseline_model_testing` | Compare 5 models with stratified 5-fold CV | — |
| `03_2_baseline_model_tuning_*` | Tune each model (any order); uses `tuning_setup.py` | `results/tuning/<model>/` |

All outputs are committed, so you can start at any notebook. The tuning notebooks are slow and overwrite `results/tuning/` when run.

To come back later, `cd` into the repo, activate the venv (`source .venv/bin/activate` or `.venv\Scripts\Activate.ps1`), and run `jupyter notebook`. After a `git pull`, rerun `pip install -r requirements.txt` in case dependencies changed.

## Troubleshooting

| Problem | OS | Fix |
|---------|----|-----|
| `ModuleNotFoundError` | All | The venv isn't active, or the notebook kernel isn't `.venv` |
| `FileNotFoundError: ../data/...` or `No module named 'tuning_setup'` | All | Run the notebook from inside `notebooks/` |
| CatBoost won't install | All | Use Python 3.12 or 3.13 and recreate `.venv` |
| `Library not loaded: @rpath/libomp.dylib` | macOS | `brew install libomp`, then restart the kernel |
| `python3.12: command not found` | macOS | Run `brew install python@3.12`, or use whichever `python3.x` (3.11–3.13) you have |
| `'python' is not recognized` / `py` not found | Windows | Reinstall Python with **Add python.exe to PATH** ticked |
| `DLL load failed` importing LightGBM, XGBoost or CatBoost | Windows | Install the Visual C++ Redistributable linked above |
| `ensurepip is not available` when creating the venv | Linux | `sudo apt install python3-venv` (or `python3.12-venv`) |
| `libgomp.so.1: cannot open shared object file` | Linux | `sudo apt install libgomp1` / `sudo dnf install libgomp` |
