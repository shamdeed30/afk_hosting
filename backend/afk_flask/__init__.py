from flask import Flask, jsonify
from flask_cors import CORS
import pymysql

# ssh -i ~/.ssh/AFK-VM_key.pem jcandrews2@52.233.73.156
app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'esports'

# Database connection
def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

@app.route('/stats/<game>/<week>', methods=['GET'])
def get_game_stats(game, week):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # Fetch match stats

        # TODO: I think we need to change this to select from the correct game table. 
        cursor.execute(
            "SELECT * FROM game_stats WHERE game=%s AND week=%s", (game, week)
        )
        match = cursor.fetchone()

        if not match:
            return jsonify({"error": "No data available"}), 404

        # Fetch player stats for the match
        cursor.execute(
            "SELECT * FROM player_stats WHERE game_id=%s", (match['id'],)
        )
        player_stats = cursor.fetchall()

        # Organize response data
        response = {
            "match": {
                "school": match['school'],
                "opponent": match['opponent'],
                "didWin": match['did_win'],
                "teamScore": match['team_score'],
                "opponentScore": match['opponent_score']
            },
            "teamStats": [player for player in player_stats if player['school'] == match['school']],
            "opponentStats": [player for player in player_stats if player['school'] == match['opponent']]
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__": 
    app.run(port=8080, debug=True)

