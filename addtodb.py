#!/usr/bin/env python3
import csv

import click
import requests


@click.command()
@click.option(
        "-n", "--nickname",
        type=str,
        help="Runner's nickname.",
        required=True
)
def addtodb(nickname):
    """Add user to runners.csv.

    If the user does not exist print "{nickname} could not be found.".
    If the user already in runners.csv print "{nickname} is already in database."
    If successful, don't print anything.
    """
    data = requests.get(
        f"https://www.speedrun.com/api/v1/users?lookup={nickname}"
    ).json()

    if not data["pagination"]["size"]:
        return click.echo(
            f"{nickname} could not be found."
        )

    if data["data"][0]["location"]:
        flag = f":flag_{data['data'][0]['location']['country']['code']}:"
    else:
        flag = ":united_nations:"

    with open("runners.csv", 'r') as csvfile:
        filereader = csv.reader(csvfile)
        if nickname.lower() in [line[0].lower() for line in filereader]:
            return click.echo(
                f"{nickname} is already in database"
            )

    with open("runners.csv", 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow([
            data["data"][0]["names"]["international"],
            data["data"][0]["id"],
            flag
        ])


if __name__ == "__main__":
    addtodb()
