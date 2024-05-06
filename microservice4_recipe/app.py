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
        recipes_response = requests.get(f"{SPOONACULAR_BASE_URL}&ingredients={ingredients}&number=5")
        if recipes_response.status_code == 200:
            return jsonify(recipes_response.json())
        else:
            return jsonify({'error': 'Failed to retrieve recipes'}), recipes_response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    # # Fetch the cart contents from the Pantry Microservice
    # cart_response = requests.get(PANTRY_SERVICE_URL)
    # if cart_response.status_code != 200:
    #     # Return a simple JSON error instead of rendering an error page
    #     return jsonify({'error': 'Failed to fetch cart data'}), 502

    # cart_items = cart_response.json()
    # ingredients = ','.join(cart_items.keys())

    # # Fetch recipes from Spoonacular
    # recipes_response = requests.get(f"{SPOONACULAR_BASE_URL}&ingredients={ingredients}&number=5")
    # if recipes_response.status_code != 200:
    #     # Return a simple JSON error instead of rendering an error page
    #     return jsonify({'error': 'Failed to retrieve recipes'}), 503

    # recipes = recipes_response.json()
    # return render_template('recipe.html', recipes=recipes)

if __name__ == '__main__':
    app.run(port=5004, debug=True)
