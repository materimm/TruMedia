from flask import Flask, render_template, redirect, url_for
import apis as a

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('select_player'))


@app.route('/select_player')
def select_player():
    players = a.get_all_players()
    return render_template('select_player.html', **locals())


@app.route('/player/<id>')
def player(id=None):
    if id is None:
        return redirect(url_for('select_player'))
    obj = a.get_player_games(id)
    return render_template('games.html', **locals())


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
