from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Settings
SPOONACULAR_API_KEY = 'ffaeea8303ac4006bac35629dc34f9a7'
SPOONACULAR_BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=" + SPOONACULAR_API_KEY

@app.route('/recipe', methods=['POST'])
def home():
    data = request.get_json()
    ingredients = ','.join(data.get('ingredients', []))  # Ensure 'ingredients' is a list of strings

    # Fetch recipes from Spoonacular using the ingredients
    try:
        recipes_response = requests.get(f"{SPOONACULAR_BASE_URL}&ingredients={ingredients}&number=8")
        if recipes_response.status_code == 200:
            return jsonify(recipes_response.json())
        else:
            return jsonify({'error': 'Failed to retrieve recipes'}), recipes_response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5004, debug=True)
