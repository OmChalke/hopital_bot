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
    ['how is the weather', ['I’m not sure, I live in the cloud ☁']],
    ['are you happy', ['I’m just code, but I love talking to you!']],
    ['(.*) your hobby', ['Chatting with people like you.']],
    ['my name is (.*)', ['Nice to meet you, %1!']],
    ['(hi|hello|hey|hii|heyy)', ['Hello!', 'Hi there!', 'Hey!', 'Greetings!']],
    ['good (morning|afternoon|evening)', ['Good %1 to you too!']],
    ['howdy', ['Howdy partner!']],
    ['(bye|goodbye|see you|see ya)', ['Bye!', 'Goodbye!', 'See you later!', 'Take care!']],
    ['(exit|quit)', ['Goodbye! Type again if you need anything.', 'Session ended.']],
    ['how are you', ['I’m doing great, thanks! How about you?']],
    ['(i am|i\'m) (fine|good|okay|not good|sad|happy)', ['Glad to hear that!', 'Oh, I hope you feel better soon.']],
    ['what is your name', ['My name is ChatBot, your assistant!']],
    ['who are you', ['I am a rule-based chatbot created to talk with you.']],
    ['are you real', ['I’m virtual, but I’m here for you!']],
    ['(help|assist) me', ['Sure! I’ll do my best. What do you need help with?']],
    ['can you help me with (.*)', ['I can try to help with %1. What exactly do you need?']],
    ['tell me a joke', ['Why don’t scientists trust atoms? Because they make up everything!', 'Why was the math book sad? It had too many problems.']],
    ['make me laugh', ['I would, but I only know bad jokes 😅']],
    ['i feel (sad|down|upset)', ['I’m sorry to hear that. I’m here for you.']],
    ['i feel (happy|good|great)', ['That’s wonderful to hear!']],
    ['i\'m bored', ['Let’s chat! Or I can tell you a joke.']],
    ['what time is it', ['I’m not wearing a watch 😄, but your system clock knows!']],
    ['what day is it', ['Check your calendar, but I think it’s a great day!']],
    ['do you like (.*)', ['I don’t have preferences, but %1 sounds interesting!']],
    ['i like (.*)', ['Cool! %1 is nice.']],
    ['i hate (.*)', ['Oh no! Why do you hate %1?']],
    ['are you single', ['Haha! I’m committed to chatting with you 😄']],
    ['do you have a girlfriend', ['Nope, I’m just a bunch of code!']],
    ['do you sleep', ['Nope, I’m always awake for you.']],
    ['where do you live', ['I live in your device – or maybe in the cloud!']],
    ['how old are you', ['I was created recently, but I’m learning fast!']],
    ['what is life', ['42! Just kidding. It’s what you make of it.']],
    ['do you believe in god', ['I don’t have beliefs, but many people do.']],
    ['do you know me', ['I’m getting to know you more each time we chat!']],
    ['(thank you|thanks)', ['You’re welcome!', 'Anytime!', 'Glad to help!']],
    ['thanks a lot', ['It’s my pleasure!']],
    ['(.*)', ['Interesting...', 'Tell me more.', 'Why do you say that?', 'Let’s talk about something else.']]
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


# Initialize database connection with error handling
try:
    db = mysql.connector.connect(**mysql_config)
    cursor = db.cursor()
    print("Database connection established successfully")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL database: {err}")
    # Set defaults that will allow the bot to start even if DB connection fails
    db = None
    cursor = None
except Exception as e:
    print(f"Unexpected error during database connection: {e}")
    db = None
    cursor = None

bot = telebot.TeleBot('7121615580:AAEcXUik52npkXXmTPUxUd2ZNLf26Tp6e7o')

user_data={}

@bot.message_handler(commands=['start', 'hello']) 
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, "hiee", reply_markup=markup)

 
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.lower().strip()
    chat_id = message.chat.id

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
        'joke': "Why don’t programmers like nature? It has too many bugs. 😄 Need a doctor? Just say so.",
        'bored': "Let’s do something useful! Need a checkup? Say 'book appointment'."
    }

    for key in known_intents:
        if key in text:
            bot.send_message(message.chat.id, known_intents[key])
            return

    reply = get_chatbot_response(text)
    bot.send_message(message.chat.id, f"Do you want to book an appointment.")


