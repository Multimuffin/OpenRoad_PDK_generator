# PDK Generator

This project is an assistant for quick generation of PDK platforms in OpenROAD.
It is currently designed for use with the Tower PDK, but additional PDKs will be added in the near future.

## Features
- Configuration file (config.mk) will be generated automatically
- A local directory structure is created with symbolic links to the source files

## Quick Start (for new users)

### Prerequisites
- Git
- Python 3.10 (or newer)
- Pyhton Venv (available at python3-venv)
- Access to the required Tower directories

### 1. Clone the Repository
```sh
git clone https://github.com/Multimuffin/OpenRoad_PDK_generator.git
cd OpenRoad_PDK_generator
```

### 2. Set up local virtual environment
```sh
python3.10 -m venv venv
source venv/bin/activate.csh  # für tcsh/csh
# oder: source venv/bin/activate      # für bash/zsh
```

### 3. Upgrade pip and setuptools
```sh
pip install --upgrade pip setuptools wheel
```

### 4. Install the PDK Generator Package
```sh
pip install .
```

### 5. Add the venv/bin directory to your PATH (if needed)
```tcsh
setenv PATH "$PATH":"$VIRTUAL_ENV/bin"
```

### 6. One-time user configuration (path specifications)
After installation execute:
```sh
pdk-setup
```
Follow the instructions and specify the paths to the tech and platform root directories. These are stored in `.pdkgenrc` in the current project folder.

### 7. Run the CLI Tool
```sh
pdk-gen
```

<!-- 
## Installation
Python 3.10 and the package `click` are required.

```sh
python3.10 -m pip install --user click
``` -->

## Usage
Start the CLI-Tool from the project directory:

```sh
pdk-gen
```

## Licence
ISDI-Austria
