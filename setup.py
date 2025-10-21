from setuptools import setup, find_packages, Extension

# Define our custom msr reader extension
msr_extension = Extension('energy_toolkit.msr_reader', sources=['energy_toolkit/msr_reader.c'])

setup(
    name="energy_toolkit",
    version="1.0.2",
    packages=find_packages(),
    description="Provides functionality to benchmark a program and measure time and energy during execution.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Maximilian Krebs, Ben Hermann",
    author_email="maximilian.krebs@cs.tu-dortmund.de",
    url="https://github.com/printerboi/energy-toolkit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "py-cpuinfo>=9.0.0",
        "click>=8.3.0",
        "PyYAML>=6.0.3",
    ],
    entry_points={
        "console_scripts": [
            "energy-toolkit = energy_toolkit.cli:cli",
        ],
    },
    ext_modules=[msr_extension]
)
