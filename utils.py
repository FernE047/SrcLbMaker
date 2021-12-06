import requests

API = "https://www.speedrun.com/api/v1/"

lbtypehelp = """Type of the leaderboard.\n
Wrs - world records count,\n
runs - runs count,\n
gp - games played count,\n
cat - categories played count,\n
pod - podiums count,\n
mc - games moderation count.
"""


def getWrs(userid):
    """Return a user's world records count."""
    return len(requests.get(
            f"{API}users/{userid}/personal-bests?top=1"
        ).json()["data"])


def getRuns(userid):
    """Return a user's runs count."""
    done = False
    offset = 0

    while not done:
        data = requests.get(
            f"{API}runs?user={userid}&max=200&offset={offset * 200}"
        ).json()
        offset += 1
        if data["pagination"]["size"] < 200:
            done = True

    return data["pagination"]["offset"] + data["pagination"]["size"]


def getGamesPlayed(userid):
    """Return a number of games in which the user has runs."""
    data = requests.get(
        f"{API}users/{userid}/personal-bests"
    ).json()

    return len(set([i["run"]["game"] for i in data["data"]]))


def getModCount(userid):
    """Return a number of games moderated by user."""
    return requests.get(
        f"{API}games?moderator={userid}&_bulk=yes&max=1000"
    ).json()["pagination"]["size"]


def getRunner(username):
    """Check if the user exists, return his data if any, otherwise False."""
    data = requests.get(
        f"{API}users?lookup={username}"
    ).json()

    return data if data["pagination"]["size"] > 0 else False

def getCategoriesPlayed(userid):
    """Return a number of categories in which the user has runs."""
    data = requests.get(
        f"{API}users/{userid}/personal-bests"
    ).json()

    return len(set([i["run"]["category"] for i in data["data"]]))

def getPodiums(userid):
    """Return a user's podium count."""
    return len(requests.get(
            f"{API}users/{userid}/personal-bests?top=3"
        ).json()["data"])
