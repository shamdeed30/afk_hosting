from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import bcrypt

# ssh -i ~/.ssh/AFK-VM_key.pem jcandrews2@52.233.73.156
app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'AFK'

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
    app.run(port=8080, debug=True)

