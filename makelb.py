import csv
import datetime

from tqdm import tqdm
import click

import utils

result = []

@click.command()
@click.option(
    "-t", "--lbtype", required=True,
    type=click.Choice(["wrs", "runs", "gp", "rv", "mc"]),
    help=utils.lbtypehelp)
@click.option(
    "-L", "--lblength",
    type=int, default=100
    ,show_default=True,
    help="Length of the leaderboard")
def makeLb(lbtype, lblength):
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

        elif lbtype == "rv":
            for i in tqdm(file, total=filelength, ncols=75,
                            unit="runner", ascii=True):
                result.append([i[0], utils.getRunsVerified(i[1]), i[2]])
    
        elif lbtype == "mc":
            for i in tqdm(file, total=filelength, ncols=75,
                            unit="runner", ascii=True):
                result.append([i[0], utils.getModCount(i[1]), i[2]])
        else:
            return

    result.sort(key = lambda x: x[1], reverse=True)

    print(datetime.datetime.now().date())

    for n, i in enumerate(result):
        print(f"{n + 1}. {i[0]} - {i[1]} {i[2]}")
        if n + 1 >= lblength:
            break


if __name__ == "__main__":
    makeLb()