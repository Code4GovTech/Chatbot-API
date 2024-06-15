from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load menu structure from JSON file
with open('menu_structure.json', 'r', encoding="utf-8") as file:
    menu_structure = json.load(file)

@app.route('/')
def home():
    return "Welcome to the Chatbot API! Use the /chatbot endpoint to interact with the bot."

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_choice = request.json.get('choice', '').strip()
    
    # Determine the current state based on the user choice
    if user_choice.lower() == 'back to main menu':
        current_state = 'menu'
    elif user_choice.lower() == 'menu':
        current_state = 'menu'
    elif user_choice in menu_structure:
        current_state = user_choice
    else:
        return jsonify({"error": "Invalid choice. Please type menu to get the faq."}), 400

    # Get the current state data
    state_data = menu_structure.get(current_state, [])
    
    # Prepare the response based on the type of state data
    if isinstance(state_data, list):
        response = {
            "question": f"Please choose an option from {current_state}",
            "options": state_data
        }
    else:
        response = {
            "answer": state_data,
            "options": ["Back to Main Menu"]
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
