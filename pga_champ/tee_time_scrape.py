from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.pgachampionship.com/starting-times"

res = requests.get(url)
data = res.text

soup = BeautifulSoup(data, 'html.parser')
# print(soup.prettify)


tee_time_dict = {'time': [], 'first_name': [], 'last_name': []}
rows = soup.find_all(class_= "TeeTimeTable-tr")

for row in rows:
    tee_time = row.find(class_="event").text

    players = row.select(".TeeTimeRow-td .BriefPlayer-player")

    for player in players:
        tee_time_dict['time'].append(tee_time)
        tee_time_dict['first_name'].append(player.select('.BriefPlayer-firstName')[0].text)
        tee_time_dict['last_name'].append(player.select('.BriefPlayer-lastName')[0].text)

tee_time_frame = pd.DataFrame(tee_time_dict)
tee_time_frame.to_csv("tee_times.csv", index=False)
