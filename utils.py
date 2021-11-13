import requests

API = "https://www.speedrun.com/api/v1/"

lbtypehelp = """Type of the leaderboard.\n
Wrs - world records count,\n
runs - runs count,\n
gp - games played count,\n
rv - runs verified by user,\n
mc - games moderation count.
"""


def getWrs(userid):
    return len(requests.get(
            f"{API}users/{userid}/personal-bests?top=1"
        ).json()["data"])


def getRuns(userid):
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
    data = requests.get(
        f"{API}users/{userid}/personal-bests"
    ).json()

    return len(set([i["run"]["game"] for i in data["data"]]))


def getRunsVerified(userid):
    done = False
    offset = 0

    while not done:
        data = requests.get(
            f"{API}runs?examiner={userid}&max=200&offset={offset * 200}"
        ).json()
        offset += 1
        if data["pagination"]["size"] < 200:
            done = True

    return data["pagination"]["offset"] + data["pagination"]["size"]


def getModCount(userid):
    data = requests.get(
        f"{API}games?moderator={userid}&_bulk=yes&max=1000"
    ).json()

    return data["pagination"]["size"]


def getRunner(username):
    data = requests.get(
        f"{API}users?lookup={username}"
    ).json()

    return data if data["pagination"]["size"] > 0 else False
