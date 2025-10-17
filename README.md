# Energy Toolkit

`energy-toolkit` is a Python module designed to facilitate the execution of programs while measuring their energy consumption and execution time. This toolkit provides users with valuable insights into the performance of their code, allowing for better resource management and optimization.

## Features

- Execute Python functions or scripts
- Measure energy usage during execution
- Measure execution time
- Return a comprehensive set of metrics upon completion

## Requirements

- Python 3.6 or a newer version
- Linux OS
- Intel/AMD CPU offering RAPL registers

## Installation

You can install the `energy-toolkit` module via pip:

```bash
pip install energy-toolkit
```

## Command Line Usage

The `energy-toolkit` also provides a powerful **command-line interface (CLI)** for measuring energy consumption and validating program configurations.
This interface is built with [Click](https://click.palletsprojects.com/), offering a clean and intuitive user experience.

### Overview

To use the CLI, simply run:

```bash
energy-toolkit [COMMAND] [OPTIONS]
```

Run the following command to view all available options:

```bash
energy-toolkit --help
```

---

### 1. Measure Command

The `measure` command is used to **measure the energy consumption** and execution performance of target executables defined in a program configuration file (`programs.yaml`).

```bash
energy-toolkit measure PROGRAMS [OPTIONS]
```

#### **Arguments**

* **`PROGRAMS`**
  Path to a YAML configuration file describing the programs to be measured.
  The file must include details such as executable paths, arguments, and input data.

#### **Options**

| Option          | Short | Type    | Default     | Description                                            |
| :-------------- | :---- | :------ | :---------- | :----------------------------------------------------- |
| `--core`        | `-c`  | Integer | `0`         | CPU core on which the measurement should be performed. |
| `--repetitions` | `-r`  | Integer | `100`       | Number of repetitions to average each measurement.     |
| `--datapoints`  | `-d`  | Integer | `100`       | Number of measurement datapoints to collect.           |
| `--output`      | `-o`  | Path    | `./results` | Directory where results will be stored.                |
| `--verbose`     | `-v`  | Flag    | -           | Enables debug logging and detailed output.             |
| `--stats`       | `-s`  | Flag    | -           | Prints statistics after measurement completion.        |

#### **Usage Example**

```bash
sudo energy-toolkit measure ./programs.yaml -c 2 -r 50 -d 200 -o ./output --stats --verbose
```

#### **Notes**

* This command **must be run with elevated privileges** (e.g., using `sudo`) to access energy measurement interfaces like RAPL.
* Results and statistics are saved automatically in the specified output directory.
* Running with `--verbose` prints detailed runtime logs with timestamps.

#### **Example Output**

```text
[12:32:05] Validating programs configuration
[12:32:05] Configuration valid.
[12:32:05] Running analysis on core 2.
[12:32:05] Measurement will record 200 datapoints.
[12:32:05] Each datapoint will be averaged over 50 repetitions.
[12:32:05] Resulting files will be saved at /home/user/output
[12:32:06] Starting measurements! Grab a coffee...
[12:36:44] Measurements finished.
[12:36:44] Saving results!
```

---

### 2. Validate Command

The `validate` command checks whether a given program configuration file (`programs.yaml`) is properly formatted and contains all required fields.

```bash
energy-toolkit validate PROGRAMS [OPTIONS]
```

#### **Arguments**

* **`PROGRAMS`**
  Path to the YAML file describing the programs to measure.

#### **Options**

| Option      | Short | Type | Default | Description                              |
| :---------- | :---- | :--- | :------ | :--------------------------------------- |
| `--verbose` | `-v`  | Flag | -       | Prints debug messages during validation. |

#### **Usage Example**

```bash
energy-toolkit validate ./programs.yaml --verbose
```

#### **Example Output**

```text
[09:45:12] Validating programs file ./programs.yaml
[09:45:12] Configuration valid.
```

---

### 3. Example `programs.yaml` File

Below is a minimal example of a configuration file for defining the executables to be measured:

```yaml
programs:
  - executeable: ./my_program
    args: ["--input", "data.txt", "--mode", "fast"]
    input: null

  - executeable: /usr/bin/python3
    args: ["script.py", "--option", "value"]
    input: input_data.txt
```

Each entry defines:

* `executeable`: Path to the program or script.
* `args`: Optional list of command-line arguments.
* `input`: Optional input file or data stream.

---

### Summary

| Command    | Purpose                                                           |
| :--------- | :---------------------------------------------------------------- |
| `measure`  | Runs the configured programs and records energy consumption data. |
| `validate` | Validates program configuration files before measurement.         |

The CLI provides a flexible and scriptable way to benchmark energy efficiency, making it ideal for automated testing or performance evaluation workflows.

Here’s a polished **“Usage as Library”** section that matches the tone and structure of your existing README, and cleanly demonstrates how to use the `energy-toolkit` programmatically in Python.
It builds on the example you provided and fits naturally after your CLI documentation.

---

## Usage as Library

In addition to the command-line interface, `energy-toolkit` can also be used directly as a **Python library** to measure the energy consumption and execution time of programs within your own code or tests.

### Example

The following example demonstrates how to use the `Energy_Toolkit` class to:

1. Create an energy measurement toolkit.
2. Define two programs to be measured.
3. Run the measurements.
4. Write results and statistics to disk.

```python
from energy_toolkit.energy_toolkit import Energy_Toolkit, Program

# Create an Energy_Toolkit instance
# Parameters: datapoints=3, repetitions=2
toolkit = Energy_Toolkit(datapoints=3, repetitions=2)

# Define the programs to be measured
program1 = Program("./program_a", ["--mode", "fast"], "")
program2 = Program("./program_b", ["--input", "data.txt"], "")

# Add programs to the toolkit
toolkit.add_program(program1)
toolkit.add_program(program2)

# Run the measurement process
toolkit.measure()

# Write results and statistics to files
toolkit.write_results()
toolkit.write_statistics()

# Optionally print statistics to the console
toolkit.print_statistics()
```

### Explanation

* **`Energy_Toolkit(datapoints, repetitions)`**
  Initializes the toolkit with the number of datapoints to collect and repetitions to average per datapoint.

* **`Program(executable, args, input)`**
  Defines an executable program, its command-line arguments, and optional input.

* **`add_program()`**
  Adds the program to the measurement queue.

* **`measure()`**
  Executes all added programs and records energy and timing data.

* **`write_results()` / `write_statistics()`**
  Save detailed measurement results and computed statistics to the output directory.

* **`print_statistics()`**
  Prints a summary of the measurement results to the console.


## Metrics Returned

After executing a measurement - whether through the **command-line interface** or the **Python library** - the `energy-toolkit` automatically generates a structured set of result files in the specified output directory.

### Output Structure

Each measured program is assigned a unique **program ID (`pid`)**, numbered in ascending order based on how the programs were added to the toolkit or defined in the `programs.yaml` configuration file.

For each program, a dedicated subdirectory is created:

```
results/<pid>/
```

Within each `<pid>` directory, the following files are generated:

| File                 | Description                                                                                                                                              |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`results.csv`**    | Contains raw measurement data, including the recorded **energy consumption** and **execution time** for each datapoint.                                  |
| **`statistics.csv`** | Contains aggregated metrics derived from the raw data, such as **mean**, **variance**, and **standard deviation** for both energy and time measurements. |

### Example Directory Layout

```
results/
├── 0/
│   ├── results.csv
│   └── statistics.csv
└── 1/
    ├── results.csv
    └── statistics.csv
```

This structure makes it easy to analyze individual program runs or combine results for larger performance and energy efficiency studies.

## Contributing

Contributions to the `energy-toolkit` are welcome!
If you encounter any bugs, unexpected behavior, or have feature suggestions, please open an **issue** on the project’s GitHub repository.

When reporting a bug, include as much detail as possible — such as the command used, environment information, and any error messages — to help us reproduce and resolve the issue quickly.

