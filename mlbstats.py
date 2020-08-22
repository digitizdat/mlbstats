import pandas as pd
import statsapi

# Common baseball stats abbreviations:
# http://m.mlb.com/glossary/standard-stats
# https://www.sportsbettingdime.com/guides/resources/baseball-stat-abbreviations/
trans = {
    "gamesPlayed": "G",
    "airOuts": "AO",
    "runs": "R",
    "doubles": "2B",
    "triples": "3B",
    "homeRuns": "HR",
    "strikeOuts": "SO",
    "baseOnBalls": "BB",
    "intentionalWalks": "IBB",
    "hits": "H",
    "hitByPitch": "HBP",
    "avg": "AVG",
    "atBats": "AB",
    "obp": "OBP",
    "slg": "SLG",
    "ops": "OPS",
    "caughtStealing": "CS",
    "stolenBases": "SB",
    "stolenBasePercentage": "SBP",
    "groundIntoDoublePlay": "GDP",
    "plateAppearances": "PA",
    "totalBases": "TB",
    "rbi": "RBI",
    "sacBunts": "SH",
    "sacFlies": "SF",
    "babip": "BABIP",
    "groundOutsToAirouts": "GO_AO",
    "atBatsPerHomeRun": "AB_HR",
    "groundOuts": "GO",
    "leftOnBase": "LOB",
}


def buildyears(data):
    df = []
    for year in data["stats"]:
        d = {"season": year["season"]}
        d.update(year["stats"])
        df += [d]

    return df


def get_player_data(name, group="hitting", lookupyear=None):
    if lookupyear is not None:
        players = statsapi.lookup_player(name, season=lookupyear)
    else:
        for year in range(2020, 1900, -1):
            players = statsapi.lookup_player(name, season=year)
            if len(players) > 0:
                break
    if len(players) > 1:
        print("Results are not unique")
        return None
    elif len(players) == 0:
        print("No results")
        return None

    pid = players[0]["id"]
    data = statsapi.player_stat_data(pid, group, type="yearByYear")

    df = pd.DataFrame(buildyears(data))
    df = df.rename(columns=trans)

    return df
