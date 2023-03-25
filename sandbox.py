import requests
from os import environ as env
from dotenv import load_dotenv
import json
load_dotenv()

# url = "https://orchestrator.pgatour.com/graphql"

# querystring = {"":""}

# payload = "{\"query\":\"\\tquery PlayerProfileSeasonResults($playerId: ID!, $tourCode: TourCode, $year: Int) {\\n  playerProfileSeasonResults(\\n    playerId: $playerId\\n    tourCode: $tourCode\\n    year: $year\\n  ) {\\n    playerId\\n    tour\\n    displayYear\\n    year\\n    events\\n    wins\\n    top10\\n    top25\\n    cutsMade\\n    missedCuts\\n    withdrew\\n    runnerUp\\n    seasonPills {\\n      tourCode\\n      years {\\n        year\\n        displaySeason\\n      }\\n    }\\n    cupRank\\n    cupPoints\\n    cupName\\n    cupLogo\\n    cupLogoDark\\n    cupLogoAccessibilityText\\n    rankLogo\\n    rankLogoDark\\n    rankLogoAccessibilityText\\n    officialMoney\\n    tournaments {\\n      tournamentId\\n      tournamentEndDate\\n      tournamentName\\n      finishPosition\\n      r1\\n      r2\\n      r3\\n      r4\\n      r5\\n      total\\n      toPar\\n      pointsRank\\n      points\\n      tourcastURL\\n      tourcastURLWeb\\n    }\\n    seasonRecap {\\n      tourCode\\n      displayMostRecentSeason\\n      mostRecentRecapYear\\n      items {\\n        year\\n        displaySeason\\n        items {\\n          tournamentId\\n          year\\n          title\\n          body\\n        }\\n      }\\n    }\\n    amateurHighlights\\n    tourcastEligible\\n  }\\n}\\n\\n\\n\\t\",\"operationName\":\"PlayerProfileSeasonResults\",\"variables\":{\"playerId\":\"35450\",\"tourCode\":\"R\",\"year\":2020}}"

# with open("player_results_header.json") as data:
#     headers = json.load(data)

# response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

with open("player_response_raw.json") as json_data:
    data = json.load(json_data)

print((data))

