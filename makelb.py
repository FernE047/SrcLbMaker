import csv
import datetime

from tqdm import tqdm
import click

import utils

result = []


@click.command()
@click.option(
        "-t", "--lbtype", required=True,
        type=click.Choice(["wrs", "runs", "gp", "mc","cat","pod"]),
        help=utils.lbtypehelp
)
@click.option(
        "-L", "--lblength",
        type=int, default=100,
        show_default=True,
        help="Leaderboard's length."
)
def makeLb(lbtype, lblength):
    """Print leaderboard of a given type."""
    filelength = len(open("runners.csv", 'r').readlines())

    with open("runners.csv", 'r') as csvfile:
        file = csv.reader(csvfile)

        if lbtype == "wrs":
            for i in tqdm(file, total=filelength, ncols=75,
                          unit="runner", ascii=True):
                result.append([i[0], utils.getWrs(i[1]), i[2]])

        elif lbtype == "runs":
            for i in tqdm(file, total=filelength, ncols=75,
                          unit="runner", ascii=True):
                result.append([i[0], utils.getRuns(i[1]), i[2]])

        elif lbtype == "gp":
            for i in tqdm(file, total=filelength, ncols=75,
                          unit="runner", ascii=True):
                result.append([i[0], utils.getGamesPlayed(i[1]), i[2]])

        elif lbtype == "mc":
            for i in tqdm(file, total=filelength, ncols=75,
                          unit="runner", ascii=True):
                result.append([i[0], utils.getModCount(i[1]), i[2]])

        elif lbtype == "cat":
            for i in tqdm(file, total=filelength, ncols=75,
                          unit="runner", ascii=True):
                result.append([i[0], utils.getCategoriesPlayed(i[1]), i[2]])

        elif lbtype == "pod":
            for i in tqdm(file, total=filelength, ncols=75,
                          unit="runner", ascii=True):
                result.append([i[0], utils.getCategoriesPlayed(i[1]), i[2]])
        else:
            return

    result.sort(
        key=lambda x: x[1], reverse=True
    )

    click.echo(
        datetime.datetime.now().date()
    )

    for n, i in enumerate(result):
        click.echo(
            f"`{n+1}.`{i[2]}`{i[0]} {' ' * (23-len(str(n+1))-len(i[0]))} {i[1]}`"
        )  # i[0] - nickname, i[1] - value, i[2] - flag
        if n+1 >= lblength:
            break


if __name__ == "__main__":
    makeLb()
