from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load models and predictions for each vegetable
models = {}
predictions = {}
for vegetable in ['beans', 'beetroot', 'bhindi', 'tomato']:
    with open(f'{vegetable}.pkl', 'rb') as file:
        data = pickle.load(file)
        models[vegetable] = data['model']
        predictions[vegetable] = data['future_df']  # Assuming future_df contains the predictions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    selected_vegetable = request.form.get('vegetables')
    
    # Check if the selected vegetable has a model and predictions
    if selected_vegetable in models:
        df_html = predictions[selected_vegetable].to_html(classes='table table-striped', index=False)
        return render_template('index.html', df_html=df_html, selected_vegetable=selected_vegetable)
    
    # Handle case where no valid vegetable is selected
    return render_template('index.html', df_html=None, selected_vegetable=selected_vegetable)

if __name__ == '__main__':
    app.run(debug=True)