from flask import Flask , request , jsonify
import json
import pymysql


app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = pymysql.connect(host="localhost",
    			       	user="alfred",
                               	password="Ka075.",
                               	database="autoflaskapi",
                               	charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    except pymysql.error as e :
        print(e)
    return conn


# @app.route('/Auto' , methods=['GET' , 'POST'])
# def all_auto():
#     conn = db_connection()
#     cursor = conn.cursor()
#     if request.method == 'GET':
#         cursor.execute("SELECT * FROM autos")
#         allAuto = [
#             dict(id_auto =row['id_auto'],id_parking=row['id_parking'] ,
#                  matricule = row['matricule'])
#                  for row in cursor.fetchall()
#         ]
#         if allAuto is not None :
#             return jsonify(allAuto)

    
#     if request.method == 'POST':
#         new_id_parking = int(request.form["id_parking"])
#         new_matricule = request.form["matricule"]
#         sql = """ INSERT INTO autos (id_parking , matricule)
#                     VALUES(%s,%s)"""

#         cursor = cursor.execute(sql,(new_id_parking, new_matricule))
#         conn.commit()
#         return "created successfully",201


from flask import request, jsonify

@app.route('/Auto', methods=['GET', 'POST'])
def all_auto():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM autos")
        allAuto = [
            dict(id_auto=row['id_auto'], id_parking=row['id_parking'], matricule=row['matricule'])
            for row in cursor.fetchall()
        ]
        return jsonify(allAuto)

    if request.method == 'POST':
        data = request.json  # Get JSON data from the request
        new_id_parking = data.get("id_parking")
        new_matricule = data.get("matricule")
        
        # Check for missing fields
        if new_id_parking is None or new_matricule is None:
            return jsonify({"error": "Missing id_parking or matricule"}), 400  # Bad Request

        # Insert into database
        sql = """INSERT INTO autos (id_parking, matricule) VALUES (%s, %s)"""
        cursor.execute(sql, (new_id_parking, new_matricule))
        conn.commit()
        
        return jsonify({"message": "Created successfully"}), 201

@app.route('/Auto/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_auto(id):
    conn = db_connection()
    cursor = conn.cursor()

    # First, check if the ID exists
    cursor.execute("SELECT * FROM autos WHERE id_auto=%s", (id,))
    auto = cursor.fetchone()  # Check if record exists

    if not auto:
        return jsonify({"error": "Auto with id {} does not exist.".format(id)}), 404  # Not Found

    if request.method == "GET":
        return jsonify(auto), 200

    if request.method == 'PUT':
        sql = """UPDATE autos SET id_parking=%s,
                                   matricule=%s
                WHERE id_auto=%s"""  # Removed the extra comma
        
        # Get the JSON data
        data = request.json  # Use request.json for JSON input
        id_parking = data.get('id_parking')
        matricule = data.get('matricule')
        
        # Check if the necessary data is provided
        if id_parking is None or matricule is None:
            return jsonify({"error": "Missing id_parking or matricule"}), 400  # Bad Request

        updated_auto = {
            "id_auto": id,
            "id_parking": id_parking,
            "matricule": matricule,  # Fixed the key from "marticule" to "matricule"
        }

        cursor.execute(sql, (id_parking, matricule, id))
        conn.commit()

        return jsonify(updated_auto), 200  # Return 200 OK

    if request.method == 'DELETE':
        sql = """DELETE FROM autos WHERE id_auto=%s"""
        cursor.execute(sql, (id,))
        conn.commit()
        return "The auto with id:{} has been deleted.".format(id), 200




if __name__ == '__main__' :
    app.run(debug=True)