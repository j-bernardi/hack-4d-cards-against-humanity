import game_model
from flask import Flask, jsonify, render_template, request, Response
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app)

@app.route('/')
@cross_origin()
def hello_world():
    return Response("Welcome to the python prediction script. \n<br> \
        \n<br>\
        \n<br>Usage:\
        \n<br>Dependent variable prediction software using gaussian_processing to interpolate data from an input text document\
        \n<br>A script that takes an input dataset, learns that dataset, then provides a prediction depending on input query point\
        \n<br>\
        \n<br>argument input:\
            \n<br>/data.txt/dimensions\
            \n<br>(dimension input delimited by: '/', eg 'x1/x2/x3/x4 ... etc') \
        \n<br>The order of the dimensions provided on the command line must match the order in which they appear on the file input 'data.txt')\
        \n<br>\
        \n<br>Eg: requires file input as:\
        \n<br>(optional headers as strings) row 1: title1 title2 title3  .... dependent_variable_title\
        \n<br>('dependent_variable' header must appear last)\
        \n<br>\
        \n<br>row 2: value1 value2 value3 .... dependent_value - as values\
        \n<br>row 3: value1 value2 value3 .... dependent_value\
        \n<br>etc ..\
        ", mimetype="text/html")

@app.route('/play')
@cross_origin()
def start_game():
    game = main.GameState()
    return game.human_players[0].card_strings
