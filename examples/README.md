# Example

This folder provides an example setup for the usage of the energy toolkit.

## Set Up Python Virtual Environment

Before using the energy toolkit, it is recommended to create a Python virtual environment to isolate dependencies:

```bash
python3 -m venv .venv
```

**Explanation:**

* `.venv` is the folder where the virtual environment will be created. 
* This environment allows you to install packages without affecting your system Python installation.

Activate the virtual environment:

```bash
source .venv/bin/activate
```

**Explanation:**

* This command switches your current shell to use the Python environment inside `.venv`.
* You should see your prompt change, typically with `(.venv)` at the beginning.

Once activated, install the energy toolkit:

```bash
pip install energy-toolkit
```

## Compile Programs

Before you can measure energy consumption, you need to compile the programs you want to analyze. Use the following command:

```bash
./compile.sh
```

The compiled programs will be stored in the folder `./build`.

## Run Energy Measurements

Once the programs are compiled, you can measure their energy consumption using the toolkit:

```bash
sudo .venv/bin/energy-toolkit measure -r 10 -d 10 programs.yaml
```

**Explanation of the command:**

* `.venv/bin/energy-toolkit` refers to the executable inside the Python virtual environment. Make sure you have a virtual environment first.
* `measure` is the command to perform energy measurements.
* `-r 10` specifies the number of repetitions per program. In this example, each program will be run **10 times** to get a reliable average measurement.
* `-d 10` sets the amount of datapoints recorded by energy toolkit.
* `programs.yaml` is the configuration file listing the programs you want to measure and any parameters or inputs they require.

**Tip:** Adjust `-r` and `-d` depending on how long your programs take to execute and how precise you want the measurements to be.

## Plot Measurement Results

After collecting energy measurements, you can visualize the results:

```bash
sudo .venv/bin/energy-toolkit plot results
```

After executing the command, the resulting `.html` file will be located in the `results/` folder. Open it with your favourite browser.

**Explanation:**

* `plot` is the command that generates graphs from the collected measurements.
* `results` is the folder containing the measurement output files (created by the previous `measure` step).

