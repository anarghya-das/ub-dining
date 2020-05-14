import responses
from location_status import generate_status, generate_place_info


def get_open_places(location, date=None):
    open_places = generate_status(location, date)
    alexa_out = []
    for place in open_places:
        duration = open_places[place].replace('-', 'to')
        s = f"{place} from {duration}. "
        alexa_out.append(s)
    return alexa_out


def get_custom_value(content, intent, id_value=False):
    try:
        if id_value:
            return content["request"]["intent"]["slots"][intent]["resolutions"][
                "resolutionsPerAuthority"][0]["values"][0]["value"]["id"]
        else:
            return content["request"]["intent"]["slots"][intent]["resolutions"][
                "resolutionsPerAuthority"][0]["values"][0]["value"]["name"]
    except:
        return None


def statement_helper(plcaes, location):
    places_msg = ""
    if len(plcaes) == 1:
        places_msg = f"The only food place open in {location} is {plcaes[0]}"
    elif len(plcaes) == 0:
        places_msg = f"There are no food places open in {location}! "
    else:
        msg = ""
        for places_text in plcaes:
            msg += places_text
        places_msg = f"The food places open in {location} are {msg}"
    places_msg += responses.ADDITIONAL_QUESTION
    return places_msg


def read_menu(menu, place, time=None):
    if menu == "Closed":
        return f"{place} is Closed! "
    else:
        if time is None or len(menu) > 1:
            menu_msg = f"The menu for {place} is..."
            for meal_time in menu:
                menu_msg += f"{meal_time} menu..."
                for item in menu[meal_time]:
                    menu_msg += f"{item}, "
        else:
            menu_msg = f"The {time} menu for {place} is "
            for item in menu:
                menu_msg += f"{item}, "
        return menu_msg
