"""
Plotter module to plot data recorded with the energy-toolkit application
"""

from typing import Dict, List
import csv
import os
from pathlib import Path
from datetime import datetime

import click
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from energy_toolkit.logger import Logger
from energy_toolkit.util import PlotMode


class Plotter:
    """
    Energy-Toolkit Plotter component. On Object creation the plotter parses the data found under
    the given path. Offers methods for plotting the data using plotly
    """

    # Data attribute used to store the parsed data
    data: List[Dict[str, np.ndarray]]

    # Mode to handle bar/line chart plotting
    _mode: PlotMode

    # Class logger
    _logger = Logger().get_logger()

    def __init__(self, path: str, mode: PlotMode):
        """
        Create a new plotter object, validate the strucure of the given path and
        read the data under the given path (if possible)
        """
        # Check if we received a valid mode
        if mode is PlotMode.UNDEFINED:
            raise click.ClickException("Mode is undefined!")

        self._mode = mode
        # Valide the strucure of the path
        has_valid_structure = self.validate_results_structure(path)

        if has_valid_structure:
            # If the structure is valid, read the data
            self._read_data(path)
        else:
            raise click.ClickException(
                "Given path has an invalid structure. Make sure the path contains numbered" \
                " folders that each at least contain a results.csv"
            )

    def _read_data(self, base_path: str) -> List[Dict[str, np.ndarray]]:
        """
        Read the results data from the given path
        """
        results_list: List[Dict[str, np.ndarray]] = []

        # Iterate over the <pid>/ folders in the given folder
        for entry in sorted(os.listdir(base_path)):
            # Construct the path to the results.csv for each folder
            subfolder = os.path.join(base_path, entry)
            results_file = os.path.join(subfolder, "results.csv")

            # Filter out folders not meeting our requirements
            if not os.path.isdir(subfolder):
                continue
            if not os.path.exists(results_file):
                continue

            # Read data and store energy and time values separately
            with open(results_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data_columns = {field: [] for field in reader.fieldnames}

                for row in reader:
                    for field, value in row.items():
                        data_columns[field].append(value)

            # convert lists to NumPy arrays
            for field in data_columns:
                try:
                    data_columns[field] = np.array(data_columns[field], dtype=float)
                except ValueError:
                    data_columns[field] = np.array(data_columns[field], dtype=object)

            results_list.append(data_columns)

        self.data = results_list

    def validate_results_structure(self, parserpath: str) -> bool:
        """
        Validate if the folder structure under the given path meets our requirements

        - There should be a folder for each executed program
        - Each folder should contain a results.csv file

        E.g:
        ├── 0
        │   ├── results.csv
        │   └── statistics.csv
        └── 1
            ├── results.csv
            └── statistics.csv

        """
        base = Path(parserpath)

        # Check base exists and is a directory
        if not base.exists() or not base.is_dir():
            return False

        # Check directory not empty (has at least one item)
        subdirs = [p for p in base.iterdir() if p.is_dir()]
        if not subdirs:
            return False

        # Every subdir must contain at least one result.csv file
        for sd in subdirs:
            # Check exactly one level deep
            if not (sd / "results.csv").exists():
                return False

        return True

    def plot(self, headless=False):
        """
        Plot the data stored in the object. If headless is true the plot will be saved as .pdf file,
        otherwise plotlys web rendering is used.
        """

        fig = None

        # Check the mode stored in the object and call the respective plotting function
        if self._mode == PlotMode.BARCHART:
            fig = self._plot_bars(self.data)
        elif self._mode == PlotMode.LINECHART:
            fig = self._plot_lines(self.data)
        else:
            raise click.ClickException("Mode is undefined!")

        # If headless is true safe as pdf file. Otherwise just call show()
        if headless:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            fig.write_image(f"figure_{current_time}.pdf", width=1000, height=520)
        else:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/figure_{current_time}.html"
            fig.write_html(filename)

    def _plot_lines(self, data) -> go.Figure:
        """
        Function to create a figure object that shows the raw data of each programs energy and time
        as line chart respectively.
        """
        labels = [f"PID {i+1}" for i in range(len(data))]

        # One figure, two subplots stacked vertically
        fig = make_subplots(
            rows=2, cols=1, subplot_titles=("Energy per program", "Time per program")
        )

        # Add a line for each program
        for i, d in enumerate(data):
            fig.add_trace(
                go.Scatter(
                    y=d["# Time"], mode="lines+markers", name=f"{labels[i]} Time"
                ),
                row=2,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    y=d["Energy"], mode="lines+markers", name=f"{labels[i]} Energy"
                ),
                row=1,
                col=1,
            )

        fig.update_layout(
            showlegend=True, autosize=True, margin={"l": 20, "r": 20, "t": 40, "b": 20}
        )
        fig.update_xaxes(title_text="Measurements", row=2, col=1)
        fig.update_xaxes(title_text="Measurements", row=1, col=1)
        fig.update_yaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Energy", row=1, col=1)

        return fig

    def _plot_bars(self, data) -> go.Figure:
        """
        Function to create a figure object that shows the mean of each program's 
        energy and time as bar charts, with standard deviation error bars.
        """
        labels = [f"Program {i+1}" for i in range(len(data))]

        avg_times = [float(np.mean(d["# Time"])) for d in data]
        avg_energy = [float(np.mean(d["Energy"])) for d in data]

        std_times = [float(np.std(d["# Time"])) for d in data]
        std_energy = [float(np.std(d["Energy"])) for d in data]

        # One figure, two subplots
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("Average Time per Program", "Average Energy per Program"),
        )

        fig.add_trace(
            go.Bar(
                x=labels,
                y=avg_times,
                name="Time in s",
                error_y={"type": 'data', "array": std_times, "visible": True},
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                x=labels,
                y=avg_energy,
                name="Energy in J",
                error_y={"type": 'data', "array": std_energy, "visible": True},
            ),
            row=1,
            col=2,
        )

        fig.update_layout(
            showlegend=True,
            autosize=True,
            margin={"l": 20, "r": 20, "t": 40, "b": 20},
        )

        fig.update_xaxes(title_text="Programs")
        fig.update_yaxes(title_text="Time", row=1, col=1)
        fig.update_yaxes(title_text="Energy", row=1, col=2)

        return fig
