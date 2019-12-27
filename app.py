from flask import Flask
from flask_ask import Ask, statement, question, session
from location_status import generate_status

app = Flask(__name__)

ask = Ask(app, "/ub_locations")

AREAS = ["Ellicott / Greiner Hall", "North Campus Academic Buildings",
         "South Campus", "Governors", "Downtown"]


def get_open_places(location, date=None):
    open_places = generate_status(location, date)
    alexa_out = []
    for place in open_places:
        duration = open_places[place].replace('-', 'to')
        s = f"{place} from {duration}. "
        alexa_out.append(s)
    return alexa_out


def get_area(area):
    for loc in AREAS:
        locUp = loc.lower()
        if locUp.find(area) >= 0:
            return loc


def statement_helper(plcaes):
    places_msg = ""
    if len(plcaes) == 1:
        places_msg = f"The only food place open at UB is {plcaes[0]}"
    elif len(plcaes) == 0:
        places_msg = f"There are no food places open at UB! "
    else:
        msg = ""
        for places_text in plcaes:
            msg += places_text
        places_msg = f"The food places open at UB are {msg}"
    places_msg += "Do you want to ask something else?"
    return places_msg


@app.route('/')
def homepage():
    return "Hello, this shit works!"


@ask.launch
def start_skill():
    welcome_message = 'Hello, would you like to know where you can eat at UB? Ask about where you could eat by date and I will tell you.'
    return question(welcome_message)


@ask.intent("YesIntent")
def share_places():
    plcaes = get_open_places()
    return statement(statement_helper(plcaes))


@ask.intent("NoIntent")
def no_intent():
    bye_text = "Glad I could be of help, have a wonderful day!"
    return statement(bye_text)


@ask.intent("OpenByDate")
def open_by_date(time, location):
    places = get_open_places(get_area(location), time)
    return question(statement_helper(places))


@ask.intent("AMAZON.FallbackIntent")
def default_fallback():
    msg = "Sorry I don't know what you mean!"
    return statement(msg)


if __name__ == "__main__":
    app.run(debug=True)