def process_name(message):
    name = message.text.strip()

    if not name.replace(" ", "").isalpha():
        msg = bot.send_message(message.chat.id, "That doesn't seem like a valid name. Please enter your full name (letters only).")
        bot.register_next_step_handler(msg, process_name)
        return

    # Initialize user data dictionary if it doesn't exist
    try:
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {}
        user_data[message.chat.id]['name'] = name
        print(f"Name saved for user {message.chat.id}: {name}")
    except Exception as e:
        print(f"Error saving name for user {message.chat.id}: {e}")
        # Create a new dictionary if there was an error
        user_data[message.chat.id] = {'name': name}

    msg = bot.send_message(message.chat.id, f"OK {name}, now please enter your contact number.")
    bot.register_next_step_handler(msg, process_contact)
   

def process_contact(message):
    contact = message.text.strip()
    if len(contact) != 10:
        msg = bot.send_message(message.chat.id, "Invalid contact number. Please enter a 10-digit mobile number")
        bot.register_next_step_handler(msg, process_contact)
        return
    
    user_data[message.chat.id].update({'contact': message.text})
    bot.send_message(message.chat.id, f"Thanks! We've saved your contact: {message.text}")
    msg= bot.send_message(message.chat.id, "Enter your address.")
    bot.register_next_step_handler(msg, process_address)

def process_address(message):
    user_data[message.chat.id].update({'address': message.text})
    bot.send_message(message.chat.id,f"Your address has been no ted: {message.text}")
    msg= bot.send_message(message.chat.id, f"Enter your Age")
    bot.register_next_step_handler(msg, process_age)

