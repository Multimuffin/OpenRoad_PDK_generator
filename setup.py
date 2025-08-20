import setuptools

setuptools.setup(
    name="pdk_generator",
    version="0.1.0",
    description="PDK Platform Generator",
    author="tragicomix",
    python_requires=">=3.8",
    packages=setuptools.find_packages(),
    install_requires=[
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            # <skriptname> = <modul>:<funktion>
            "pdk-gen = pdk_gen.cli:main",
            "pdk-setup = pdk_gen.setup_config:run_setup",  # <--- Setup-Kommando für User-Konfiguration
            "pdk-unused = pdk_gen.unused_code_detector:main",  # <--- Unused code detection
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
