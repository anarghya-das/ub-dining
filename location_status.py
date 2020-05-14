from bs4 import BeautifulSoup
from utility import get_unix_time
import requests

# date format: YYYY-MM-DD
HOUR = 1


def scrap(url, area=None, place=None):
    page = requests.get(url)
    page_html = page.text

    soup = BeautifulSoup(page_html, 'html.parser')

    date_div = soup.find('h2', attrs={'class': 'sub-title text-center'})
    date = date_div.text.strip()

    recess_list = soup.find('div', attrs={'id': 'recess-content'})
    locations = recess_list.contents
    all_locations = {}
    area_locations = {}
    places = {}
    for location in locations:
        area_name = location.find(class_='sub-title').text
        buildings = location.find_all('div', 'col-xs-12 area')
        per_area = {}
        for building in buildings:
            building_contents = building.contents
            place_name_div = building_contents[0]
            status_div = building_contents[1]
            place_name = place_name_div.find('a').text.strip()
            timing = status_div.find('div').text.strip()
            places[place_name] = timing
            all_locations[place_name] = timing
            if timing != "Closed":
                per_area[place_name] = timing
        area_locations[area_name] = per_area
    if area is not None:
        return area_locations[area]
    elif place is not None:
        return places[place]
    else:
        return all_locations


def generate_open_area_info(area, date=None):
    url = "https://myubcard.com/recess"
    if date != None:
        date_param = get_unix_time(date)
        url = f"https://myubcard.com/recess?date={date_param}"
    return scrap(url, area)


def generate_place_info(place, date=None):
    url = "https://myubcard.com/recess"
    if date != None:
        date_param = get_unix_time(date)
        url = f"https://myubcard.com/recess?date={date_param}"
    return scrap(url, None, place)


if __name__ == "__main__":
    pass
