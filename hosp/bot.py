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


db = mysql.connector.connect(**mysql_config)
cursor = db.cursor()

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
        msg = bot.send_message(message.chat.id, "That doesn’t seem like a valid name. Please enter your full name (letters only).")
        bot.register_next_step_handler(msg, process_name)
        return

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
    user_data[message.chat.id].update({'age': message.text})
    bot.send_message(message.chat.id,f"Your noted age is: {message.text}")
    msg= bot.send_message(message.chat.id, f"Enter your wieght")
    bot.register_next_step_handler(msg, process_weight)

def process_weight(message):
    user_data[message.chat.id].update({'weight': message.text})
    bot.send_message(message.chat.id,f"Yours weight is: {message.text}")
    msg= bot.send_message(message.chat.id, f"What problem are you facing")
    bot.register_next_step_handler(msg, process_treatment)

def process_treatment(message):
    user_data[message.chat.id].update({'problem': message.text})
    msg = bot.send_message(message.chat.id, "Do you have fever, fatigue, nausea, dizziness, or any other symptoms?")
    bot.register_next_step_handler(msg, process_other_symptoms)

def process_other_symptoms(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response or 'fever' in response or 'nausea' in response or 'weakness' in response or 'dizziness' in response:
        score = 30
    elif 'no' in response or 'nope' in response:
        score = 10
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Do you have any known allergies?")
    bot.register_next_step_handler(msg, process_allergies)

def process_allergies(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 20
    elif 'no' in response or 'nope' in response:
        score = 10
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Is the pain mild, moderate, or severe?")
    bot.register_next_step_handler(msg, process_pain_level)

def process_pain_level(message):    
    response = message.text.lower().strip()
    score = 0
    
    if 'sever' in response:
        score = 40
    elif 'moderate' in response:
        score = 20
    elif 'mild' in response:
        score = 10

    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "How did the symptoms start—suddenly or gradually?")
    bot.register_next_step_handler(msg, process_symptom_onset)

def process_symptom_onset(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'suddenly' in response:
        score = 30
    elif 'gradually' in response:
        score = 20
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Have you tried any treatments before coming here?")
    bot.register_next_step_handler(msg, process_previous_treatments)

def process_previous_treatments(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 15
    elif 'no' in response or 'nope' in response:
        score = 30
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    
    msg = bot.send_message(message.chat.id, "Have you noticed weight loss or gain?")
    bot.register_next_step_handler(msg, process_weight_changes)

def process_weight_changes(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 40
    elif 'no' in response or 'nope' in response:
        score = 20
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Have you had similar problems in the past?")
    bot.register_next_step_handler(msg, process_past_problems)

def process_past_problems(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 30
    elif 'no' in response or 'nope' in response:
        score = 25
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Do you have any chronic conditions like diabetes, high BP, asthma, etc.?")
    bot.register_next_step_handler(msg, process_chronic_conditions)

def process_chronic_conditions(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score =40
    elif 'no' in response or 'nope' in response:
        score = 20
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Have you undergone any surgeries?")
    bot.register_next_step_handler(msg, process_surgeries)

def process_surgeries(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 40
    elif 'no' in response or 'nope' in response:
        score = 20
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Is there a family history of heart disease, diabetes, cancer, or other conditions?")
    bot.register_next_step_handler(msg, process_family_history)

def process_family_history(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 30
    elif 'no' in response or 'nope' in response:
        score = 20
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Do you smoke or drink alcohol?")
    bot.register_next_step_handler(msg, process_smoking_drinking)

def process_smoking_drinking(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 40
    elif 'no' in response or 'nope' in response:
        score = 10
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Are you under stress or anxiety lately?")
    bot.register_next_step_handler(msg, process_stress_level)

def process_stress_level(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 25
    elif 'no' in response or 'nope' in response:
        score = 10
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Do you exercise regularly?")
    bot.register_next_step_handler(msg, process_gender)

def process_gender(message):
    response = message.text.lower().strip()
    score = 0

    if 'yes' in response or 'yess' in response:
        score = 10
    elif 'no' in response or 'nope' in response:
        score = 30

    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score

    msg = bot.send_message(message.chat.id, "Are you male or female?")
    bot.register_next_step_handler(msg, process_gender_response)

    
def process_gender_response(message):
    gender = message.text.lower().strip()
    user_data[message.chat.id].update({'gender': gender})

    if gender in ['female', 'f', 'woman']:
        msg = bot.send_message(message.chat.id, "Are you currently pregnant?")
        bot.register_next_step_handler(msg, process_pregnancy_status)
    else:
        msg = bot.send_message(message.chat.id, "From how many days are you facing this problem?")
        bot.register_next_step_handler(msg, ask_clinic_visit)

def process_pregnancy_status(message):
    user_data[message.chat.id].update({'gender': message.text.lower()})
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 40
    elif 'no' in response or 'nope' in response:
        score = 10
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    user_data[message.chat.id].update({'pregnancy_status': message.text})
    msg = bot.send_message(message.chat.id, "Are you currently using any contraception?")
    bot.register_next_step_handler(msg, process_contraception_use)

def process_contraception_use(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 15
    elif 'no' in response or 'nope' in response:
        score = 10
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Are you experiencing any menstrual irregularities?")
    bot.register_next_step_handler(msg, process_menstrual_issues)

def process_menstrual_issues(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 20
    elif 'no' in response or 'nope' in response:
        score = 10
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "Have you gone through menopause? (If applicable)")
    bot.register_next_step_handler(msg, process_menopause_status)

def process_menopause_status(message):
    response = message.text.lower().strip()
    score = 0
    
    if 'yes' in response or 'yess' in response:
        score = 15
    elif 'no' in response or 'nope' in response:
        score = 10
    
    current_score = user_data[message.chat.id].get('score', 0)
    user_data[message.chat.id]['score'] = current_score + score
    msg = bot.send_message(message.chat.id, "From How many days your facing this problem?")
    bot.register_next_step_handler(msg, ask_clinic_visit)

def ask_clinic_visit(message):
    days = message.text.strip()
    user_data[message.chat.id].update({'days': days})
    try:
        days = int(message.text.strip())
    except ValueError:
        msg = bot.send_message(message.chat.id, "Please enter the number of days as a numeric value.")
        bot.register_next_step_handler(msg, ask_clinic_visit)
        return

    user_data[message.chat.id].update({'days': days})
    
    if days > 2:
        user_data[message.chat.id]['score'] = user_data[message.chat.id].get('score', 0) + 30
    else:
        user_data[message.chat.id]['score'] = user_data[message.chat.id].get('score', 0)+ 10
    msg = bot.send_message(message.chat.id, "Did you visit our clinic prior?")
    bot.register_next_step_handler(msg, process_visit)


def process_visit(message):
    user_data[message.chat.id].update({'prior_visit': message.text})
    msg= bot.send_message(message.chat.id, f"on which date do you want appointment?")
    bot.register_next_step_handler(msg, process_date)

def process_date(message):
    chat_id = message.chat.id
    user_data[chat_id].update({'appointment_date': message.text})
    
    total_score = user_data[chat_id].get('score', 0)

    now = datetime.datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    bot.send_message(chat_id, f"Your requested appointment date: {message.text}")
    bot.send_message(chat_id, f"Your total priority score is: {total_score}**")

    if total_score >= 200:
        risk_level = "Emergency "
    elif total_score >= 100:
        risk_level = "Urgent "
    else:
        risk_level = "Routine"

    bot.send_message(chat_id, f"Risk Assessment: {risk_level}")


    user_data[chat_id]['points'] = total_score
    user_data[chat_id]['date'] = now 
    user_data[chat_id]['risk_level'] = risk_level
    user_data[chat_id]['x'] = now  # Ensure x is defined as the current datetime

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
        user_data[chat_id]['name'],
        user_data[chat_id]['contact'],
        user_data[chat_id]['address'],
        age,
        weight,
        user_data[chat_id]['appointment_date'],
        user_data[chat_id].get('gender', ''),
        user_data[chat_id].get('pregnancy_status', 'N/A'), 
        days,
        user_data[chat_id]['prior_visit'],
        total_score,
        x,
        user_data[chat_id]['problem'],
        risk_level
    )
    cursor.execute(query, values)
    db.commit()
    
    payload = {
        'name': user_data[chat_id]['name'],
        'contact': user_data[chat_id]['contact'],
        'address': user_data[chat_id]['address'],
        'age': user_data[chat_id]['age'],
        'weight': user_data[chat_id]['weight'],
        'appointment_date': user_data[chat_id]['appointment_date'],
        'gender': user_data[chat_id].get('gender', ''),
        'pregnancy_status': user_data[chat_id].get('pregnancy_status', 'N/A'),
        'days': user_data[chat_id].get('days', 0),
        'prior_visit': user_data[chat_id]['prior_visit'],
        'points': total_score,  # Use points instead of total_score to match the database field
        'problem': user_data[chat_id].get('problem', 'N/A'),  # Add problem field
        'risk_level': risk_level,  # Add risk_level field
        'date': now.strftime('%Y-%m-%d %H:%M:%S')  # Use date instead of x
    }

    try:
        response = requests.post("http://127.0.0.1:5001/notify", json=payload)  # Update port to 5001 to match Flask app
        if response.status_code == 200:
            bot.send_message(chat_id, "✅ Appointment saved and sent to hospital system.")
        else:
            bot.send_message(chat_id, "⚠️ Appointment saved, but website did not accept it.")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Appointment saved, but failed to notify website. Error: {e}")
    
    #if response.status_code == 200:
       # bot.send_message(chat_id, "Your data was also sent to the hospital system.")

bot.infinity_polling()
