import sys
sys.path.append('backend/')
import json
from battle import Battle
from trainer import TrainerAI, makeTeam
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://localhost:3000"}})


def sendToLog(battle):
    return battle.getBattleLog()

@app.route("/run", methods=["POST", "OPTIONS"])
@cross_origin(origin='*')
def simulate():
    print(request.get_json(force=True))
    pokemon = request.form['no']
    trainer_teams = {v['trainer']:v for v in pokemon}
    for trainer in trainer_teams:
        pass #TODO
    return
def run_battle(battle):
    """ Runs a battle simulation. """

    scores = []

    while battle.over == False:
        battle.nextRound()
        sendToLog(battle)

    for p in battle.players:
        print(p.name + " scored " + str(p.score) + " point(s)!")
        scores.append([p.name, p.score])


# Simulate(Sample_Battle)
