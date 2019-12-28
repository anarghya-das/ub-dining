from flask import Flask, request
from flask_ask import Ask, statement, question, session
from location_status import generate_status, generate_place_info
from menu import get_menu

app = Flask(__name__)

ask = Ask(app, "/ub_dining")

DEFAULT_LOCATION = "North Campus Academic Buildings"


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
        places_msg = f"The only food place open at {location} is {plcaes[0]}"
    elif len(plcaes) == 0:
        places_msg = f"There are no food places open at {location}! "
    else:
        msg = ""
        for places_text in plcaes:
            msg += places_text
        places_msg = f"The food places open at {location} are {msg}"
    places_msg += "Do you want to ask something else?"
    return places_msg


def read_menu(menu, place, time=None):
    if menu == "Closed":
        return f"{place} is Closed! "
    else:
        if time is None:
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


@app.route('/')
def homepage():
    return "UB Dining Alexa skill details will be here soon!"


@ask.launch
def start_skill():
    welcome_message = 'Hello, I will help you with dining places at UB. For more information about what I can do just say help!'
    return question(welcome_message)


@ask.intent("AMAZON.HelpIntent")
def help():
    help_text = "Here are a few examples of things you can ask me...Is a dining location open? what is open in north/south/ellicott today/tomorrow? So, what do you want to ask?"
    return question(help_text)


@ask.intent("NoIntent")
@ask.intent("AMAZON.StopIntent")
def no_intent():
    bye_text = "Glad I could help, have a wonderful day!"
    return statement(bye_text)


@ask.intent("OpenByLocation")
def open_by_date(time):
    try:
        content = request.json
        location = get_custom_value(content, "location")
        if location is None:
            location = DEFAULT_LOCATION
        places = get_open_places(location, time)
        return question(statement_helper(places, location))
    except:
        msg = "Sorry I don't know what you mean!"
        return statement(msg)


@ask.intent("IsPlaceOpen")
def check_place_open(time):
    try:
        content = request.json
        place = get_custom_value(content, "place")
        if place is None:
            raise Exception("Invalid on-campus dining location")
        place_info = generate_place_info(place, time)
        msg = "Sorry I don't know what you mean!"
        if place_info == "Closed":
            msg = f"{place} is {place_info}..."
        else:
            duration = place_info.replace("-", "to")
            msg = f"{place} is open from {duration}..."
        msg += "Do you want to ask something else?"
        return question(msg)
    except:
        msg = "Sorry I don't know what you mean!"
        return statement(msg)


@ask.intent("Menu")
def menu(time):
    try:
        content = request.json
        dining_place = get_custom_value(content, "diningCenter")
        meal_time = get_custom_value(content, "mealTime")
        dining_place_id = get_custom_value(content, "diningCenter", True)
        if dining_place_id is None:
            raise Exception("Invalid dining location id")
        menu = get_menu(dining_place_id, time, meal_time)
        out_msg = read_menu(menu, dining_place, meal_time)
        out_msg += "Do you want to ask something else?"
        return question(out_msg)
    except Exception as ex:
        print(ex)
        msg = "Sorry I don't know what you mean!"
        return statement(msg)


@ask.intent("AMAZON.FallbackIntent")
def default_fallback():
    msg = "Sorry I don't know what you mean!"
    return statement(msg)


if __name__ == "__main__":
    app.run(debug=True)
