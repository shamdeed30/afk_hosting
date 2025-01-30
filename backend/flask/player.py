from flask import Blueprint, jsonify, request
import pymysql
from urllib.parse import unquote
from db import get_db_connection

player_bp = Blueprint('player', __name__)

@player_bp.route('/player/<game>', methods=['GET'])
def get_player_stats(game):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    data = request.args.get('player')
    player = unquote(data)

    game_queries = { 
        "RL": "SELECT school, player_name, score, goals, assists, saves, shots from RL_game WHERE player_name = %s",
        "Val": "SELECT school, player_name, combat_score, kills, deaths, assists, econ, fb, plants, defuses from Val_game WHERE player_name = %s",
        "Apex": "SELECT school, player_name, kills, assists, knocks, damage, score from Apex_game WHERE player_name = %s",
        }
    
    try:
        cursor.execute(game_queries[game], (player,))

        reports = cursor.fetchall()

        if not reports:
            return jsonify({"error": "No stats found for player."}), 404
  
        return jsonify(reports), 200
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()