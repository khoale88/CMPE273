"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import pizza_functions as PF
import json
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    
# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}

    card_title = "Welcome"
    speech_output = "Hi, Welcome to Mod Pizza, Individual Artisan-Style Pizzas, " \
                    "Please let me know in few words if you would like to place order or track existing order, " \
                    " by saying, place order, or, track order. " 

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I did not receive a response, " \
                    "Please let me know in few words if you would like to place order or check status of existing order, " \
                    " by saying, place order, or, check status. " 

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_place_order(intent,session):
    #crete a new order
    session_attributes = session.get('attributes')
    card_title = "order a pizza"
    #initialize a menu
    if('order' not in session_attributes):  
        session_attributes = json.load(open("data_schema.json"))

    #instruct to size
    speech_output = "You have choosen to place an order. " \
                    "Please let me know if you would like to order 6 inches or 11 inches pizza"
    reprompt_text = "I did not receive a response, " \
                    "Please let me know if you would like to order 6 inches or 11 inches pizza"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_size(intent,session):
    session_attributes = session.get('attributes')
    card_title = 'PizzaSize'

    #update pizza size
    session_attributes['current_pizza']['size'] = intent['slots'][card_title]['value']

    #instruct to sauce
    #only get sauce if it is the 1st time in this session - not yet in the menu
    if('sauce' not in session_attributes['menu']):
        session_attributes['menu']['sauce'] = PF.getMenu('sauce')
    
    #build sauce speech
    sauce_speech = "Please let me know which of the following sauces would you like to Add to base,"
    sauce_speech += str(', '.join(session_attributes['menu']['sauce']))

    #build output
    speech_output = "You have choosen %s inches pizza. " %(session_attributes['current_pizza']['size'])
    speech_output += sauce_speech

    reprompt_text = "I did not receive a response, " 
    reprompt_text += sauce_speech          

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_sauce(intent,session):
    session_attributes = session.get('attributes')
    card_title = 'PizzaSauce'

    #get the sauce response out
    sauce_response = intent['slots'][card_title]['value']

    #add sauce
    selected_sauce = []
    if ('no sauce' in sauce_response.lower()):
        pass
    elif ('all sauce' in sauce_response.lower()):
        selected_sauce = session_attributes['menu']['sauce']
    else:
        selected_sauce = sauce_response
    session_attributes['current_pizza']['sauce'] = selected_sauce

    #instruct to cheese
    #only get chees if it is not in the menu
    if('cheese' not in session_attributes):
        session_attributes['menu']['cheese'] = PF.getMenu('cheese')

    #cheese speech, need to add all cheese?
    cheese_speech = "Please let me know which of the following cheeses would you like to Add, "
    cheese_speech += str(', '.join(session_attributes['menu']['cheese']))

    #build output
    speech_output = "You have choosen %s on pizza base. " %(', '.join(selected_sauce))
    speech_output += cheese_speech

    reprompt_text = "I did not receive a response, " 
    reprompt_text += cheese_speech

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_cheese(intent,session):
    session_attributes = session.get('attributes')
    card_title = 'PizzaCheese'

    #get the cheese out
    cheese_response = intent['slots'][card_title]['value']

    #add cheese into pizza 
    menu = session_attributes['menu']
    selected_cheese = [c for c in menu['cheese'] if c.lower() in cheese_response.lower()]
    current_pizza = session_attributes['current_pizza']
    current_pizza['cheese'] = str(', '.join(selected_cheese))
    session_attributes['current_pizza'] = current_pizza

    #instruct to meat
    #only get meat if it is not in the menu
    if('meat' not in session_attributes):
        session_attributes['menu']['meat'] = []
        meat = PF.getMenu('meat')
        session_attributes['menu']['meat'] = meat

    #build meat speech
    meat_speech = "Please let me know which of the following meat would you like to Add, "
    meat_speech += str(', '.join(meat))

    #build output
    speech_output = "You have choosen %s  on pizza base. " %(', '.join(selected_cheese))
    speech_output += meat_speech
                     
    reprompt_text = "I did not receive a response, " 
    reprompt_text += meat_speech

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_meat(intent,session):
    session_attributes = session.get('attributes')
    card_title = 'PizzaMeat'

    #get the meat out
    meat_response = intent['slots'][card_title]['value']

    #add meat into pizza 
    menu = session_attributes['menu']
    selected_meat = [m for m in menu['meat'] if m.lower() in meat_response.lower()]
    current_pizza = session_attributes['current_pizza']
    current_pizza['meat'] = str(', '.join(selected_meat))
    session_attributes['current_pizza'] = current_pizza

    #instruct to veggies
    #only get veggies if it is not in the menu
    if('veggies' not in session_attributes):
        session_attributes['menu']['veggies'] = []
        veggies = PF.getMenu('veggies')
        session_attributes['menu']['veggies'] = veggies

    #build veggies instructions
    veggies_speech = "Please let me know which of the following veggies would you like to Add, "
    veggies_speech += str(", ".join(veggies))
    #build output
    speech_output = "You have choosen %s  on pizza base. " %(', '.join(selected_meat))
    speech_output += veggies_speech

    reprompt_text = "I did not receive a response, "
    reprompt_text += veggies_speech

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_pizza_veggies(intent,session):
    session_attributes = session.get('attributes',{})
    card_title = 'PizzaVeggies'

    #get the veggies out
    veggies_response = intent['slots'][card_title]['value']

    #add veggies into pizza 
    menu = session_attributes['veggies']
    selected_veggies = [v for v in menu['veggies'] if v.lower() in veggies_response.lower()]
    current_pizza = session_attributes['current_pizza']
    current_pizza['veggies'] = str(', '.join(selected_veggies))
    session_attributes['current_pizza'] = current_pizza

    #finish this pizza
    if'order' not in session_attributes:
        session_attributes['order'] = []
    order = session_attributes['order']
    order.append(session_attributes['current_pizza'])
    session_attributes['order'] = order


    #instruct to next
    #Read veggies from Menu
    speech_output = "You have choosen %s on pizza base. " %(', '.join(selected_veggies))
    speech_output += "do you want to add another pizza?"

    reprompt_text = "I did not receive a response, " \
                    "Do you want to add another pizza?"    

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request(session):
    card_title = "Session Ended"
    size = len(session['attributes']['order'])
    # y = entire order 
    speech_output = "You have order %s pizza,"\
                    "Your order number is: 1234," \
                    "Thank you for using MOD Pizza automated pizza ordering system, " \
                    "Have a nice day! "%(size)
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])



def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch

    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "PlaceOrderIntent":
        return handle_place_order(intent,session)
    if intent_name == "PizzaSizeIntent":
        return handle_pizza_size(intent,session)
    if intent_name == "PizzaSauceIntent":
        return handle_pizza_sauce(intent,session)
    if intent_name == "PizzaCheeseIntent":
        return handle_pizza_cheese(intent,session)
    if intent_name == "PizzaMeatIntent":
        return handle_pizza_meat(intent,session)
    if intent_name == "PizzaVeggiesIntent":
        return handle_pizza_veggies(intent,session)
    if intent_name == "AddAnotherPizzaIntent":
        return handle_place_order(intent,session)
    if intent_name == "DoNotAddPizzaIntent":
        return handle_session_end_request(session)
    if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request(session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
    


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])