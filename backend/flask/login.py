from flask import Blueprint, jsonify, request
import pymysql
from db import get_db_connection
import bcrypt

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
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

