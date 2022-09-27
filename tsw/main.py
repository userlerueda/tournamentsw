"""Main module"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"


import json

import click
import daiquiri
import numpy as np
import pandas as pd
from tabulate import tabulate

from tsw import TSW
from tsw.settings import Settings

LOGGER = daiquiri.getLogger(__name__)


@click.group()
@click.option(
    "-L",
    "--log-level",
    help="Log level",
    default=Settings().dict().get("log_level"),
    type=click.Choice(
        [
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
        ],
        case_sensitive=False,
    ),
)
@click.pass_context
def cli(ctx, log_level: str):
    """Tournament Software Command Line Interface."""
    daiquiri.setup(level=log_level.upper())
    ctx.ensure_object(dict)
    ctx.obj["my_tsw"] = TSW()


@cli.command()
@click.pass_context
@click.argument("tournament_id")
@click.argument("draw_id")
def matches(ctx, tournament_id, draw_id):
    """Matches Subcommand"""

    LOGGER.debug("Getting matches for draw with id: '%s'", draw_id)
    my_tsw = ctx.obj["my_tsw"]
    df = my_tsw.get_matches(tournament_id, draw_id)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


@cli.command()
@click.pass_context
@click.argument("tournament_id")
@click.argument("event_id")
def draws(ctx, tournament_id, event_id):
    """Draws Subcommand"""

    LOGGER.debug(
        "Getting draws for event with id %s and tournament with id: '%s'",
        event_id,
        tournament_id,
    )
    my_tsw = ctx.obj["my_tsw"]
    df = my_tsw.get_draws(tournament_id, event_id)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


@cli.command()
@click.pass_context
@click.argument("tournament_id")
def events(ctx, tournament_id):
    """Events Subcommand"""

    LOGGER.debug("Getting events for tournament with id: '%s'", tournament_id)
    my_tsw = ctx.obj["my_tsw"]
    df = my_tsw.get_events(tournament_id)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


if __name__ == "__main__":
    cli()
