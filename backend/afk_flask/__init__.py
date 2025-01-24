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
        # Fetch all matches for the given week
        query = f"""
        SELECT game_id, school, opponent, did_win, team_score, opponent_score 
        FROM {game}_game 
        WHERE week_number = %s 
        GROUP BY game_id 
        ORDER BY game_number
        """
        cursor.execute(query, (week,))
        matches = cursor.fetchall()

        if not matches:
            return jsonify({"error": "No matches found for this week"}), 404

        # Prepare the response structure
        response = []

        for match in matches:
            game_id = match['game_id']

            # Fetch player stats for the match
            cursor.execute(
                f"""
                SELECT school, player_name, score, goals, assists, saves, shots 
                FROM {game}_game 
                WHERE game_id = %s
                """,
                (game_id,)
            )
            player_stats = cursor.fetchall()

            # Separate stats into teamStats and opponentStats
            team_stats = [player for player in player_stats if player['school'] == match['school']]
            opponent_stats = [player for player in player_stats if player['school'] == match['opponent']]

            # Add match and stats to the response
            response.append({
                "match": {
                    "school": match['school'],
                    "opponent": match['opponent'],
                    "didWin": bool(match['did_win']),
                    "teamScore": match['team_score'],
                    "opponentScore": match['opponent_score']
                },
                "teamStats": team_stats,
                "opponentStats": opponent_stats
            })

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__": 
    app.run(port=8080, debug=True)

