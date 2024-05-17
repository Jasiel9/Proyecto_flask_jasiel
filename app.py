from flask import Flask, jsonify, request

import mariadb
import sys

#imporst db access config
from config import DATABASE_CONFIG

app = Flask(__name__)

try:
        conn = mariadb.connect(**DATABASE_CONFIG)
except mariadb.Error as e:
        print(f"Error  on connection: {e}")
        sys.exit(1)

cursor = conn.cursor()
#En este api se escoge todos los usuarios para mostrarlos en pantalla
@app.route('/api/get_users', methods=['GET'])
def get_users():
    try:
#conexion a base de datos
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
#request en sql para mostrar todos los usuarios 
        cursor.execute("SELECT nombre, apellido, email FROM Usuarios")
        users = cursor.fetchall()
        return str(users)
#verificacion
    except mariadb.Error as e:
        print(f"Error al obtener usuarios: {e}")
        return 'Error al obtener usuarios', 500
    finally:
        cursor.close()
        conn.close()
#En este api se escoge una transaccion especifico con su ID
@app.route('/api/get_transaction/<int:id>', methods=['GET'])
def get_transaction(id):  # Agrega el id aquí para identificar la transaccion
#conexion a la base de datos y request enviado al cursor con formato SQL
    try:
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Gastos WHERE id_gasto = ?", (id,))
        transaction = cursor.fetchone()
#Verificar que sea exitoso
        if transaction:
            return jsonify(transaction), 200
        else:
            return 'Transacción no encontrada', 404
    except mariadb.Error as e:
        print(f"Error al obtener transacción: {e}")
        return 'Error al obtener transacción', 500
    finally:
        cursor.close()
        conn.close()
#api para ver todas las transacciones
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Gastos")
        transactions = cursor.fetchall()

        if transactions:
            return jsonify(transactions), 200
        else:
            return 'No se encontraron transacciones', 404
    except mariadb.Error as e:
        print(f"Error al obtener transacciones: {e}")
        return 'Error al obtener transacciones', 500
    finally:
        cursor.close()
        conn.close()

#En este api escoge todas las transacciones relacionadas con alimentacion para mostrarlas
@app.route('/api/get_transaction/alimentacion', methods=['GET'])
def get_alimentacion_transactions(): 
#conexion a base de datos
    try:
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
#request en sql para buscar las transacciones relacionadas con alimentacion
        cursor.execute("SELECT * FROM Gastos WHERE tipo_transaccion = 'Alimentacion'")
        transactions = cursor.fetchall()
        return jsonify(transactions), 200
#Verificar que sea exitoso
    except mariadb.Error as e:
        print(f"Error al obtener transacciones de alimentación: {e}")
        return 'Error al obtener transacciones de alimentación', 500
    finally:
        cursor.close()
        conn.close()
#En este api escoge todas las transacciones relacionadas con transportacion para mostrarlas
@app.route('/api/get_transaction/transportacion', methods=['GET'])
def get_transportacion_transactions(): 
    try:
#conexion a base de datos
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
#request en sql para buscar las transacciones relacionadas con transportacion
        cursor.execute("SELECT * FROM Gastos WHERE tipo_transaccion = 'Transportacion'")
        transactions = cursor.fetchall()
        return jsonify(transactions), 200
#Verificar que sea exitoso
    except mariadb.Error as e:
        print(f"Error al obtener transacciones de transportación: {e}")
        return 'Error al obtener transacciones de transportación', 500
    finally:
        cursor.close()
        conn.close()
#En este api escoge todas las transacciones relacionadas con entretenimineto para mostrarlas

@app.route('/api/get_transaction/entretenimiento', methods=['GET'])
def get_entretenimiento_transactions(): 
    try:
#conexion a base de datos

        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
#request en sql para buscar las transacciones relacionadas con entretenimiento

        cursor.execute("SELECT * FROM Gastos WHERE tipo_transaccion = 'Entretenimiento'")
        transactions = cursor.fetchall()
        return jsonify(transactions), 200
#Verificar que sea exitoso

    except mariadb.Error as e:
        print(f"Error al obtener transacciones de entretenimiento: {e}")
        return 'Error al obtener transacciones de entretenimiento', 500
    finally:
        cursor.close()
        conn.close()
#NEW USER Permite crear un nuevo usuario para agregarlo a la base de datos,guardando su nombre junto con toda la informacion perteneciente a dicho usuario 
@app.route('/api/new_user', methods=['POST'])
def new_user():
    try:
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        datos = request.json
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        email = datos.get('email')
        contrasena = datos.get('contrasena')
        
        
        query = "INSERT INTO Usuarios (nombre, apellido, email, contrasena, ) VALUES ( ?, ?, ?, ?)"
        cursor.execute(query, (nombre, apellido, email, contrasena))
        
        conn.commit()

        response = {"message": "Record inserted"}
        return jsonify(response), 200
    
    except mariadb.Error as e:
        print(f"Error: {e}")
        response = {"error": "Failed to insert record"}
        return jsonify(response), 500
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/new_transaction', methods=['POST'])
def new_transaction():
    try:
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        datos = request.json
        
        tipo_transaccion = datos.get('tipo_transaccion')
        descripcion = datos.get('descripcion')
        precio = datos.get('precio')
        fecha = datos.get('fecha')
        
        query = "INSERT INTO Gastos (tipo_transaccion, descripcion, precio, fecha) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (tipo_transaccion, descripcion, precio, fecha))
        
        conn.commit()

        response = {"message": "Transacción creada exitosamente."}
        return jsonify(response), 200
    
    except mariadb.Error as e:
        print(f"Error: {e}")
        response = {"error": "Error al insertar la transacción en la base de datos."}
        return jsonify(response), 500
    
    finally:
        cursor.close()
        conn.close()

    
#(OK) DELETE Transaction, este api borra una transaccion junto con toda su informacion
@app.route('/api/delete_transaction/<int:id>', methods=['GET'])
def delete_transaction(id):
    try:
        # Establece conexion con la base de datos
        conn = mariadb.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        # validar el id
        if id == 0:
            return jsonify({"error": "Invalid ID"}), 404

        # request en sql para borrar usuario
        cursor.execute("DELETE FROM Gastos WHERE id_gasto = ?", (id,))
        conn.commit()

        
        cursor.close()
        conn.close()
#verificar que la transaccion se borro
        return jsonify({"message": "Transaccion eliminada con exito."}), 200

    except mariadb.Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al eliminar transaccion"}), 500


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)


