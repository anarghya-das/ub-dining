from bs4 import BeautifulSoup
import requests
import time
import datetime

# date format: YYYY/MM/DD


def generate_status(area, date=None):
    url = "https://myubcard.com/recess"
    if date != None:
        x = date.split("-")
        year = int(x[0])
        month = int(x[1])
        day = int(x[2])
        d = datetime.date(year, month, day)
        unixtime = time.mktime(d.timetuple())
        date_param = str(int(unixtime))
        url = f"https://myubcard.com/recess?date={date_param}"
    page = requests.get(url)
    page_html = page.text

    soup = BeautifulSoup(page_html, 'html.parser')

    date_div = soup.find('h2', attrs={'class': 'sub-title text-center'})
    date = date_div.text.strip()

    recess_list = soup.find('div', attrs={'id': 'recess-content'})
    locations = recess_list.contents
    all_locations = {}
    area_locations = {}
    for location in locations:
        area_name = location.find(class_='sub-title').text
        buildings = location.find_all('div', 'col-xs-12 area')
        per_area = {}
        for building in buildings:
            b_contents = building.contents
            p_name_div = b_contents[0]
            status_div = b_contents[1]
            p_name = p_name_div.find('a').text.strip()
            timing = status_div.find('div').text.strip()
            all_locations[p_name] = timing
            if timing != "Closed":
                per_area[p_name] = timing
        area_locations[area_name] = per_area
    return area_locations[area]


AREAS = ["Ellicott / Greiner Hall", "North Campus Academic Buildings",
         "South Campus", "Governors", "Downtown"]


if __name__ == "__main__":
    now = datetime.datetime.now()
    da = now.strftime("%Y-%m-%d")
    a = generate_status(AREAS[0], da)
    print(f"Open: {a}")
