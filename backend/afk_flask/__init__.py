from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import bcrypt

# ssh -i ~/.ssh/AFK-VM_key.pem jcandrews2@52.233.73.156
app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = '40.85.147.30'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'SCAC_STATS'

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

    # Define game-specific queries and columns
    game_queries = {
        "RL": {
            "match_query": """
                SELECT game_id, school, opponent, did_win, team_score, opponent_score 
                FROM RL_game 
                WHERE week_number = %s 
                GROUP BY game_id 
                ORDER BY game_number
            """,
            "player_query": """
                SELECT school, player_name, score, goals, assists, saves, shots 
                FROM RL_game 
                WHERE game_id = %s
            """
        },
        "Val": {
            "match_query": """
                SELECT game_id, school, opponent, did_win, team_score, opponent_score 
                FROM Val_game 
                WHERE week_number = %s 
                GROUP BY game_id 
                ORDER BY game_number
            """,
            "player_query": """
                SELECT school, player_name, combat_score, kills, deaths, assists, econ, fb, plants, defuses 
                FROM Val_game 
                WHERE game_id = %s
            """
        },
        "Apex": {
            "match_query": """
                SELECT game_id, school, opponent, placement AS team_placement 
                FROM Apex_game 
                WHERE week_number = %s 
                GROUP BY game_id 
                ORDER BY game_number
            """,
            "player_query": """
                SELECT school, player_name, kills, assists, knocks, damage, score 
                FROM Apex_game 
                WHERE game_id = %s
            """
        }
    }

    try:
        # Check if the game is supported
        if game not in game_queries:
            return jsonify({"error": f"Game '{game}' is not supported"}), 400

        # Fetch all matches for the given week
        cursor.execute(game_queries[game]["match_query"], (week,))
        matches = cursor.fetchall()

        if not matches:
            return jsonify({"error": "No matches found for this week"}), 404

        # Prepare the response structure
        response = []

        for match in matches:
            game_id = match['game_id']

            # Fetch player stats for the match
            cursor.execute(game_queries[game]["player_query"], (game_id,))
            player_stats = cursor.fetchall()

            # Separate stats into teamStats and opponentStats
            team_stats = [player for player in player_stats if player['school'] == match['school']]
            opponent_stats = [player for player in player_stats if player['school'] == match['opponent']]

            # Add match and stats to the response
            match_data = {
                "match": {
                    "school": match.get('school'),
                    "opponent": match.get('opponent'),
                    "didWin": bool(match.get('did_win')),
                    "teamScore": match.get('team_score'),
                    "opponentScore": match.get('opponent_score')
                },
                "teamStats": team_stats,
                "opponentStats": opponent_stats
            }

            # Apex has placement instead of scores
            if game == "apex-legends":
                match_data["match"]["placement"] = match.get("team_placement")

            response.append(match_data)

        return jsonify(response)
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    data = request.get_json()  # Parse the JSON body of the request
    username = data.get('username')
    password = data.get('password')

    try: 
        # get row that matches username
        cursor.execute( 
            "SELECT * from Admins WHERE username = %s", (username,)
        )

        user = cursor.fetchone()

        # DONT DELETE: It's for hashing passwords to store in the db for admin accounts
        # print(bcrypt.hashpw('jca2CC66.'.encode('utf-8'), bcrypt.gensalt()))

        if user: 
            # hash the password given by user and compare
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')): 
                return jsonify({"message": "Success"}, 200)
            else: 
                return jsonify({"error": "Invalid credentials"}), 401
        else: 
            return jsonify({"error": "Username not found."}), 404

    except Exception as e: 
        print(e)
        return jsonify({"error": str(e)}), 500
    
    finally: 
        cursor.close()
        conn.close()

if __name__ == "__main__": 
    app.run(host='0.0.0.0',port=8080, debug=True)

