import flask
import requests
import json
import os

app = flask.Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

def getSum(req):

    numb_one = req.get('queryResult').get('parameters').get('number')
    numb_two = req.get('queryResult').get('parameters').get('number1')
    outString = "The sum of the numbers is {}".format(numb_one+numb_two)
    outDict = {'fulfillmentText':outString}
    return outDict

def getChuckNorrisJoke(req):

    url = 'http://api.icndb.com/jokes/random'
    data = requests.get(url)

    if data.status_code == 200:
        data = json.loads(data.content.decode('utf-8'))
        outString = data['value']['joke']
    else:
        outString = "Chunk Norris Joke is not available, please try after sometime."

    outDict = {'fulfillmentText':outString} 
    return outDict

def getDateTrivia(req):

    date = req.get('queryResult').get('parameters').get('date')
    month = int(date[5:7])
    day = int(date[8:10])
    url = 'http://numbersapi.com/{}/{}/date'.format(month, day)
    data = requests.get(url)

    if data.status_code == 200:
        outString = data.text
    else:
        outString = "Date trivia is not available, please try after sometime."

    outDict = {'fulfillmentText':outString}
    return outDict

def getPlanetAttribute(req):

    planet = req.get('queryResult').get('parameters').get('planet')
    attribute = req.get('queryResult').get('parameters').get('attribute')

    url = os.environ.get("URL_PLANETS")+"?q={\"Name\": \""+planet+"\"}"
    headers = {
        'content-type': "application/json",
        'x-apikey': os.environ.get("API_KEY"),
        'cache-control': "no-cache"
    }
    data = requests.request("GET", url, headers=headers)

    if data.status_code == 200:
        data = data.json()
        val = data[0][attribute]
        outString = "The "+attribute.lower()+" of "+planet+" is "+val+"."
    else:
        outString = "Planet data is not available, please try after sometime."

    outDict = {'fulfillmentText':outString}
    return outDict

def saveFeedback(req):

    outputContexts = req.get('queryResult').get('outputContexts')
    
    if outputContexts[0]['name'].split('/')[-1] == 'session-vars':

        firstName = outputContexts[0]['parameters']['given-name']
        emailAddress = outputContexts[0]['parameters']['email']
        comment = outputContexts[0]['parameters']['any']

        url = os.environ.get("URL_FEEDBACK")

        payload = json.dumps( {"FirstName": firstName,
                        "EmailAddress": emailAddress,
                        "Comment":comment} )
        headers = {
            'content-type': "application/json",
            'x-apikey': os.environ.get("API_KEY"),
            'cache-control': "no-cache"
        }
        data = requests.request("POST", url, data=payload, headers=headers)

        if data.status_code == 201:
            outString = "Thank you! Your feedback was successfully received!"
        else:
            outString = "Sorry, your feedback is not saved, try again later."

    outDict = {'fulfillmentText':outString}
    return outDict

def checkDateOfBirth(req):

    date = req.get('queryResult').get('parameters').get('date')
    
    if date[0:4] == "UUUU":
        session = req.get('session')
        contextToAdd = session+"/contexts/awaiting_year_of_birth"
        contextToDelete = session+"/contexts/awaiting_patient_name"
        outDict = {'fulfillmentText':"What is the year of birth?"}
        outDict['outputContexts'] = [
            {"name":contextToAdd, "lifespanCount":1},
            {"name":contextToDelete, "lifespanCount":0}
        ]
        return outDict
    else:
        outString = "What is the patient's name?"
        outDict = {'fulfillmentText':outString}
        return outDict

def flightBooking(req):

    slots = ["nop", "dep", "dest", "depdt", "retdt", "class"]

    actionToSlot = {"bookFlight":"nop",
                    "inputs.numpassengers":"dep",
                    "inputs.departurecity":"dest",
                    "inputs.destinationcity":"depdt",
                    "inputs.departuredate":"retdt",
                    "inputs.returndate":"class"}

    slotMessages = {"nop":"How many passengers?",
                    "dep":"Where from?",
                    "dest":"Where to?",
                    "depdt":"What date do you leave?",
                    "retdt":"What date do you return?",
                    "class":"What flight class do you wish to fly?"}

    expectedSlot = actionToSlot[req.get("queryResult").get("action")]
    filledSlots, slotValues = getFilledSlots(req)
    print("Filled slots --> ", filledSlots)
    print("Slot values --> ", slotValues)
    actualSlot = expectedSlot
    for slot in slots:
        if slot not in filledSlots:
            actualSlot = slot
            break

    session = req.get('session')
    contextName = session+"/contexts/awaiting_"+actualSlot
    outDict = {'fulfillmentText':slotMessages[actualSlot]}
    outDict['outputContexts'] = [
        {"name":contextName, "lifespanCount":1},
    ]
    return outDict

def getFilledSlots(req):
    outputContexts = req.get('queryResult').get('outputContexts')

    slotValues = {"nop":None,
                  "dep":None,
                  "dest":None,
                  "depdt":None,
                  "retdt":None,
                  "class":None}

    filledSlots = []
    for outputContext in outputContexts:
        if outputContext['name'].split('/')[-1] == 'session-vars':
            try:
                params = outputContext["parameters"]
                for param in params:
                    if "original" not in param:
                        slotValues[param] = params[param]
                        filledSlots.append(param)
            except KeyError:
                pass
    
    return filledSlots, slotValues

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    req = flask.request.get_json(force=True)
    action = req.get('queryResult').get('action')

    if action == 'getSum':
        response = getSum(req)
    elif action == 'getChuckNorrisJoke':
        response = getChuckNorrisJoke(req)
    elif action == 'getDateTrivia':
        response = getDateTrivia(req)
    elif action == 'getPlanetAttribute':
        response = getPlanetAttribute(req)
    elif action == 'saveFeedback':
        response = saveFeedback(req)
    elif action == 'checkDateOfBirth':
        response = checkDateOfBirth(req)
    else:
        response = flightBooking(req)

    return flask.make_response(flask.jsonify(response))

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()