def process_age(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your age. Please enter your age.")
        bot.register_next_step_handler(msg, process_age)
        return
    
    # Get and validate age
    age_text = message.text.strip()
    
    # Check if age is empty
    if not age_text:
        msg = bot.send_message(chat_id, "Age cannot be empty. Please enter your age.")
        bot.register_next_step_handler(msg, process_age)
        return
    
    # Try to convert age to integer
    try:
        age = int(age_text)
        
        # Validate age range
        if age < 0 or age > 120:  # Reasonable age range
            msg = bot.send_message(chat_id, "Please enter a valid age between 0 and 120.")
            bot.register_next_step_handler(msg, process_age)
            return
            
    except ValueError:
        msg = bot.send_message(chat_id, "Please enter a valid numeric age.")
        bot.register_next_step_handler(msg, process_age)
        return
    
    # Update user data with validated age
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        user_data[chat_id].update({'age': age})
        bot.send_message(chat_id,f"Your noted age is: {age}")
    except Exception as e:
        print(f"Error saving age for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'age': age}
        else:
            user_data[chat_id]['age'] = age
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, f"Enter your wieght")
        bot.register_next_step_handler(msg, process_weight)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_weight(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your weight. Please enter your weight in kg.")
        bot.register_next_step_handler(msg, process_weight)
        return
    
    # Get and validate weight
    weight_text = message.text.strip()
    
    # Check if weight is empty
    if not weight_text:
        msg = bot.send_message(chat_id, "Weight cannot be empty. Please enter your weight in kg.")
        bot.register_next_step_handler(msg, process_weight)
        return
    
    # Try to convert weight to float
    try:
        weight = float(weight_text)
        
        # Validate weight range (reasonable human weight range in kg)
        if weight <= 0 or weight > 500:  
            msg = bot.send_message(chat_id, "Please enter a valid weight between 0 and 500 kg.")
            bot.register_next_step_handler(msg, process_weight)
            return
            
    except ValueError:
        msg = bot.send_message(chat_id, "Please enter a valid numeric weight.")
        bot.register_next_step_handler(msg, process_weight)
        return
    
    # Update user data with validated weight
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        user_data[chat_id].update({'weight': weight})
        bot.send_message(chat_id,f"Yours weight is: {weight}")
    except Exception as e:
        print(f"Error saving weight for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'weight': weight}
        else:
            user_data[chat_id]['weight'] = weight
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, f"What problem are you facing")
        bot.register_next_step_handler(msg, process_treatment)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_treatment(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your problem description. Please describe the health issue you're facing.")
        bot.register_next_step_handler(msg, process_treatment)
        return
    
    # Get and validate problem description
    problem = message.text.strip()
    
    # Check if problem description is empty
    if not problem:
        msg = bot.send_message(chat_id, "Problem description cannot be empty. Please describe the health issue you're facing.")
        bot.register_next_step_handler(msg, process_treatment)
        return
    
    # Update user data with validated problem description
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        user_data[chat_id].update({'problem': problem})
    except Exception as e:
        print(f"Error saving problem description for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'problem': problem}
        else:
            user_data[chat_id]['problem'] = problem
    
    # Proceed to next step
    msg = bot.send_message(message.chat.id, "Do you have fever, fatigue, nausea, dizziness, or any other symptoms?")
    bot.register_next_step_handler(msg, process_other_symptoms)

def process_other_symptoms(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your symptoms. Please describe any symptoms you're experiencing.")
        bot.register_next_step_handler(msg, process_other_symptoms)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response or 'fever' in response or 'nausea' in response or 'weakness' in response or 'dizziness' in response:
        score = 30
    elif 'no' in response or 'nope' in response:
        score = 10
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Do you have any known allergies?")
        bot.register_next_step_handler(msg, process_allergies)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_allergies(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response about allergies. Please let me know if you have any allergies.")
        bot.register_next_step_handler(msg, process_allergies)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 20
    elif 'no' in response or 'nope' in response:
        score = 10
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Is the pain mild, moderate, or severe?")
        bot.register_next_step_handler(msg, process_pain_level)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_pain_level(message):    
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your pain level. Please indicate if your pain is mild, moderate, or severe.")
        bot.register_next_step_handler(msg, process_pain_level)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'sever' in response:
        score = 40
    elif 'moderate' in response:
        score = 20
    elif 'mild' in response:
        score = 10

    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "How did the symptoms start—suddenly or gradually?")
        bot.register_next_step_handler(msg, process_symptom_onset)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_symptom_onset(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if your symptoms started suddenly or gradually.")
        bot.register_next_step_handler(msg, process_symptom_onset)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'suddenly' in response:
        score = 30
    elif 'gradually' in response:
        score = 20
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Have you tried any treatments before coming here?")
        bot.register_next_step_handler(msg, process_previous_treatments)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_previous_treatments(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you've tried any treatments before coming here.")
        bot.register_next_step_handler(msg, process_previous_treatments)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 15
    elif 'no' in response or 'nope' in response:
        score = 30
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Have you noticed weight loss or gain?")
        bot.register_next_step_handler(msg, process_weight_changes)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_weight_changes(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you've noticed any weight loss or gain.")
        bot.register_next_step_handler(msg, process_weight_changes)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 40
    elif 'no' in response or 'nope' in response:
        score = 20
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Have you had similar problems in the past?")
        bot.register_next_step_handler(msg, process_past_problems)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_past_problems(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you've had similar problems in the past.")
        bot.register_next_step_handler(msg, process_past_problems)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 30
    elif 'no' in response or 'nope' in response:
        score = 25
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Do you have any chronic conditions like diabetes, high BP, asthma, etc.?")
        bot.register_next_step_handler(msg, process_chronic_conditions)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_chronic_conditions(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have any chronic conditions like diabetes, high BP, asthma, etc.")
        bot.register_next_step_handler(msg, process_chronic_conditions)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 40
    elif 'no' in response or 'nope' in response:
        score = 20
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Have you undergone any surgeries?")
        bot.register_next_step_handler(msg, process_surgeries)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_surgeries(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have undergone any surgeries.")
        bot.register_next_step_handler(msg, process_surgeries)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 40
    elif 'no' in response or 'nope' in response:
        score = 20
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Do you smoke or drink alcohol?")
        bot.register_next_step_handler(msg, process_smoking_drinking)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_smoking_drinking(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you smoke or drink alcohol.")
        bot.register_next_step_handler(msg, process_smoking_drinking)
        return
    
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 40
    elif 'no' in response or 'nope' in response:
        score = 10
    
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Do you exercise regularly?")
        bot.register_next_step_handler(msg, process_gender)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_gender(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you exercise regularly.")
        bot.register_next_step_handler(msg, process_gender)
        return
    
    # Get exercise information
    response = message.text.lower().strip()
    score = 0
    
    # Calculate score based on exercise habits
    if 'yes' in response or 'yess' in response:
        score = 10
    elif 'no' in response or 'nope' in response:
        score = 30
    
    # Update user data with score
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
        print(f"Score updated for user {chat_id} based on exercise habits. New score: {user_data[chat_id]['score']}")
    except Exception as e:
        print(f"Error updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'score': score}
        else:
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Are you male or female?")
        bot.register_next_step_handler(msg, process_gender_response)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

    
def process_gender_response(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate your gender (male/female).")
        bot.register_next_step_handler(msg, process_gender_response)
        return
    
    # Get gender information
    gender = message.text.lower().strip()
    
    # Validate gender input
    valid_genders = ["male", "female", "m", "f", "man", "woman", "other", "non-binary"]
    if not any(g in gender for g in valid_genders):
        msg = bot.send_message(chat_id, "Please enter a valid gender (male/female/other).")
        bot.register_next_step_handler(msg, process_gender_response)
        return
    
    # Update user data with gender information
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        user_data[chat_id].update({'gender': gender})
        print(f"Gender information saved for user {chat_id}: {gender}")
    except Exception as e:
        print(f"Error saving gender information for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'gender': gender}
        else:
            user_data[chat_id]['gender'] = gender
    
    # Proceed to next step based on gender
    try:
        if gender in ['female', 'f', 'woman']:
            msg = bot.send_message(chat_id, "Are you currently pregnant?")
            bot.register_next_step_handler(msg, process_pregnancy_status)
        else:
            msg = bot.send_message(chat_id, "From how many days are you facing this problem?")
            bot.register_next_step_handler(msg, ask_clinic_visit)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_pregnancy_status(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you are currently pregnant.")
        bot.register_next_step_handler(msg, process_pregnancy_status)
        return
    
    # Get pregnancy status information
    response = message.text.lower().strip()
    score = 0
    
    # Calculate score based on pregnancy status
    if any(answer in response for answer in ["yes", "y", "yeah", "pregnant", "expecting"]):
        score = 40
    elif any(answer in response for answer in ["no", "n", "nope", "not pregnant"]):
        score = 10
    else:
        # If response is unclear, ask for clarification
        msg = bot.send_message(chat_id, "Please answer with 'yes' or 'no' if you are currently pregnant.")
        bot.register_next_step_handler(msg, process_pregnancy_status)
        return
    
    # Update user data with pregnancy status and score
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        # Update pregnancy status
        user_data[chat_id].update({'pregnancy_status': response})
        print(f"Pregnancy status saved for user {chat_id}: {response}")
        
        # Update score
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
        print(f"Score updated for user {chat_id} based on pregnancy status. New score: {user_data[chat_id]['score']}")
    except Exception as e:
        print(f"Error saving pregnancy status or updating score for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'pregnancy_status': response, 'score': score}
        else:
            user_data[chat_id]['pregnancy_status'] = response
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Are you currently using any contraception?")
        bot.register_next_step_handler(msg, process_contraception_use)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_contraception_use(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you are currently using any contraception.")
        bot.register_next_step_handler(msg, process_contraception_use)
        return
    
    # Get contraception use information
    response = message.text.lower().strip()
    score = 0
    
    # Calculate score based on contraception use
    if any(answer in response for answer in ["yes", "y", "yeah", "using"]):
        score = 15
    elif any(answer in response for answer in ["no", "n", "nope", "not using"]):
        score = 10
    else:
        # If response is unclear, ask for clarification
        msg = bot.send_message(chat_id, "Please answer with 'yes' or 'no' if you are currently using any contraception.")
        bot.register_next_step_handler(msg, process_contraception_use)
        return
    
    # Update user data with score
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        # Update score
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
        print(f"Score updated for user {chat_id} based on contraception use. New score: {user_data[chat_id]['score']}")
        
        # Save contraception status
        user_data[chat_id].update({'contraception_use': response})
        print(f"Contraception use information saved for user {chat_id}: {response}")
    except Exception as e:
        print(f"Error updating score or saving contraception use for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'contraception_use': response, 'score': score}
        else:
            user_data[chat_id]['contraception_use'] = response
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Are you experiencing any menstrual irregularities?")
        bot.register_next_step_handler(msg, process_menstrual_issues)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_menstrual_issues(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you are experiencing any menstrual irregularities.")
        bot.register_next_step_handler(msg, process_menstrual_issues)
        return
    
    # Get menstrual issues information
    response = message.text.lower().strip()
    score = 0
    
    # Calculate score based on menstrual issues
    if any(answer in response for answer in ["yes", "y", "yeah", "irregular", "issues", "problems"]):
        score = 20
    elif any(answer in response for answer in ["no", "n", "nope", "regular", "normal"]):
        score = 10
    else:
        # If response is unclear, ask for clarification
        msg = bot.send_message(chat_id, "Please answer with 'yes' or 'no' if you are experiencing any menstrual irregularities.")
        bot.register_next_step_handler(msg, process_menstrual_issues)
        return
    
    # Update user data with score and menstrual issues information
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        # Update score
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
        print(f"Score updated for user {chat_id} based on menstrual issues. New score: {user_data[chat_id]['score']}")
        
        # Save menstrual issues information
        user_data[chat_id].update({'menstrual_issues': response})
        print(f"Menstrual issues information saved for user {chat_id}: {response}")
    except Exception as e:
        print(f"Error updating score or saving menstrual issues for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'menstrual_issues': response, 'score': score}
        else:
            user_data[chat_id]['menstrual_issues'] = response
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "Have you gone through menopause? (If applicable)")
        bot.register_next_step_handler(msg, process_menopause_status)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_menopause_status(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have gone through menopause (if applicable).")
        bot.register_next_step_handler(msg, process_menopause_status)
        return
    
    # Get menopause status information
    response = message.text.lower().strip()
    score = 0
    
    # Calculate score based on menopause status
    if any(answer in response for answer in ["yes", "y", "yeah", "gone through", "completed"]):
        score = 15
    elif any(answer in response for answer in ["no", "n", "nope", "not yet", "ongoing"]):
        score = 10
    elif any(answer in response for answer in ["na", "n/a", "not applicable", "male", "man"]):
        # Handle not applicable responses
        score = 0
    else:
        # If response is unclear, ask for clarification
        msg = bot.send_message(chat_id, "Please answer with 'yes', 'no', or 'not applicable' regarding menopause status.")
        bot.register_next_step_handler(msg, process_menopause_status)
        return
    
    # Update user data with score and menopause status
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            
        # Update score
        current_score = user_data[chat_id].get('score', 0)
        user_data[chat_id]['score'] = current_score + score
        print(f"Score updated for user {chat_id} based on menopause status. New score: {user_data[chat_id]['score']}")
        
        # Save menopause status
        user_data[chat_id].update({'menopause_status': response})
        print(f"Menopause status saved for user {chat_id}: {response}")
    except Exception as e:
        print(f"Error updating score or saving menopause status for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'menopause_status': response, 'score': score}
        else:
            user_data[chat_id]['menopause_status'] = response
            user_data[chat_id]['score'] = score
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "For how many days have you been facing this problem?")
        bot.register_next_step_handler(msg, ask_clinic_visit)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def ask_clinic_visit(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please enter the number of days you've been facing this problem.")
        bot.register_next_step_handler(msg, ask_clinic_visit)
        return
    
    # Store the raw input first
    days_text = message.text.strip()
    user_data[chat_id] = user_data.get(chat_id, {})
    user_data[chat_id].update({'days_text': days_text})
    
    # Try to convert to integer with comprehensive error handling
    try:
        days = int(days_text)
        
        # Validate the range
        if days < 0:
            msg = bot.send_message(chat_id, "The number of days cannot be negative. Please enter a valid number.")
            bot.register_next_step_handler(msg, ask_clinic_visit)
            return
        elif days > 365:  # Assuming symptoms for more than a year is unusual
            msg = bot.send_message(chat_id, "That's a very long time. Are you sure you've been facing this problem for more than a year? Please enter the number of days.")
            bot.register_next_step_handler(msg, ask_clinic_visit)
            return
            
        # Update user data with validated days
        user_data[chat_id].update({'days': days})
        
        # Calculate score based on days
        if days > 2:
            user_data[chat_id]['score'] = user_data[chat_id].get('score', 0) + 30
        else:
            user_data[chat_id]['score'] = user_data[chat_id].get('score', 0) + 10
            
        # Proceed to next step
        msg = bot.send_message(chat_id, "Did you visit our clinic prior?")
        bot.register_next_step_handler(msg, process_visit)
        
    except ValueError:
        # Handle non-numeric input
        msg = bot.send_message(chat_id, "Please enter the number of days as a numeric value (e.g., 5).")
        bot.register_next_step_handler(msg, ask_clinic_visit)
        return
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error in ask_clinic_visit: {e}")
        msg = bot.send_message(chat_id, "There was an error processing your response. Please enter the number of days again.")
        bot.register_next_step_handler(msg, ask_clinic_visit)
        return


def process_visit(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your response. Please indicate if you have visited our clinic before.")
        bot.register_next_step_handler(msg, process_visit)
        return
    
    # Get prior visit information
    response = message.text.lower().strip()
    
    # Validate response format
    if not any(answer in response for answer in ["yes", "y", "yeah", "no", "n", "nope"]):
        msg = bot.send_message(chat_id, "Please answer with 'yes' or 'no' if you have visited our clinic before.")
        bot.register_next_step_handler(msg, process_visit)
        return
    
    # Update user data with prior visit information
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
        
        # Save prior visit information
        user_data[chat_id].update({'prior_visit': response})
        print(f"Prior visit information saved for user {chat_id}: {response}")
    except Exception as e:
        print(f"Error saving prior visit information for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'prior_visit': response}
        else:
            user_data[chat_id]['prior_visit'] = response
    
    # Proceed to next step
    try:
        msg = bot.send_message(chat_id, "On which date would you like to schedule your appointment?")
        bot.register_next_step_handler(msg, process_date)
    except Exception as e:
        print(f"Error sending message or registering next step: {e}")
        # Try to recover by sending a simple message
        bot.send_message(chat_id, "There was an error processing your request. Please try again later.")
        return

def process_date(message):
    chat_id = message.chat.id
    
    # Validate that we have a message
    if not message or not message.text:
        msg = bot.send_message(chat_id, "I didn't receive your preferred date. Please enter a date for your appointment.")
        bot.register_next_step_handler(msg, process_date)
        return
    
    # Get appointment date information
    appointment_date = message.text.strip()
    
    # Basic date validation (could be enhanced with more sophisticated date parsing)
    if len(appointment_date) < 3:  # Very basic check for minimum meaningful date input
        msg = bot.send_message(chat_id, "Please enter a valid date format for your appointment.")
        bot.register_next_step_handler(msg, process_date)
        return
    
    # Update user data with appointment date
    try:
        # Ensure user_data dictionary exists for this chat_id
        if chat_id not in user_data:
            user_data[chat_id] = {}
            bot.send_message(chat_id, "I'm sorry, but your session data was lost. Let's restart the appointment process.")
            msg = bot.send_message(chat_id, "What's your name?")
            bot.register_next_step_handler(msg, process_name)
            return
        
        # Save appointment date
        user_data[chat_id].update({'appointment_date': appointment_date})
        print(f"Appointment date saved for user {chat_id}: {appointment_date}")
    except Exception as e:
        print(f"Error saving appointment date for user {chat_id}: {e}")
        # Try to recover by creating a new dictionary if needed
        if chat_id not in user_data:
            user_data[chat_id] = {'appointment_date': appointment_date}
        else:
            user_data[chat_id]['appointment_date'] = appointment_date
    
    # Calculate risk level based on score
    try:
        total_score = user_data[chat_id].get('score', 0)
        print(f"Retrieved total score for user {chat_id}: {total_score}")
    except Exception as e:
        print(f"Error retrieving score: {e}")
        total_score = 0
        bot.send_message(chat_id, "⚠️ There was an issue calculating your priority score.")
        print(f"Set default score of 0 for user {chat_id} due to error")


    now = datetime.datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    bot.send_message(chat_id, f"Your requested appointment date: {message.text}")
    bot.send_message(chat_id, f"Your total priority score is: {total_score}**")

    # Determine risk level with error handling
    try:
        if total_score >= 200:
            risk_level = "Emergency"
        elif total_score >= 100:
            risk_level = "Urgent"
        else:
            risk_level = "Routine"
    except Exception as e:
        print(f"Error determining risk level: {e}")
        risk_level = "Routine"  # Default to routine if there's an error
        bot.send_message(chat_id, "⚠️ There was an issue determining your risk level. Using default level.")

    bot.send_message(chat_id, f"Risk Assessment: {risk_level}")

    # Update user data with proper error handling
    try:
        user_data[chat_id]['points'] = total_score
        user_data[chat_id]['date'] = now 
        user_data[chat_id]['risk_level'] = risk_level
        user_data[chat_id]['x'] = now  # Ensure x is defined as the current datetime
    except Exception as e:
        print(f"Error updating user data: {e}")
        bot.send_message(chat_id, "⚠️ There was an issue updating your appointment information.")

    query = """INSERT INTO appointments (name, contact, address, age, weight, appointment_date,gender,pregnancy_status,days,prior_visit,points,date,problem,risk_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
    
    # Safely convert age to integer with comprehensive error handling
    try:
        age = int(user_data[chat_id]['age'])
    except (ValueError, KeyError) as err:
        print(f"Age conversion error: {err}, value was: {user_data[chat_id].get('age', 'missing')}")
        age = 0 
        bot.send_message(chat_id, "⚠️ Warning: Age value was invalid, using 0 as default.")
    except Exception as e:
        print(f"Unexpected error processing age: {e}")
        age = 0
        bot.send_message(chat_id, "⚠️ Warning: Could not process age value, using 0 as default.")
    
    # Safely convert weight to float with comprehensive error handling
    try:
        weight = float(user_data[chat_id]['weight'])
    except (ValueError, KeyError) as err:
        print(f"Weight conversion error: {err}, value was: {user_data[chat_id].get('weight', 'missing')}")
        weight = 0.0
        bot.send_message(chat_id, "⚠️ Warning: Weight value was invalid, using 0.0 as default.")
    except Exception as e:
        print(f"Unexpected error processing weight: {e}")
        weight = 0.0
        bot.send_message(chat_id, "⚠️ Warning: Could not process weight value, using 0.0 as default.")
    
    # Safely convert days to integer with comprehensive error handling
    try:
        days = int(user_data[chat_id].get('days', 0))
    except ValueError as err:
        print(f"Days conversion error: {err}, value was: {user_data[chat_id].get('days', 'missing')}")
        days = 0
        bot.send_message(chat_id, "⚠️ Warning: Days value was invalid, using 0 as default.")
    except Exception as e:
        print(f"Unexpected error processing days: {e}")
        days = 0
        bot.send_message(chat_id, "⚠️ Warning: Could not process days value, using 0 as default.")

    # Prepare values for database insertion with defaults for all fields
    try:
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
            x,
            user_data[chat_id].get('problem', 'Unknown'),
            risk_level
        )
    except Exception as e:
        print(f"Error preparing database values: {e}")
        bot.send_message(chat_id, "⚠️ Error preparing your data for storage. Some information may be missing.")
        # Create a minimal values tuple with defaults
        values = ('Unknown', 'Unknown', 'Unknown', 0, 0.0, 'Unknown', '', 'N/A', 0, 'Unknown', 0, now, 'Unknown', 'Routine')
    
    # Execute database operation with comprehensive error handling
    try:
        if db is None or cursor is None:
            bot.send_message(chat_id, "❌ Database connection is not available. Your appointment information has been recorded but not saved to the database.")
        else:
            cursor.execute(query, values)
            db.commit()
            bot.send_message(chat_id, "✅ Your appointment has been successfully saved to our database.")
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

    
    # Prepare payload for API call with comprehensive error handling for missing keys
    try:
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
            'points': total_score,  # Use points instead of total_score to match the database field
            'problem': user_data[chat_id].get('problem', 'N/A'),  # Add problem field
            'risk_level': risk_level,  # Add risk_level field
            'date': now.strftime('%Y-%m-%d %H:%M:%S')  # Use date instead of x
        }
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Error preparing data for hospital system: {str(e)[:100]}...")
        print(f"Error preparing payload: {e}")
        payload = {}

    # Make API call with comprehensive error handling and retry mechanism
    if payload:
        max_retries = 2
        retry_count = 0
        while retry_count <= max_retries:
            try:
                # Set a timeout to prevent hanging if the server is unresponsive
                response = requests.post(
                    "http://127.0.0.1:5001/notify", 
                    json=payload,
                    timeout=5  # 5 second timeout
                )
                
                if response.status_code == 200:
                    bot.send_message(chat_id, "✅ Appointment saved and sent to hospital system.")
                    break  # Success, exit retry loop
                else:
                    # Only retry on server errors (5xx)
                    if 500 <= response.status_code < 600 and retry_count < max_retries:
                        retry_count += 1
                        print(f"API server error, retrying {retry_count}/{max_retries}")
                        continue
                    
                    bot.send_message(
                        chat_id, 
                        f"⚠️ Appointment saved, but hospital system returned error code: {response.status_code}\n" +
                        f"Response: {response.text[:100]}..."
                    )
                    print(f"API error: Status {response.status_code}, Response: {response.text}")
                    break  # Non-retryable error, exit loop
            except requests.exceptions.Timeout:
                if retry_count < max_retries:
                    retry_count += 1
                    print(f"API timeout, retrying {retry_count}/{max_retries}")
                    continue
                bot.send_message(chat_id, "⚠️ Appointment saved, but hospital system did not respond in time.")
                print("API timeout: Hospital system did not respond in time")
                break
            except requests.exceptions.ConnectionError:
                if retry_count < max_retries:
                    retry_count += 1
                    print(f"API connection error, retrying {retry_count}/{max_retries}")
                    continue
                bot.send_message(chat_id, "⚠️ Appointment saved, but could not connect to hospital system.")
                print("API connection error: Could not connect to hospital system")
                break
            except Exception as e:
                bot.send_message(chat_id, f"⚠️ Appointment saved, but failed to notify hospital system. Error: {str(e)[:100]}...")
                print(f"API error: {e}")
                break
    else:
        bot.send_message(chat_id, "⚠️ Appointment saved, but could not prepare data for hospital system.")

    # Final confirmation message with appointment details
    try:
        confirmation_msg = f"📅 Appointment Summary:\n" + \
                          f"Name: {user_data[chat_id].get('name', 'Unknown')}\n" + \
                          f"Date: {user_data[chat_id].get('appointment_date', 'Unknown')}\n" + \
                          f"Priority: {risk_level}\n\n" + \
                          f"Thank you for using our appointment system. If you need to make changes, please contact the hospital directly."
        bot.send_message(chat_id, confirmation_msg)
    except Exception as e:
        print(f"Error sending confirmation: {e}")
        bot.send_message(chat_id, "Thank you for booking your appointment.")

bot.infinity_polling()
