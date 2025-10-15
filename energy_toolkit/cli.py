import click
import os
from energy_toolkit.config_parser import Config_Parser
from energy_toolkit.energy_toolkit import Energy_Toolkit
from energy_toolkit.program import Program
from datetime import datetime


@click.group()
def cli():
    """Energy Toolkit - Measure and analyze energy consumption."""
    pass


@cli.command(
    help=(
        "Measure the energy consumption of target executables defined in the PROGRAMS yaml file.\n\n"
        "Energy usage using RAPL or other supported interfaces. The measurement "
        "data and derived statistics are saved to the specified output directory."
    )
)
@click.argument("programs", type=click.Path(exists=True))
@click.option("--core", "-c", type=click.IntRange(0, os.cpu_count()), default=0, show_default=True, help="Core the measurement should be performed on.")
@click.option("--repetitions", "-r", type=click.IntRange(min=1), default=100, show_default=True, help="Repetitions used to average the measurements.")
@click.option("--datapoints", "-d", type=click.IntRange(min=1), default=100, show_default=True, help="Datapoints that should be collected.")
@click.option("--output", "-o", default="./results", help="Output directory for results.")
@click.option("--verbose", "-v", is_flag=True, help="Output debug prints")
@click.option("--stats", "-s", is_flag=True, help="Print statistics after execution")
def measure(programs, core, repetitions, datapoints, output, verbose, stats):
    """Measure command. Used to measure the files defined in the given program config."""

    # Validate that the command was called with elevated rights
    if not is_admin():
        raise click.ClickException("measure has to be run with elevated rights (e.g sudo) otherwise we cannot record measurements!")

    if verbose:
        debug_log("Validating programs configuration")

    # Validate the given program config
    config = Config_Parser.parse(programs)
    Config_Parser.validate(config)

    if verbose:
        debug_log(f"Configuration valid.")
        debug_log(f"Running analysis on core {core}.")
        debug_log(f"Measurement will record {datapoints}.")
        debug_log(f"Each datapoint will be averaged over {repetitions}.")
        debug_log(f"Resulting files will be saved at {os.path.abspath(output)}")

    # Create the toolkit with the defined configuration
    Toolkit = Energy_Toolkit(datapoints, repetitions, core, [], output)

    # Add the parsed programs to the toolkit
    for prog_obj in config["programs"]:
        pname = prog_obj["executeable"]

        if verbose:
            debug_log(f"Adding program {pname} to EnergyToolkit")

        prog = Program(pname, prog_obj["args"], prog_obj["input"])
        Toolkit.add_program(prog)
    
    if verbose:
        debug_log(f"Starting measurements! Grab a coffee...")

    # Start the measurements and write the measurement files
    Toolkit.measure()
    Toolkit.write_results()
    Toolkit.write_statistics()

    if verbose:
        debug_log(f"Measurements finished.")
        debug_log(f"Saving results!")

    if stats:
        Toolkit.print_statistics()

    

@cli.command(
    help=(
        "Validates a given program.yaml.\n\n"
        "Takes the given file and checks if it is valid."
    )
)
@click.argument("programs", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Output debug prints")
def validate(programs, verbose):
    """Verbose command to validate a given program config"""
    debug_log(f"Validating programs file {programs}")
    config = Config_Parser.parse(programs)
    Config_Parser.validate(config)
    
    if verbose:
        debug_log(f"Configuration valid.")


def debug_log(message):
    """Debug helper function to print debug messages with time code and styling"""
    current_time = datetime.now().strftime("%H:%M:%S")
    colored_time = click.style(f"[{current_time}]", fg="green")
    click.echo(f"{colored_time} {message}")

def is_admin():
    return os.geteuid() == 0