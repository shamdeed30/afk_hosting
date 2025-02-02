from flask import Blueprint, jsonify, request
import pymysql
from urllib.parse import unquote
from db import get_db_connection

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats/<videogame>', methods=['GET'])
def get_game_stats(videogame):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    data = request.args.get('week')
    week = unquote(data)

    # Queries for getting matchup list
    matchup_queries = { 
        # "rl": "SELECT DISTINCT school, opponent FROM rl_picture WHERE week_number = %s;",
        # "val": "SELECT DISTINCT school, opponent FROM val_picture WHERE week_number = %s;",
        "apex": "SELECT DISTINCT school FROM apex_week WHERE week_number = %s;"
    }

    # Queries for getting overall match scores

    # Game queries
    game_queries = {
        "rl": {
            "game_query": """
                SELECT game_id, game_number, w_school, l_school, w_points, l_points
                FROM rl_picture
                WHERE week_number = %s AND school = %s
                GROUP BY game_id
                ORDER BY game_number;
            """,
            "player_query": """
                SELECT school, player_name, score, goals, assists, saves, shots
                FROM rl_game
                WHERE game_id = %s;
            """
        },
        "val": {
            "game_query": """
                SELECT game_id, game_number, w_school, l_school, w_points, l_points
                FROM val_game
                WHERE week_number = %s AND school = %s
                ORDER BY game_number;
            """,
            "player_query": """
                SELECT school, player_name, combat_score, kills, deaths, assists, econ, fb, plants, defuses, score
                FROM val_game
                WHERE game_id = %s AND school = %s;
            """
        },
        "apex": {
            "game_query": """
                SELECT school, game_number, game_id
                FROM apex_picture
                WHERE week_number = %s AND school = %s
                GROUP BY game_id
                ORDER BY game_number;
            """,
            "player_query": """
                SELECT school, player_name, kills, assists, knocks, damage, score 
                FROM apex_game
                WHERE game_id = %s AND school = %s;
            """
        }
    }

    try:
        if videogame not in game_queries:
            return jsonify({"error": f"Game '{videogame}' is not supported"}), 400

        # Get the matchups
        cursor.execute(matchup_queries[videogame], (week,))
        matchups = cursor.fetchall()
        
        response = []

        for matchup in matchups:

            if videogame == "apex": 

                # Get the school
                school = matchup['school']

                match_data = { 
                    "match" : { 
                        "school": school,
                        "games": []
                    }
                }
                
                cursor.execute(game_queries[videogame]["game_query"], (week, school))
                games = cursor.fetchall()

                for game in games: 

                    cursor.execute(game_queries[videogame]["player_query"], (game['game_id'], school))
                    player_stats = cursor.fetchall()

                    total_points = 0
                    team_stats = []

                    for player in player_stats: 
                        if player['placement'] == 1: 
                            total_points += 12
                        elif player['placement'] == 2: 
                            total_points += 9
                        elif player['placement'] == 3: 
                            total_points += 7
                        elif player['placement'] == 4:
                            total_points += 5 
                        elif player['placement'] == 5: 
                            total_points += 4
                        elif player['placement'] <= 7: 
                            total_points += 3
                        elif player['placement'] <= 10: 
                            total_points += 2
                        elif player['placement'] <= 15: 
                            total_points += 1

                        total_points += player['kills']
                        total_points += player['damage'] % 200
                        
                        team_stats.append(player)

                    game_data = {
                        "game": {
                            "school": school,
                            "points": total_points,
                            "gameNumber": game["game_number"]
                        },
                        "teamStats": team_stats,
                    }

                    match_data["match"]['games'].append(game_data)

            else: 
                pass
                # # Get the matchup
                # school, opponent = matchup['school'], matchup['opponent']

                # cursor.execute(match_score_queries[videogame], (school, opponent))
                # match_scores = cursor.fetchall()

                # print(match_scores)

                # # Format the match data
                # match_data = { 
                #     "match" : { 
                #         "school": school,
                #         "opponent": opponent,
                #         "schoolScore": match_scores[0]['wins'],
                #         "opponentScore": match_scores[1]['wins'],
                #         "games": []
                #     }
                # }
                
                # # Get the match's games
                # cursor.execute(game_queries[videogame]["game_query"], (week, school))
                # games = cursor.fetchall()

                

                # # Go thru the games and get player data
                # for game in games: 

                #     # Get the player stats
                #     cursor.execute(game_queries[videogame]["player_query"], (game['game_id'],))
                #     player_stats = cursor.fetchall()

                #     team_stats = [player for player in player_stats if player['school'] == school]
                #     opponent_stats = [player for player in player_stats if player['school'] == opponent]

                #     game_data = {
                #         "game": {
                #             "school": school,
                #             "opponent": opponent,
                #             "teamScore": team_stats[0]['score'],
                #             "opponentScore": opponent_stats[0]['score'],
                #             "gameNumber": game["game_number"]
                #         },
                #         "teamStats": team_stats,
                #         "opponentStats": opponent_stats
                #     }

                #     match_data["match"]['games'].append(game_data)

            response.append(match_data)

        return jsonify(response)
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()
