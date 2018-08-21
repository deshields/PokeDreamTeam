import sys
sys.path.append('backend/')

from battle import Battle, Sample_Battle
from trainer import TrainerAI
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
#
# def homepage():
#     return render_template("index.html")


@app.route("/run")
def Simulate(battle):
    """ Runs a battle simulation. """

    scores = []

    while battle.over == False:
        battle.nextRound()

    for p in battle.players:
        print(p.name + " scored " + str(p.score) + " point(s)!")
        scores.append([p.name, p.score])

Simulate(Sample_Battle)
