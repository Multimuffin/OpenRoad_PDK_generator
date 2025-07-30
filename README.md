# PDK Generator

This project is an assisstant for quick generation of PDK platforms in OpenROAD.

## Features
- Configuration file (config.mk) will be generated automatically
- A local directory structure is created with symbolic links to the source files

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
