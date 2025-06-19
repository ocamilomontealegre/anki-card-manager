from click import command, option
from .scripts import migrate


@command()
@option("--message", required=True, help="Migration message")
def cli(message: str):
    migrate(message=message)


if __name__ == "__main__":
    cli()
