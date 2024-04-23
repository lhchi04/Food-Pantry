from flask import Flask, render_template, request, jsonify, redirect
import requests

app = Flask(__name__)

# Placeholder data for available items
available_items = [
    {"id": 1, "name": "Apple"},
    {"id": 2, "name": "Banana"},
    {"id": 3, "name": "Flour"},
    {"id": 4, "name": "Sugar"},
    {"id": 5, "name": "Milk"}
]

# Placeholder data for selected items
selected_items = []

@app.route('/')
def index():
    return render_template('pantry.html', items=available_items)

@app.route('/select-items', methods=['POST'])
def select_items():
    if request.method == 'POST':
        selected_ids = request.form.getlist('item')
        for item_id in selected_ids:
            item = next((item for item in available_items if item['id'] == int(item_id)), None)
            if item and item not in selected_items:
                selected_items.append(item)
        return redirect('/')

@app.route('/fetch-recipes', methods=['GET'])
def fetch_recipes():
    items = [item['name'] for item in selected_items]
    ingredients_string = ',+'.join(selected_items)
    api_key = 'ffaeea8303ac4006bac35629dc34f9a7'
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_string}&number=2&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        recipes = response.json()
        return jsonify(recipes)
    else:
        return jsonify({'error': 'Failed to fetch recipes'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
