from flask import Flask, request
from flask_ask import Ask, statement, question, session
from menu import get_menu
from utility import get_custom_value, generate_place_info, get_open_places, statement_helper, read_menu
import responses

app = Flask(__name__)

ask = Ask(app, "/ub_dining")


@app.route('/')
def homepage():
    return responses.HOMEPAGE_TEXT


@ask.launch
def start_skill():
    return question(responses.WELCOME_MESSAGE)

# Three things: Ask what is open at any day; Ask if that a particular location is open or not; Ask the menu for a dining center.
@ask.intent("AMAZON.HelpIntent")
def help():
    return question(responses.HELP_RESPONSE)


@ask.intent("AMAZON.CancelIntent")
@ask.intent("AMAZON.StopIntent")
@ask.session_ended
def no_intent():
    bye_text = "Glad I could help, go feast your taste buds now!"
    return statement(bye_text)


@ask.intent("OpenByLocation")
def open_by_date(time):
    try:
        content = request.json
        location = get_custom_value(content, "location")
        if location is None:
            location = responses.DEFAULT_LOCATION
        places = get_open_places(location, time)
        return question(statement_helper(places, location))
    except:
        msg = responses.ERROR_STATEMENT+responses.ADDITIONAL_QUESTION
        return question(msg)


@ask.intent("IsPlaceOpen")
def check_place_open(time):
    try:
        content = request.json
        place = get_custom_value(content, "place")
        if place is None:
            raise Exception("Invalid on-campus dining location")
        place_info = generate_place_info(place, time)
        msg = ""
        if place_info == "Closed":
            msg = f"{place} is {place_info}..."
        else:
            duration = place_info.replace("-", "to")
            msg = f"{place} is open from {duration}..."
        msg += responses.ADDITIONAL_QUESTION
        return question(msg)
    except:
        msg = responses.ERROR_STATEMENT
        return question(msg)


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
        out_msg += responses.ADDITIONAL_QUESTION
        return question(out_msg)
    except Exception as ex:
        msg = responses.ERROR_STATEMENT
        return question(msg)


@ask.intent("AMAZON.FallbackIntent")
def default_fallback():
    return question(responses.ERROR_STATEMENT)


if __name__ == "__main__":
    app.run(debug=True)
