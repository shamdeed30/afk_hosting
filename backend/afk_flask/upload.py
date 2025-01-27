from flask import Blueprint, jsonify, request
import pymysql
from db import get_db_connection

upload_bp = Blueprint('upload', __name__)


# Upload new match data (or update existing)
@upload_bp.route('/upload_match', methods=['POST'])
def upload_match():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

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
            if game == "rocket-league":
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
            elif game == "valorant":
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
            elif game == "apex-legends":
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

