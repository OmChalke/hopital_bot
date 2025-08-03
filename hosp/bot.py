import os 
import telebot
from telebot import types
import mysql.connector
import requests
from nltk.chat.util import Chat, reflections
import datetime

x = datetime.datetime.now()

pairs = [
    ['my name is (.*)', ['Hi %1!']],
    ['(hi|hello|hey)', ['Hello!', 'Hi there!']],
    ['what can you do', ['I can chat with you!']],
    ['quit', ['Bye-bye!', 'See you later!']],
    ['(help|assist) me', ['Sure, I am here to help.']],
    ['what (can|do) you (do|offer)', ['I can chat, answer questions, and more!']],
    ['good (morning|afternoon|evening)', ['Good %1!']],
    ['(bye|goodbye|see you)', ['Goodbye!', 'Take care!', 'See you soon!']],
    ['what is your name', ['I am a chatbot created to help you.']],
    ['who are you', ['I am a simple rule-based chatbot.']],
    ['(.*) your favorite color', ['I like all colors equally!']],
    ['how is the weather', ["I'm not sure, I live in the cloud"]],
    ['are you happy', ["I'm just code, but I love talking to you!"]],
    ['(.*) your hobby', ['Chatting with people like you.']],
    ['my name is (.*)', ['Nice to meet you, %1!']],
    ['(hi|hello|hey|hii|heyy)', ['Hello!', 'Hi there!', 'Hey!', 'Greetings!']],
    ['good (morning|afternoon|evening)', ['Good %1 to you too!']],
    ['howdy', ['Howdy partner!']],
    ['(bye|goodbye|see you|see ya)', ['Bye!', 'Goodbye!', 'See you later!', 'Take care!']],
    ['(exit|quit)', ['Goodbye! Type again if you need anything.', 'Session ended.']],
    ['how are you', ["I'm doing great, thanks! How about you?"]],
    ['(i am|i\'m) (fine|good|okay|not good|sad|happy)', ['Glad to hear that!', 'Oh, I hope you feel better soon.']],
    ['what is your name', ['My name is ChatBot, your assistant!']],
    ['who are you', ['I am a rule-based chatbot created to talk with you.']],
    ['are you real', ["I'm virtual, but I'm here for you!"]],
    ['(help|assist) me', ["Sure! I'll do my best. What do you need help with?"]],
    ['can you help me with (.*)', ['I can try to help with %1. What exactly do you need?']],
    ['tell me a joke', ["Why don't scientists trust atoms? Because they make up everything!", "Why was the math book sad? It had too many problems."]],
    ['make me laugh', ['I would, but I only know bad jokes 😅']],
    ['i feel (sad|down|upset)', ["I'm sorry to hear that. I'm here for you."]],
    ['i feel (happy|good|great)', ["That's wonderful to hear!"]],
    ['i\'m bored', ["Let's chat! Or I can tell you a joke."]],
    ['what time is it', ['I\'m not wearing a watch 😄, but your system clock knows!']],
    ['what day is it', ["Check your calendar, but I think it's a great day!"]],
    ['do you like (.*)', ['I don\'t have preferences, but %1 sounds interesting!']],
    ['i like (.*)', ['Cool! %1 is nice.']],
    ['i hate (.*)', ['Oh no! Why do you hate %1?']],
    ['are you single', ['Haha! I\'m committed to chatting with you 😄']],
    ['do you have a girlfriend', ['Nope, I\'m just a bunch of code!']],
    ['do you sleep', ['Nope, I\'m always awake for you.']],
    ['where do you live', ['I live in your device – or maybe in the cloud!']],
    ['how old are you', ['I was created recently, but I\'m learning fast!']],
    ['what is life', ['42! Just kidding. It\'s what you make of it.']],
    ['do you believe in god', ['I don\'t have beliefs, but many people do.']],
    ['do you know me', ['I\'m getting to know you more each time we chat!']],
    ['(thank you|thanks)', ['You\'re welcome!', 'Anytime!', 'Glad to help!']],
    ['thanks a lot', ['It\'s my pleasure!']],
    ['(.*)', ['Interesting...', 'Tell me more.', 'Why do you say that?', 'Let\'s talk about something else.']]
]

chatbot = Chat(pairs, reflections)

