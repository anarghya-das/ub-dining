from bs4 import BeautifulSoup
from location_status import get_unix_time
import requests
import time
import datetime

# date format: YYYY-MM-DD


def scrap_menu(url, dining_center, time=None):
    page = requests.get(url)
    page_html = page.text
    soup = BeautifulSoup(page_html, 'html.parser')

    dining_div = soup.find('div', attrs={'id': dining_center})
    meal_periods = dining_div.find_all("div", "panel-group")
    menu = {}
    for meal in meal_periods:
        closed = meal.get('id').split('-')[1]
        if closed == "nomenu":
            return "Closed"
        meal_time = meal.get('id').split('-')[2]
        menu_div = meal.find('div', attrs={'class': 'panel-body'})
        menu_items = menu_div.find_all("li", f"item-li {meal_time}-border")
        items = [item.text for item in menu_items]
        menu[meal_time] = items
    if time is None or time not in menu:
        return menu
    else:
        return menu[time]


def get_menu(dining_center, date=None,  time=None):
    url = "https://myubcard.com/dining/menu"
    if date != None:
        date_param = get_unix_time(date)
        url = f"https://myubcard.com/dining/menu?date={date_param}"
    return scrap_menu(url, dining_center, time)


if __name__ == "__main__":
    dining_centers = ['center-C3',
                      'center-mainstreetmarketdiningcen', 'center-governors']
    date = "2019-12-16"
    print(get_menu(dining_centers[2], date, "breakfast"))
