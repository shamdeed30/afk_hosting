from flask import Blueprint, jsonify, request
import pymysql
from db import get_db_connection
import os
import subprocess
import json

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    school = request.form.get('school')
    opponent_school = request.form.get('opponent_school')
    week = request.form.get('week')
    game = request.form.get('game')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    UPLOAD_FOLDER = 'uploads/'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Define the OCR script path
        ocr_script = os.path.join(os.path.dirname(__file__), "../ocr/Valorant/ValMatch/ValOCR.py")

        # Run the OCR script
        subprocess.run(
            ["python", ocr_script, "-f", file_path],
            check=True
        )

        # Construct the JSON file path based on your directory structure
        json_file_path = f'JSON/players_uploads/{file.filename.replace(".png","")}.json'


        # Load the JSON data from the file
        with open(json_file_path, 'r') as json_file:
            ocr_data = json.load(json_file)

        # Format the output to include all required attributes
        formatted_data = {
            "game": game,  # Assuming the game is Valorant for this OCR
            "week": week,  # Week will need to be added manually in the ModifyPage
            "school": school,  # School will need to be added manually in the ModifyPage
            "opponent_school": opponent_school,  # Opponent will need to be added manually in the ModifyPage
            "map": ocr_data.get("map", ""),
            "players": ocr_data.get("players", []),
        }
        print(formatted_data)

        return jsonify(formatted_data)

    except FileNotFoundError:
        return jsonify({"error": "OCR output file not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode OCR output"}), 500
    except subprocess.CalledProcessError as e:
        print(f"OCR script error: {e.stderr}")
        return jsonify({"error": "OCR processing failed"}), 500


# Upload new match data (or update existing)
@upload_bp.route('/upload_match', methods=['POST'])
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
