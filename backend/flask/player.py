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
        "RL": "SELECT * from RL_game WHERE player_name = %s",
        "Val": "SELECT * from Val_game WHERE player_name = %s",
        "Apex": "SELECT * from Apex_game WHERE player_name = %s",
        }
    
    try:
        cursor.execute(game_queries[game], (player,))

        stats = cursor.fetchall()

        
  
        return jsonify(stats), 200
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()