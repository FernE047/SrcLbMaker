import csv
import datetime

import click
from tqdm import tqdm

import utils


functions = {
    "wrs": utils.getWrs,
    "runs": utils.getRuns,
    "gp": utils.getGamesPlayed,
    "mc": utils.getModCount,
    "cat": utils.getCategoriesPlayed,
    "pod": utils.getPodiums
}

def getData(type):
    result = []

    with open("runners.csv", 'r') as f:
        filelength = len(f.readlines())

    with open("runners.csv", 'r') as csvfile:
        file = csv.reader(csvfile)

        for i in tqdm(file, total=filelength, ncols=75,
                      unit="runner", ascii=True):
            result.append([i[0], functions[type](i[1]), i[2]])
    
    return result


@click.command()
@click.option(
        "-t",
        "--lbtype",
        required=True,
        help=utils.lbtypehelp,
        type=click.Choice([i for i in functions])
)
@click.option(
        "-L",
        "--lblength",
        type=int,
        default=100,
        show_default=True,
        help="Leaderboard's length."
)
def makeLb(lbtype, lblength):
    """Print leaderboard of a given type."""
    result = getData(lbtype)
    
    result.sort(
        key=lambda x: x[1], reverse=True
    )

    click.echo(
        datetime.datetime.now().date()
    )

    for n, i in enumerate(result, start=1):
        click.echo(
            f"`{n}.`{i[2]}`{i[0]} {' ' * (23-len(str(n))-len(i[0]))} {i[1]}`"
        )  # i[0] - nickname, i[1] - value, i[2] - flag
        if n >= lblength:
            break


if __name__ == "__main__":
    makeLb()
