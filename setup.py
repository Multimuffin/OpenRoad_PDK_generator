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
            "pdk-gen = pdk_generator.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
