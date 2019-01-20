#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask, jsonify, render_template, request, Response
from flask_cors import CORS, cross_origin
import game_model

app = Flask(__name__)
CORS(app)

@app.route('/main')
@cross_origin()
def hello(name=None):
    return render_template('CAH.html', name=name)

@app.route('/start')
@cross_origin()
def start(name=None):
    return render_template('start.html', name=name)

@app.route('/js/<path:filename>')
@cross_origin()
def serve_static(filename):
    return send_from_directory(os.path.join('.', 'static', 'js'), filename)

@app.route('/geta-question')
@cross_origin()
def get_question():
    game = game_model.GameState()
    q = game.pop_q()
    current_question = q
    return jsonify(question=current_question)

@app.route('/play/<question>')
@cross_origin()
def start_game(question):
    return_string = "error"

    game = game_model.GameState()
    game.set_question(" ".join(question.split("|")))

    possible_answers = "|".join(game.human_players[0].player.card_strings)
    ai_answer = game.choose_ai_answer()
    # print(possible_answers)

    return jsonify(answers=possible_answers, ai_answer=ai_answer)

@app.route('/analyse/<arg_string>')
@cross_origin()
def analyse(arg_string):
    return_string = "error"
    human_phrase = arg_string.split("+")[0]
    ai_phrase = arg_string.split("+")[1]

    amazon_human_sentiment = game_model.amazon_sentiment_score(" ".join(human_phrase.split("|")))
    azure_human_sentiment = game_model.azure_sentiment_score(" ".join(human_phrase.split("|")))

    amazon_ai_sentiment = game_model.amazon_sentiment_score(" ".join(ai_phrase.split("|")))
    azure_ai_sentiment = game_model.azure_sentiment_score(" ".join(ai_phrase.split("|")))
    #google_ai_sentiment = game_model.google_sentiment_score(" ".join(arg_string.split("|")))

    return jsonify(amazon_human_score=amazon_human_sentiment, azure_human_score=azure_human_sentiment,
                   amazon_ai_score=amazon_ai_sentiment, azure_ai_score=azure_ai_sentiment)
