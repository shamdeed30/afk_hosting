from flask import Flask, request, jsonify
import mysql.connector

# ssh -i ~/.ssh/AFK-VM_key.pem jcandrews2@52.233.73.156
app = Flask(__name__)

# create db connection
def get_db():
    db = mysql.connector.connect(
            host='localhost',
            user='jcandrews2',
            password='jca2CC66.',
            database='AFK'
    )
    return db

@app.route('/stats/<game>/<week>')
def get_weekly_game_stats(game, week):
    db = get_db()
    cursor = db.cursor()
    match_stats = handle_get_match_stats(db, cursor, game, week)
    print(match_stats)

    return jsonify({
        "message": game, 
        "week": week
    })

def handle_get_match_stats(db, cursor, game, week): 
    sql_cmd = "SELECT school, opponent, didWin, team_score, opponent_score FROM ?_game WHERE week_num = ? GROUP BY game_id", (game, week)

    return cursor.execute(sql_cmd).fetchall()

if __name__ == "__main__": 
    app.run(port=8080, debug=True)
