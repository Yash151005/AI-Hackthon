from flask import Blueprint, request, jsonify
from models import db, Chat
from flask_login import login_required, current_user

chatbot = Blueprint('chatbot', __name__)

def generate_response(prompt):
    """ Simple Cyber Law Chatbot Logic (Replace with AI model) """
    responses = {
        "What is cybercrime?": "Cybercrime refers to illegal activities conducted online, such as hacking and fraud.",
        "What is phishing?": "Phishing is a cyber-attack where criminals trick users into revealing sensitive information.",
        "What are cyber laws?": "Cyber laws govern digital activities and protect users from cyber threats."
    }
    return responses.get(prompt, "Sorry, I don't have an answer to that.")

@chatbot.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    prompt = data['prompt']
    response = generate_response(prompt)

    chat_entry = Chat(user_id=current_user.id, prompt=prompt, response=response)
    db.session.add(chat_entry)
    db.session.commit()

    return jsonify({"prompt": prompt, "response": response})

@chatbot.route('/history', methods=['GET'])
@login_required
def chat_history():
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    history = [{"prompt": c.prompt, "response": c.response} for c in chats]
    return jsonify(history)
