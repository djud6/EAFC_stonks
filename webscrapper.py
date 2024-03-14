from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re
import cloudscraper

def find_best_value_players(rating, price):
    data = {'Rating': rating, 'Price': price}
    df = pd.DataFrame(data)

    # Convert price to numeric values
    df['Price'] = df['Price'].str.replace(',', '').astype(int)

    # Group by rating and find the lowest price for each rating
    best_value_players = df.groupby('Rating')['Price'].min().reset_index()

    return best_value_players

# Setting Up User Agent, URL and Lists that will be filled with info. when Scrapping.
scraper = cloudscraper.create_scraper(delay=1000, browser={"custom": "ScraperBot/1.0",})
url = "https://www.futbin.com/players?page="
names = []  # Player Names
values = []  # Player IDs
Full_Link = []  # FutBin players URLs
rating = []  # Player Ratings
positioning = []  # Player Favourite Position
sec_position = []  # Player Secondary Position
price = []  # Player Average Price

for pages in range(1, 16):
    current_url = f'{url}{pages}&sort=likes&order=desc'
    print(current_url)
    req = scraper.get(current_url)
    soup = BeautifulSoup(req.text, "lxml")

    # Player Names
    player_names = soup.find_all("a", class_="player_name_players_table get-tp")
    for data in player_names:
        names.append(data.text.strip())

    # Player IDs
    player_id = soup.find_all("div", {"data-playerid": re.compile(".*")})
    for pid in player_id:
        values.append(pid.get("data-playerid"))

    # Player Links
    links = soup.find_all("a", class_="player_name_players_table get-tp")
    for fURL in links:
        Full_Link.append("https://www.futbin.com/" + fURL.get('href'))

    # Player Ratings
    card_rating = re.compile('.*form rating ut23.*')
    player_ratings = soup.find_all("span", {"class": card_rating})
    for ratings in player_ratings:
        rating.append(ratings.text.strip())

    # Player Preferred Position
    player_position = soup.find_all("div", class_="font-weight-bold")
    for pos in player_position:
        positioning.append(pos.text.strip())

    # Player Secondary Position
    player_sec_position = soup.find_all("div", style="font-size: 12px;")
    for sec_pos in player_sec_position:
        sec_position.append(sec_pos.text.strip())

    # Player Price
    player_price = soup.find_all("span", class_="font-weight-bold")
    for cost in player_price:
        price.append(cost.text.strip())

print("We're done here!")

# Call the find_best_value_players method
best_value_players = find_best_value_players(rating, price)

# Print the results
print("Best Value Players:")
print(best_value_players)