high_priority = [
    "chest pain", "shortness of breath", "severe headache", "high fever", "severe abdominal pain",
    "bleeding", "sudden weakness", "paralysis", "seizures", "loss of consciousness",
    "allergic reaction", "difficulty breathing", "uncontrolled vomiting", "confusion or disorientation",
    "unconscious", "stiff neck with fever", "slurred speech", "rapid heartbeat", "blood in stool",
    "blood in urin"]

def get_chatbot_response(text):
    response = chatbot.respond(text)
    return response if response else "I'm not sure how to respond to that."

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'omchalke2003',
    'database': 'appointment_bot'
}

try:
    db = mysql.connector.connect(**mysql_config)
    cursor = db.cursor()
    print("Database connection established successfully")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL database: {err}")
    db = None
    cursor = None
except Exception as e:
    print(f"Unexpected error during database connection: {e}")
    db = None
    cursor = None

bot = telebot.TeleBot('7121615580:AAEcXUik52npkXXmTPUxUd2ZNLf26Tp6e7o')

user_data = {}

@bot.message_handler(commands=['start', 'hello']) 
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, "hiee", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Basic error handling for incoming messages
    try:
        if message is None or not hasattr(message, 'text') or message.text is None:
            # Handle case where message or text is None
            if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
                bot.send_message(message.chat.id, "I couldn't understand that message. Please try again.")
            return
            
        text = message.text.lower().strip()
        chat_id = message.chat.id
    except Exception as e:
        print(f"Error in handle_text: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            bot.send_message(message.chat.id, "Sorry, I encountered an error processing your message. Please try again.")
        return

    if chat_id in user_data and 'appointment_date' not in user_data[chat_id] and 'asked_help' not in user_data[chat_id]:
        return

    if chat_id in user_data and user_data[chat_id].get('asked_help'):
        if "address" in text:
            bot.send_message(chat_id, "Our hospital is located at: lonere, raigad.")
        elif "timing" in text or "time" in text or "open" in text:
            bot.send_message(chat_id, "We are open from 9 AM to 5 PM, Monday to Saturday.")
        elif "fees" in text or "charge" in text or "cost" in text:
            bot.send_message(chat_id, "The consultation fee is ₹500.")
        elif "website" in text:
            bot.send_message(chat_id, "You can visit our website for more info:--------------", parse_mode='Markdown')
        elif "book" in text or "appointment" in text:
            bot.send_message(chat_id, "Alright, let's get started. What's your name?")
            user_data[chat_id] = {}
            bot.register_next_step_handler(message, process_name)
        else:
            bot.send_message(chat_id, "I'm not sure about that. You can ask about our address, timing, fees, or website.")
        user_data[chat_id]['asked_help'] = False
        return
    
    appointment_keywords = ['appointment','yes', 'yess','book', 'i want', 'see doctor', 'checkup', 'doctor', 'consult', 'schedule']

    if any(word in text for word in appointment_keywords):
        msg = bot.send_message(message.chat.id, "Great! Let's get started. What's your name?")
        user_data[message.chat.id] = {}
        bot.register_next_step_handler(msg, process_name)
        return
    
    if text in ['no', 'nope', 'not now', 'nah']:
        bot.send_message(message.chat.id, "Alright, how can I help you?")
        user_data[chat_id] = {'asked_help': True}
        return

    known_intents = {
        'headache': "I'm sorry you're feeling unwell. Want to book an appointment?",
        'help': "I can help you book a doctor appointment. Just say 'I want to book'.",
        'joke': "Why don't programmers like nature? It has too many bugs. 😄 Need a doctor? Just say so.",
        'bored': "Let's do something useful! Need a checkup? Say 'book appointment'."
    }

    for key in known_intents:
        if key in text:
            bot.send_message(message.chat.id, known_intents[key])
            return

    reply = get_chatbot_response(text)
    bot.send_message(message.chat.id, f"Do you want to book an appointment.")

def process_name(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_name")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your name. Please enter your name.")
            bot.register_next_step_handler(msg, process_name)
            return
            
        name = message.text.strip()
        if not name.replace(" ", "").isalpha():
            msg = bot.send_message(chat_id, "That doesn't seem like a valid name. Please enter your full name (letters only).")
            bot.register_next_step_handler(msg, process_name)
            return
        
        user_data[chat_id] = {'name': name}
        msg = bot.send_message(chat_id, f"OK {name}, now please enter your contact number.")
        bot.register_next_step_handler(msg, process_contact)
    except Exception as e:
        print(f"Error in process_name: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please enter your name again.")
            bot.register_next_step_handler(msg, process_name)
        return

def process_contact(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_contact")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your contact number. Please enter your contact number.")
            bot.register_next_step_handler(msg, process_contact)
            return
            
        contact = message.text.strip()
        # Validate contact number - should be 10 digits
        if not contact.isdigit() or len(contact) != 10:
            msg = bot.send_message(chat_id, "Invalid contact number. Please enter a 10-digit mobile number")
            bot.register_next_step_handler(msg, process_contact)
            return
        
        user_data[chat_id]['contact'] = contact
        msg = bot.send_message(chat_id, "Enter your address.")
        bot.register_next_step_handler(msg, process_address)
    except Exception as e:
        print(f"Error in process_contact: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please enter your contact number again.")
            bot.register_next_step_handler(msg, process_contact)
        return

def process_address(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_address")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your address. Please enter your address.")
            bot.register_next_step_handler(msg, process_address)
            return
            
        address = message.text.strip()
        if len(address) < 3:  # Basic validation for address
            msg = bot.send_message(chat_id, "That address seems too short. Please provide a complete address.")
            bot.register_next_step_handler(msg, process_address)
            return
            
        user_data[chat_id]['address'] = address
        msg = bot.send_message(chat_id, f"What problem are you facing?")
        bot.register_next_step_handler(msg, process_treatment)
    except Exception as e:
        print(f"Error in process_address: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please enter your address again.")
            bot.register_next_step_handler(msg, process_address)
        return

def process_treatment(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_treatment")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your problem description. Please describe the health issue you're facing.")
            bot.register_next_step_handler(msg, process_treatment)
            return
        
        problem = message.text.strip()
        if not problem:
            msg = bot.send_message(chat_id, "Problem description cannot be empty. Please describe the health issue you're facing.")
            bot.register_next_step_handler(msg, process_treatment)
            return
        
        user_data[chat_id]['problem'] = problem
        msg = bot.send_message(chat_id, "Please enter your gender (male/female/other).")
        bot.register_next_step_handler(msg, process_gender)
    except Exception as e:
        print(f"Error in process_treatment: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please describe your health issue again.")
            bot.register_next_step_handler(msg, process_treatment)
        return

def process_gender(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_gender")
            return
            
        chat_id = message.chat.id
        if not message.text:
            user_data[chat_id]['score'] = 0
            msg = bot.send_message(chat_id, "I didn't receive your gender. Please indicate your gender (male/female/other).")
            bot.register_next_step_handler(msg, process_gender)
            return
        
        gender = message.text.lower().strip()
        valid_genders = ["male", "female", "m", "f", "man", "woman", "other", "non-binary"]
        if not any(g in gender for g in valid_genders):
            msg = bot.send_message(chat_id, "Please enter a valid gender (male/female/other).")
            bot.register_next_step_handler(msg, process_gender)
            return
        
        user_data[chat_id]['gender'] = gender
        msg = bot.send_message(chat_id, "Please enter your age.")
        bot.register_next_step_handler(msg, process_age)
    except Exception as e:
        print(f"Error in process_gender: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please specify your gender again.")
            bot.register_next_step_handler(msg, process_gender)
        return

def process_age(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_age")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your age. Please enter your age.")
            bot.register_next_step_handler(msg, process_age)
            return
            
        age_text = message.text.strip()
        try:
            age = int(age_text)
            if age < 0 or age > 120:
                msg = bot.send_message(chat_id, "Please enter a valid age between 0 and 120.")
                bot.register_next_step_handler(msg, process_age)
                return
        except ValueError:
            msg = bot.send_message(chat_id, "Please enter your age as a number.")
            bot.register_next_step_handler(msg, process_age)
            return
        
        user_data[chat_id]['age'] = age
        msg = bot.send_message(chat_id, "Please enter your weight in kg.")
        bot.register_next_step_handler(msg, process_weight)
    except Exception as e:
        print(f"Error in process_age: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please enter your age again.")
            bot.register_next_step_handler(msg, process_age)
        return
    
    age_text = message.text.strip()
    try:
        age = int(age_text)
        if age < 0 or age > 120:
            msg = bot.send_message(chat_id, "Please enter a valid age between 0 and 120.")
            bot.register_next_step_handler(msg, process_age)
            return
    except ValueError:
        msg = bot.send_message(chat_id, "Please enter your age as a numeric value (e.g., 25).")
        bot.register_next_step_handler(msg, process_age)
        return
    
    user_data[chat_id]['age'] = age
    msg = bot.send_message(chat_id, "Please enter your weight in kg.")
    bot.register_next_step_handler(msg, process_weight)

def process_weight(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_weight")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your weight. Please enter your weight in kg.")
            bot.register_next_step_handler(msg, process_weight)
            return
        
        weight_text = message.text.strip()
        try:
            weight = float(weight_text)
            if weight < 0 or weight > 500:
                msg = bot.send_message(chat_id, "Please enter a valid weight between 0 and 500 kg.")
                bot.register_next_step_handler(msg, process_weight)
                return
        except ValueError:
            msg = bot.send_message(chat_id, "Please enter your weight as a numeric value (e.g., 70.5).")
            bot.register_next_step_handler(msg, process_weight)
            return
        
        user_data[chat_id]['weight'] = weight
        msg = bot.send_message(chat_id, "Did you visit our clinic prior?")
        bot.register_next_step_handler(msg, process_visit)
    except Exception as e:
        print(f"Error in process_weight: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please enter your weight again.")
            bot.register_next_step_handler(msg, process_weight)
        return

def process_visit(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_visit")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have visited our clinic before.")
            bot.register_next_step_handler(msg, process_visit)
            return
        
        response = message.text.lower().strip()
        if not any(answer in response for answer in ["yes", "y", "yeah", "no", "n", "nope"]):
            msg = bot.send_message(chat_id, "Please answer with 'yes' or 'no' if you have visited our clinic before.")
            bot.register_next_step_handler(msg, process_visit)
            return
        
        user_data[chat_id]['prior_visit'] = response
        msg = bot.send_message(chat_id, "Thank you for your cooperation, we need some more info about you which will help doctor to know more about your problem. If you wish to proceed further then just type 'yes' or else 'no', then we will move towards next step.")
        bot.register_next_step_handler(msg, ask_additional_info)
    except Exception as e:
        print(f"Error in process_visit: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you have visited our clinic before.")
            bot.register_next_step_handler(msg, process_visit)
        return

def ask_additional_info(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in ask_additional_info")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please type 'yes' if you want to provide additional information or 'no' to proceed.")
            bot.register_next_step_handler(msg, ask_additional_info)
            return
        
        response = message.text.lower().strip()
        if any(answer in response for answer in ["yes", "y", "yeah", "sure", "ok"]):
            if user_data[chat_id].get('gender', '').startswith(('f', 'woman', 'female')):
                msg = bot.send_message(chat_id, "Are you currently pregnant?")
                bot.register_next_step_handler(msg, process_pregnancy_status)
            else:
                msg = bot.send_message(chat_id, "Do you have any other symptoms?")
                bot.register_next_step_handler(msg, process_other_symptoms)
        else:
            msg = bot.send_message(chat_id, "On which date would you like to schedule your appointment? Please enter in DD-MM-YYYY format (e.g., 02-07-2025).")
            bot.register_next_step_handler(msg, process_date)
    except Exception as e:
        print(f"Error in ask_additional_info: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you want to provide additional information.")
            bot.register_next_step_handler(msg, ask_additional_info)
        return

def process_pregnancy_status(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_pregnancy_status")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you are pregnant.")
            bot.register_next_step_handler(msg, process_pregnancy_status)
            return
        
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response:
            score = 50  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 10
        
        # Initialize score if it doesn't exist
        if 'score' not in user_data[chat_id]:
            user_data[chat_id]['score'] = 0
            
        user_data[chat_id]['score'] += score
        user_data[chat_id]['pregnancy_status'] = response
        msg = bot.send_message(chat_id, "Are you currently using any contraception?")
        bot.register_next_step_handler(msg, process_contraception_use)
    except Exception as e:
        print(f"Error in process_pregnancy_status: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you are pregnant.")
            bot.register_next_step_handler(msg, process_pregnancy_status)
        return

def process_contraception_use(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_contraception_use")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you are currently using any contraception.")
            bot.register_next_step_handler(msg, process_contraception_use)
            return
        
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response:
            score = 35  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 10
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['contraception_use'] = response
        msg = bot.send_message(chat_id, "Are you experiencing any menstrual irregularities?")
        bot.register_next_step_handler(msg, process_menstrual_issues)
    except Exception as e:
        print(f"Error in process_contraception_use: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you are currently using any contraception.")
            bot.register_next_step_handler(msg, process_contraception_use)
        return

def process_menstrual_issues(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_menstrual_issues")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you are experiencing any menstrual irregularities.")
            bot.register_next_step_handler(msg, process_menstrual_issues)
            return
        
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response:
            score = 45  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 10
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['menstrual_issues'] = response
        msg = bot.send_message(chat_id, "Have you gone through menopause? (If applicable)")
        bot.register_next_step_handler(msg, process_menopause_status)
    except Exception as e:
        print(f"Error in process_menstrual_issues: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you are experiencing any menstrual irregularities.")
            bot.register_next_step_handler(msg, process_menstrual_issues)
        return

def process_menopause_status(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_menopause_status")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have gone through menopause (if applicable).")
            bot.register_next_step_handler(msg, process_menopause_status)
            return
        
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response:
            score = 30  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['menopause_status'] = response
        msg = bot.send_message(chat_id, "Do you have any other symptoms like fever, Fatigue, weakness,Dizziness, light-headedness, Nausea or vomiting?")
        bot.register_next_step_handler(msg, process_other_symptoms)
    except Exception as e:
        print(f"Error in process_menopause_status: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you have gone through menopause.")
            bot.register_next_step_handler(msg, process_menopause_status)
        return

def process_other_symptoms(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_other_symptoms")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your symptoms. Please describe any symptoms you're experiencing.")
            bot.register_next_step_handler(msg, process_other_symptoms)
            return
            
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response or 'fever' in response or 'Dizziness' in response or 'Fatigue' in response or 'Nausea' in response or 'vomiting' in response:
            score = 40  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['other_symptoms'] = response
        msg = bot.send_message(chat_id, "Do you have any known allergies?")
        bot.register_next_step_handler(msg, process_allergies)
    except Exception as e:
        print(f"Error in process_other_symptoms: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please describe any symptoms you're experiencing again.")
            bot.register_next_step_handler(msg, process_other_symptoms)
        return

def process_allergies(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_allergies")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response about allergies. Please let me know if you have any allergies.")
            bot.register_next_step_handler(msg, process_allergies)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response:
            score = 25  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['allergies'] = response
        msg = bot.send_message(chat_id, "Is the pain mild, moderate, or severe?")
        bot.register_next_step_handler(msg, process_pain_level)
    except Exception as e:
        print(f"Error in process_allergies: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you have any known allergies.")
            bot.register_next_step_handler(msg, process_allergies)
        return

def process_pain_level(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_pain_level")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your pain level. Please indicate if your pain is mild, moderate, or severe.")
            bot.register_next_step_handler(msg, process_pain_level)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'sever' in response:
            score = 50  # Higher score for pregnancy
        elif 'moderate' in response:
            score = 30
        else:
            score= 0
        user_data[chat_id]['score'] += score
        user_data[chat_id]['pain_level'] = response
        msg = bot.send_message(chat_id, "How did the symptoms start—suddenly or gradually?")
        bot.register_next_step_handler(msg, process_symptom_onset)
    except Exception as e:
        print(f"Error in process_pain_level: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if your pain is mild, moderate, or severe.")
            bot.register_next_step_handler(msg, process_pain_level)
        return

def process_symptom_onset(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_symptom_onset")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if your symptoms started suddenly or gradually.")
            bot.register_next_step_handler(msg, process_symptom_onset)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response or 'suddenly' in response:
            score = 40  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 10
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['symptom_onset'] = response
        msg = bot.send_message(chat_id, "Have you tried any treatments before coming here?")
        bot.register_next_step_handler(msg, process_previous_treatments)
    except Exception as e:
        print(f"Error in process_symptom_onset: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if your symptoms started suddenly or gradually.")
            bot.register_next_step_handler(msg, process_symptom_onset)
        return

def process_previous_treatments(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_previous_treatments")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you've tried any treatments before coming here.")
            bot.register_next_step_handler(msg, process_previous_treatments)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response:
            score = 0  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 20
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['previous_treatments'] = response
        msg = bot.send_message(chat_id, "Have you noticed weight loss or gain?")
        bot.register_next_step_handler(msg, process_weight_changes)
    except Exception as e:
        print(f"Error in process_previous_treatments: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you've tried any treatments before coming here.")
            bot.register_next_step_handler(msg, process_previous_treatments)
        return

def process_weight_changes(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_weight_changes")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you've noticed any weight loss or gain.")
            bot.register_next_step_handler(msg, process_weight_changes)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response or 'loss' in response:
            score = 25  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['weight_changes'] = response
        msg = bot.send_message(chat_id, "Have you had similar problems in the past?")
        bot.register_next_step_handler(msg, process_past_problems)
    except Exception as e:
        print(f"Error in process_weight_changes: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you've noticed any weight loss or gain.")
            bot.register_next_step_handler(msg, process_weight_changes)
        return

def process_past_problems(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_past_problems")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you've had similar problems in the past.")
            bot.register_next_step_handler(msg, process_past_problems)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response:
            score = 25  # Higher score for pregnancy
        elif 'no' in response or 'nope' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['past_problems'] = response
        msg = bot.send_message(chat_id, "Do you have any chronic conditions like diabetes, high BP, asthma, etc.?")
        bot.register_next_step_handler(msg, process_chronic_conditions)
    except Exception as e:
        print(f"Error in process_past_problems: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you've had similar problems in the past.")
            bot.register_next_step_handler(msg, process_past_problems)
        return

def process_chronic_conditions(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_chronic_conditions")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have any chronic conditions like diabetes, high BP, asthma, etc.")
            bot.register_next_step_handler(msg, process_chronic_conditions)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response or 'diabetes' in response or 'high bp' in response or 'asthma' in response:
            score = 35  # Higher score for chronic conditions
        elif 'no' in response or 'nope' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['chronic_conditions'] = response
        msg = bot.send_message(chat_id, "Are you currently taking any medications?")
        bot.register_next_step_handler(msg, process_medications)
    except Exception as e:
        print(f"Error in process_chronic_conditions: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you have any chronic conditions.")
            bot.register_next_step_handler(msg, process_chronic_conditions)
        return

def process_surgeries(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_surgeries")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have undergone any surgeries.")
            bot.register_next_step_handler(msg, process_surgeries)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response:
            score = 20  # Higher score for previous surgeries
        elif 'no' in response or 'nope' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['surgeries'] = response
        msg = bot.send_message(chat_id, "Are you currently taking any medications?")
        bot.register_next_step_handler(msg, process_medications)
    except Exception as e:
        print(f"Error in process_surgeries: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you have undergone any surgeries.")
            bot.register_next_step_handler(msg, process_surgeries)
        return

def process_smoking_drinking(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_smoking_drinking")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you smoke or drink alcohol.")
            bot.register_next_step_handler(msg, process_smoking_drinking)
            return
        response = message.text.lower().strip()
        score = 0
        
        if 'yes' in response or 'yess' in response or 'smoke' in response or 'drinking' in response or 'alcohol' in response:
            score = 25  # Higher score for smoking/drinking
        elif 'no' in response or 'nope' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['smoking_drinking'] = response
        msg = bot.send_message(chat_id, "Are you currently taking any medications?")
        bot.register_next_step_handler(msg, process_medications)
    except Exception as e:
        print(f"Error in process_smoking_drinking: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you smoke or drink alcohol.")
            bot.register_next_step_handler(msg, process_smoking_drinking)
        return

def process_exercise(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_exercise")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you exercise regularly.")
            bot.register_next_step_handler(msg, process_exercise)
            return
        response = message.text.lower().strip()
        
        # Process the response
        score = 0
        if 'yes' in response or 'regularly' in response:
            score = -10  # Lower score for regular exercise (good for health)
        elif 'no' in response or 'nope' in response or 'rarely' in response or 'never' in response:
            score = 10  # Higher score for lack of exercise
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['exercise'] = response
        msg = bot.send_message(chat_id, "Do you have a family history of any medical conditions?")
        bot.register_next_step_handler(msg, process_family_history)
    except Exception as e:
        print(f"Error in process_exercise: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you exercise regularly.")
            bot.register_next_step_handler(msg, process_exercise)
        return


def process_family_history(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_family_history")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have a family history of any medical conditions.")
            bot.register_next_step_handler(msg, process_family_history)
            return
        response = message.text.lower().strip()
        
        # Process the response
        score = 0
        if 'yes' in response or 'history' in response:
            score = 15  # Higher score for family history of medical conditions
        elif 'no' in response or 'nope' in response or 'none' in response:
            score = 0
        
        user_data[chat_id]['score'] += score
        user_data[chat_id]['family_history'] = response
        msg = bot.send_message(chat_id, "On which date would you like to schedule your appointment? Please enter in DD-MM-YYYY format (e.g., 02-07-2025).")
        bot.register_next_step_handler(msg, process_date)
    except Exception as e:
        print(f"Error in process_family_history: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error. Please indicate if you have a family history of any medical conditions.")
            bot.register_next_step_handler(msg, process_family_history)
        return

def process_date(message):
    try:
        # Check if message is valid
        if message is None or not hasattr(message, 'chat') or not hasattr(message, 'text'):
            print("Error: Invalid message object in process_date")
            return
            
        chat_id = message.chat.id
        if not message.text:
            msg = bot.send_message(chat_id, "I didn't receive your preferred date. Please enter a date for your appointment.")
            bot.register_next_step_handler(msg, process_date)
            return
        
        appointment_date = message.text.strip()
        import re
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', appointment_date):
            msg = bot.send_message(chat_id, "Please enter the date in DD-MM-YYYY format (e.g., 02-07-2025).")
            bot.register_next_step_handler(msg, process_date)
            return
        
        try:
            day, month, year = map(int, appointment_date.split('-'))
            if month < 1 or month > 12 or year < 2023 or day < 1:
                msg = bot.send_message(chat_id, "Please enter a valid future date in DD-MM-YYYY format.")
                bot.register_next_step_handler(msg, process_date)
                return
            
            days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
                days_in_month[2] = 29
                
            if day > days_in_month[month]:
                msg = bot.send_message(chat_id, f"Invalid date: {appointment_date}. The month {month} doesn't have {day} days.")
                bot.register_next_step_handler(msg, process_date)
                return
            
            today = datetime.datetime.now().date()
            appointment_datetime = datetime.date(year, month, day)
            
            if appointment_datetime < today:
                msg = bot.send_message(chat_id, "Please enter a future date for your appointment.")
                bot.register_next_step_handler(msg, process_date)
                return
                
        except ValueError:
            msg = bot.send_message(chat_id, "Please enter the date in DD-MM-YYYY format (e.g., 02-07-2025).")
            bot.register_next_step_handler(msg, process_date)
            return
        
        user_data[chat_id]['appointment_date'] = appointment_date
        
        total_score = 0
        try:
            total_score = user_data[chat_id].get('score', 0)
        except Exception as e:
            print(f"Error retrieving score: {e}")
            total_score = 0

        if total_score >= 200:
            risk_level = "Emergency"
        elif total_score >= 100:
            risk_level = "Urgent"
        else:
            risk_level = "Routine"

        bot.send_message(chat_id, f"Your requested appointment date: {message.text}")
        bot.send_message(chat_id, f"Your total priority score is: {total_score}")
        bot.send_message(chat_id, f"Risk Assessment: {risk_level}")

        now = datetime.datetime.now()
        user_data[chat_id]['points'] = total_score
        user_data[chat_id]['date'] = now 
        user_data[chat_id]['risk_level'] = risk_level

        query = """INSERT INTO appointments (name, contact, address, age, weight, appointment_date,gender,pregnancy_status,days,prior_visit,points,date,problem,risk_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
    
        try:
            age = int(user_data[chat_id]['age'])
        except (ValueError, KeyError):
            age = 0
        
        try:
            weight = float(user_data[chat_id]['weight'])
        except (ValueError, KeyError):
            weight = 0.0
        
        try:
            days = int(user_data[chat_id].get('days', 0))
        except ValueError:
            days = 0

        values = (
            user_data[chat_id].get('name', 'Unknown'),
            user_data[chat_id].get('contact', 'Unknown'),
            user_data[chat_id].get('address', 'Unknown'),
            age,
            weight,
            user_data[chat_id].get('appointment_date', 'Unknown'),
            user_data[chat_id].get('gender', ''),
            user_data[chat_id].get('pregnancy_status', 'N/A'), 
            days,
            user_data[chat_id].get('prior_visit', 'Unknown'),
            total_score,
            now,
            user_data[chat_id].get('problem', 'Unknown'),
            risk_level
        )
    
        try:
            if db is not None and cursor is not None:
                cursor.execute(query, values)
                db.commit()
                bot.send_message(chat_id, "✅ Your appointment has been successfully saved to our database.")
            else:
                bot.send_message(chat_id, "❌ Database connection is not available. Your appointment information has been recorded but not saved to the database.")
        except mysql.connector.Error as err:
            error_msg = str(err)
            if "Duplicate entry" in error_msg:
                bot.send_message(chat_id, "❌ You already have an appointment scheduled. Please contact the hospital directly for changes.")
            else:
                bot.send_message(chat_id, f"❌ Database error: {error_msg[:100]}... Your appointment information has been recorded but not saved to the database.")
            print(f"Database error in process_date: {err}")
        except Exception as e:
            bot.send_message(chat_id, f"❌ Unexpected error: {str(e)[:100]}... Your appointment information has been recorded but not saved to the database.")
            print(f"Unexpected error in process_date: {e}")

        payload = {
            'name': user_data[chat_id].get('name', 'Unknown'),
            'contact': user_data[chat_id].get('contact', 'Unknown'),
            'address': user_data[chat_id].get('address', 'Unknown'),
            'age': user_data[chat_id].get('age', '0'),
            'weight': user_data[chat_id].get('weight', '0'),
            'appointment_date': user_data[chat_id].get('appointment_date', 'Unknown'),
            'gender': user_data[chat_id].get('gender', ''),
            'pregnancy_status': user_data[chat_id].get('pregnancy_status', 'N/A'),
            'days': user_data[chat_id].get('days', 0),
            'prior_visit': user_data[chat_id].get('prior_visit', 'Unknown'),
            'points': total_score,
            'problem': user_data[chat_id].get('problem', 'N/A'),
            'risk_level': risk_level,
            'date': now.strftime('%Y-%m-%d %H:%M:%S')
        }

        if payload:
            try:
                response = requests.post("http://127.0.0.1:5001/notify", json=payload, timeout=5)
                if response.status_code == 200:
                    bot.send_message(chat_id, "✅ Appointment saved and sent to hospital system.")
                else:
                    bot.send_message(chat_id, f"⚠️ Appointment saved, but hospital system returned error code: {response.status_code}")
            except Exception as e:
                bot.send_message(chat_id, f"⚠️ Appointment saved, but failed to notify hospital system. Error: {str(e)[:100]}...")

        confirmation_msg = f"📅 Appointment Summary:\n" + \
                          f"Name: {user_data[chat_id].get('name', 'Unknown')}\n" + \
                          f"Date: {user_data[chat_id].get('appointment_date', 'Unknown')}\n" + \
                          f"Priority: {risk_level}\n\n" + \
                          f"Thank you for using our appointment system. If you need to make changes, please contact the hospital directly."
        bot.send_message(chat_id, confirmation_msg)
    except Exception as e:
        print(f"Error in process_date: {e}")
        if hasattr(message, 'chat') and hasattr(message.chat, 'id'):
            msg = bot.send_message(message.chat.id, "Sorry, I encountered an error processing your appointment date. Please try again.")
            bot.register_next_step_handler(msg, process_date)

if __name__ == "__main__":
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', 12345))
        bot.remove_webhook()
        print("Starting Telegram bot polling...")
        bot.polling(none_stop=True, interval=0)
    except socket.error:
        print("ERROR: Another instance of this bot is already running!")
    finally:
        sock.close()