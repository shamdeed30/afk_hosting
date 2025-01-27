from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import bcrypt
import os
import subprocess
import json

#db setting needed: SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'afkuser'
app.config['MYSQL_PASSWORD'] = 'afk'
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

# Upload new match data (or update existing)
@app.route('/upload_match', methods=['POST'])
def upload_match():
    conn = get_db_connection()
    cursor = conn.cursor()

    data = request.json  # JSON data from frontend

    # Define game-specific insert queries
    game_queries = {
        "RL": """
            INSERT INTO RL_game (game_id, school, player_name, score, goals, assists, saves, shots, team_score, did_win, opponent, opponent_score, game_number, week_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE score = VALUES(score), goals = VALUES(goals), assists = VALUES(assists), saves = VALUES(saves), shots = VALUES(shots)
        """,
        "Val": """
            INSERT INTO Val_game (game_id, school, player_name, combat_score, kills, deaths, assists, econ, fb, plants, defuses, agent, map, team_score, did_win, opponent, opponent_score, game_num, week_num)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE combat_score = VALUES(combat_score), kills = VALUES(kills), deaths = VALUES(deaths), assists = VALUES(assists), econ = VALUES(econ), fb = VALUES(fb), plants = VALUES(plants), defuses = VALUES(defuses), agent = VALUES(agent), map = VALUES(map)
        """,
        "Apex": """
            INSERT INTO Apex_game (game_id, school, player_name, kills, assists, knocks, damage, score, placement, game_num, week_num)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE kills = VALUES(kills), assists = VALUES(assists), knocks = VALUES(knocks), damage = VALUES(damage), score = VALUES(score), placement = VALUES(placement)
        """,
    }

    try:
        game = data.get("game")
        if game not in game_queries:
            return jsonify({"error": f"Game '{game}' is not supported"}), 400

        # Insert or update data for each player
        for player in data["players"]:
            if game == "RL":
                cursor.execute(
                    game_queries[game],
                    (
                        data["game_id"], player["school"], player["playerName"],
                        player["score"], player["goals"], player["assists"],
                        player["saves"], player["shots"],
                        data.get("team_score"), data.get("did_win"),
                        data["opponent"], data.get("opponent_score"),
                        data.get("game_number"), data.get("week")
                    )
                )
            elif game == "Val":
                cursor.execute(
                    game_queries[game],
                    (
                        data["game_id"], player["school"], player["playerName"],
                        player["combat_score"], player["kills"], player["deaths"],
                        player["assists"], player["econ"], player["fb"],
                        player["plants"], player["defuses"], player["agent"], player["map"],
                        data.get("team_score"), data.get("did_win"),
                        data["opponent"], data.get("opponent_score"),
                        data.get("game_num"), data.get("week")
                    )
                )
            elif game == "Apex":
                cursor.execute(
                    game_queries[game],
                    (
                        data["game_id"], player["school"], player["playerName"],
                        player["kills"], player["assists"], player["knocks"],
                        player["damage"], player["score"], player["placement"],
                        data.get("game_num"), data.get("week")
                    )
                )

        conn.commit()
        return jsonify({"message": "Match data uploaded/updated successfully"}), 200
    except Exception as e:
        print(f"Error uploading match data: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Upload File and Process OCR Endpoint
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        ocr_script = os.path.join(os.path.dirname(__file__), "../ocr/Valorant/ValMatch/IconLoop.py")
        process = subprocess.run(
            ["python", ocr_script, file_path],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse the JSON output from IconLoop.py
        ocr_output = process.stdout.strip()
        ocr_data = json.loads(ocr_output)  # Safely parse JSON

        return jsonify(ocr_data)

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode OCR output"}), 500
    except subprocess.CalledProcessError as e:
        print(f"OCR script error: {e.stderr}")
        return jsonify({"error": "OCR processing failed"}), 500


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


