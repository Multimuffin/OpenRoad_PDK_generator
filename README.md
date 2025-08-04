# PDK Generator

This project is an assistant for quick generation of PDK platforms in OpenROAD.

## Features
- Configuration file (config.mk) will be generated automatically
- A local directory structure is created with symbolic links to the source files

## Quick Start (for new users)

### Prerequisites
- Python 3.10 (or newer)
- tcsh shell (recommended for environment activation)
- Access to the required tech directories

### 1. Clone the Repository
```sh
git clone https://github.com/Multimuffin/OpenRoad_PDK_generator.git
cd OpenRoad_PDK_generator
```

### 2. Create and Activate a Virtual Environment
```sh
python3.10 -m venv venv
source venv/bin/activate.csh   # For tcsh users
```

### 3. Upgrade pip and setuptools
```sh
pip install --upgrade pip setuptools wheel
```

### 4. Install the PDK Generator Package
```sh
pip install .
```

### 5. Add the venv bin directory to your PATH (if needed)
```tcsh
setenv PATH "$PATH":"$VIRTUAL_ENV/bin"
```
Or, if `$VIRTUAL_ENV` is not set:
```tcsh
setenv PATH "$PATH":/full/path/to/your/venv/bin
```

### 6. Run the CLI Tool
```sh
pdk-gen
```
Or, alternatively:
```sh
python -m pdk_gen.cli
```

### Notes
- Make sure your tech directories are accessible as expected by the tool.
- If you use bash/zsh, activate the environment with `source venv/bin/activate`.

## Installation
Python 3.10 and the package `click` are required.

```sh
python3.10 -m pip install --user click
```

## Usage
Start the CLI file from the project directory:

```sh
python3.10 -m pdk_generator.cli
```

## Licence
ISDI-Austria
