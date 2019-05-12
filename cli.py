from utils.Convertor import Convertor
from utils.CLIManager import CLIManager
import click
from requests_html import HTMLSession


@click.command()
@click.option("--amount", type=float, required=True, help="Amount of money")
@click.option(
    "--input_currency",
    type=str,
    required=True,
    help="Base currency to convert from (symbol and ISO code accepted)",
)
@click.option(
    "--output_currency",
    type=str,
    help="Currency to convert to (symbol and ISO code accepted)",
)
def run(
    amount,
    input_currency,
    output_currency,
    cli=CLIManager(
        convertor=Convertor(),
        session=HTMLSession(),
        url="http://localhost:5000",
    ),
):
    """Command line interface to convert various currencies"""
    click.echo(click.style("Fetching", fg="green"))
    click.echo(cli.calculate(amount, input_currency, output_currency))


if __name__ == "__main__":
    run()
