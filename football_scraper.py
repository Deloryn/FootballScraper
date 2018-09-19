import urllib.request
from bs4 import BeautifulSoup


class Match:
    def __init__(self, name, league, date, host_chance, draw_chance, guest_chance, prediction, odds):
        self.name = name
        self.league = league
        self.date = date
        self.host_chance = int(host_chance) / 100
        self.draw_chance = int(draw_chance) / 100
        self.guest_chance = int(guest_chance) / 100
        self.prediction = prediction
        self.odds = float(odds)
        
    def is_worth(self):
        try:
            chance_in_bookmaker_eyes = 1 / self.odds
        except ZeroDivisionError:
            return False
        if self.prediction == "1":
            predicted_chance = self.host_chance
        elif self.prediction == "X":
            predicted_chance = self.draw_chance
        else:
            predicted_chance = self.guest_chance
        self.chance = predicted_chance
        if predicted_chance > chance_in_bookmaker_eyes:
            self.greatness = predicted_chance - chance_in_bookmaker_eyes
            return True
        else:
            return False

        
rows = []
for i in range(0, 10):
    if i == 0:
        url = "https://www.forebet.com/en/football-predictions"
    else:
        url = "https://www.forebet.com/en/football-predictions?start=" + str(i)
    html_object = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_object, "lxml")
    rows += (soup.find_all("tr", class_="tr_0") + soup.find_all("tr", class_="tr_1"))


# We gathered all the data. We need to process it
matches = []
for row in rows:
    cells = row.find_all("td")
    try:
        name = cells[0].find("a").text
        league = cells[0].find("span", class_="shortTag").text
        date = cells[0].find("span", class_="date_bah").text
        host_chance = cells[1].text
        draw_chance = cells[2].text
        guest_chance = cells[3].text
        prediction = cells[4].find("span").text
        odds = cells[10].find_all("span")[0].text
        match = Match(name, league, date, host_chance, draw_chance, guest_chance, prediction, odds)
        matches.append(match)
    except IndexError:
        continue
    except ValueError:
        continue

# We have a collection of the matches with a nice structure. Now we need to choose good matches
good_matches = []
for match in matches:
    if match.is_worth():
        good_matches.append(match)

# Print 10 'best' bets
good_matches.sort(key=lambda x: x.greatness, reverse=True)
for match in good_matches[0:10]:
    print("{0}. Prediction: {1} Chance: {2} Odds: {3} Date: {4} League: {5}".format(
    match.name, match.prediction, match.chance, match.odds, match.date, match.league))
