from location_status import generate_open_area_info

HOMEPAGE_TEXT = "UB Dining Alexa skill details will be here soon!"
DEFAULT_LOCATION = "North Campus Academic Buildings"
ADDITIONAL_QUESTION = "Can I help you with something else?"
ERROR_STATEMENT = f"Sorry I don't know what you mean! {ADDITIONAL_QUESTION}"
WELCOME_MESSAGE = "Hello, I will help you with information about dining places in UB. To know more about what I can do just say help!"
HELP_RESPONSE = f"You can ask about what is open in UB..." + \
    "You can also ask if a particular dining location is open or not and you can ask for the menu for a dining center in UB..." + \
    "For sample commands look at the alexa skills page...{ADDITIONAL_QUESTION}"
EXIT_RESPONSE = "Glad I could help, go feast your taste buds now!"


def get_open_places(location, date=None):
    open_places = generate_open_area_info(location, date)
    alexa_places_output = []
    for place in open_places:
        duration = open_places[place].replace('-', 'to')
        s = f"{place} from {duration}. "
        alexa_places_output.append(s)
    return alexa_places_output


def get_user_input_value(content, intent, id_value=False):
    """
    To get the place/location input from the user. If id_value parameter is true, then it returns the custom dinning place name
    identified by Alexa or else it just returns well defined user input value (like date, time)
    """
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
        places_msg = f"The only food place open in {location} is {plcaes[0]}. "
    elif len(plcaes) == 0:
        places_msg = f"There are no food places open in {location}! "
    else:
        msg = "".join(plcaes)
        places_msg = f"The food places open in {location} are {msg} "
    places_msg += ADDITIONAL_QUESTION
    return places_msg


def read_menu(menu, place, time=None):
    if menu == "Closed":
        return f"{place} is Closed! "
    else:
        if time is None or isinstance(menu, dict):
            menu_msg = f"The menu for {place} is..."
            for meal_time in menu:
                menu_items = ", ".join(menu[meal_time])
                menu_msg += f"{meal_time} menu...{menu_items}. "
        else:
            menu_items = ", ".join(menu)
            menu_msg = f"The {time} menu for {place} is {menu_items}"
        return menu_msg
