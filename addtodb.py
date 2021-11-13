import csv

import click

import utils


@click.command()
@click.option(
        "-n", "--nickname",
        type=str,
        help="Runners nickname."
)
def addtodb(nickname):
    data = utils.getRunner(nickname)

    if not data:
        return click.echo(
            f"User {nickname} could not be found."
        )

    if data["data"][0]["location"]:
        flag = f":flag_{data['data'][0]['location']['country']['code']}:"
    else:
        flag = ''

    filedata = open("runners.csv", 'r').read()

    if nickname in filedata:
        return click.echo(
            f"{nickname} is already in database"
        )

    with open("runners.csv", 'a+', newline='') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow([
            data["data"][0]["names"]["international"],
            data["data"][0]["id"],
            flag
        ])

    click.echo(
        f"{nickname} has been successfully added to the database."
    )


if __name__ == "__main__":
    addtodb()
