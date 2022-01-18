import requests


API = "https://www.speedrun.com/api/v1/"


def wrs(userid):
    """Return a user's world records count."""
    try:
        return len(requests.get(
                f"{API}users/{userid}/personal-bests?top=1"
            ).json()["data"])
    except KeyError:
        return 0


def runs(userid):
    """Return a user's runs count."""
    offset = 0

    while True:
        data = requests.get(
            f"{API}runs?user={userid}&max=200&offset={offset * 200}"
        ).json()
        offset += 1
        if data["pagination"]["size"] < 200:
            break

    return data["pagination"]["offset"] + data["pagination"]["size"]


def gp(userid):
    """Return a number of games in which the user has runs."""
    data = requests.get(
        f"{API}users/{userid}/personal-bests"
    ).json()

    return len(set([i["run"]["game"] for i in data["data"]]))


def cp(userid):
    """Return a number of categories in which the user has runs."""
    data = requests.get(
        f"{API}users/{userid}/personal-bests"
    ).json()

    return len(set([i["run"]["category"] for i in data["data"]]))


def mods(userid):
    """Return a number of games moderated by user."""
    return requests.get(
        f"{API}games?moderator={userid}&_bulk=yes&max=1000"
    ).json()["pagination"]["size"]


def pod(userid):
    """Return a user's podium count."""
    return len(requests.get(
            f"{API}users/{userid}/personal-bests?top=3"
        ).json()["data"])
