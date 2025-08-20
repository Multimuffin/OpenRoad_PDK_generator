# PDK Generator

This project is an assistant for quick generation of PDK platforms in OpenROAD.
It was designed exclusively for tower and dbhitek technologies.

## Features
- Configuration file (config.mk) will be generated automatically
- A local directory structure is created with symbolic links to the source files
- **Unused code detection** - Identify and clean up unused functions, imports, files, and variables

## Quick Start

### Prerequisites
- Git
- Python 3.10 (or newer)
- Python Venv (available at python3-venv)
> It is recommended running the program in a virtual environment, in order to avoid conflicts with globally installed python packages.
- Access to the required Tower directories

### 1. Clone the Repository
```sh
git clone https://github.com/Multimuffin/OpenRoad_PDK_generator.git
cd OpenRoad_PDK_generator
```

### 2. Set up local virtual environment
```sh
python3.10 -m venv venv
source venv/bin/activate.csh
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

## Work flow

At the beginning, the user must specify the source paths so that the script can function properly. If a technology is not required, it can be left blank.

After executing the main script, the user is asked which technology, metal stack, lib files, etc. they want to use. The program then performs the following steps:
- Creates a cdl, gds, lef, lib folder with symbolic links to the original files.
- Copies the config.mk template and updates its paths.
- Copies pdn.tcl, setRC.tcl, make_tracks.tcl, fastroute.tcl, and constraint.sdc (These files are **NOT** modified).

## Disclaimer

Up to this point, the script runs, but some features such as the pdn.tcl files or setRC.tcl are not implemented. However, the templates that originate in the src folder provide a good orientation for further implementation.

## License
ISDI-Austria
