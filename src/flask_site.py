from flask import Flask, render_template, jsonify

from dynamic_manager import dynamic_value_manager


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', value=dynamic_value_manager.get_value())

@app.route('/update')
def update():
    return jsonify(value=dynamic_value_manager.get_value())

