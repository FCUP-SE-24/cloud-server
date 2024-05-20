from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

# Database Requests

@app.route('/get_bowls_list', methods=['GET'])
def get_bowls_list():
   #bowls = requests.get('http://raspberry_pi_ip/get_bowls_list').json()
   bowls = ['Bowl 1', 'Bowl 2', 'Bowl 3']
   return {'bowls':bowls}

@app.route('/get_daily_goal', methods=['GET'])
def get_daily_goal():
   data = request.args
   bowl_name = data.get('bowl_name')
   daily_goal = 100
   return {'daily_goal': daily_goal}

@app.route('/get_food_amount', methods=['GET'])
def get_food_amount():
   # current dosage saved in database
   data = request.args
   bowl_name = data.get('bowl_name')
   food_amount = 50
   return {'food_amount': food_amount}

@app.route('/get_last_feeding_time', methods=['GET'])
def get_last_feeding_time():
   data = request.args
   bowl_name = data.get('bowl_name')
   last_feeding_time = '12:00'
   return {'last_feeding_time': last_feeding_time}

@app.route('/get_weight', methods=['GET'])
def get_weight():
    # weight in sensor
    data = request.args
    bowl_name = data.get('bowl_name')
    #weight = requests.get('http://raspberry_pi_ip/get_weight').json()
    return {'weight': 5}

@app.route('/set_daily_goal', methods=['POST'])
def set_daily_goal():
    bowl_name = request.form['bowl_name']
    daily_goal = request.form['daily_goal']
    return {'message': f'Daily goal of {bowl_name} was successfully changed to {daily_goal}'}

@app.route('/set_feeding_time', methods=['POST'])
def set_feeding_time():
   feeding_time = request.form['feeding_time']
   bowl_name = request.form['bowl_name']
   return {'message': f'Last feeding time set to {feeding_time}'}

@app.route('/add_bowl', methods=['POST'])
def add_bowl():
   new_bowl = request.form['bowl_name']
   daily_goal = request.form['daily_goal']
   return {'message': f'Bowl {new_bowl} added successfully with daily goal of {daily_goal}'}

# ----------

# Other types of requests

@app.route('/control_motor', methods=['POST'])
def control_motor():
    return {'message':'on' if request.form['activate_motor']== 'on' else 'off'}

@app.route('/reset_bowl', methods=['POST'])
def reset_bowl():
   bowl_name = request.form['bowl_name']
   return {'message': f'Bowl {bowl_name}\'s weight has been updated'}

# ----------


#@app.route('/send_weight', methods=['POST'])
#def receive_weight():
#    if request.method == 'POST':
#        data = request.get_json()
#        print("data received\n")
#        return jsonify({"message": "Data received and processed successfully!"})
#    return jsonify({"error": "Invalid data"}), 400


#@app.route('/change_motor_state', methods=['POST'])
#def change_motor_state():
#    if request.method == 'POST':
#        activate_motor = request.json.get('activate_motor')
#        raspberry_pi_url = 'http://google.com'
#        data = {'activate_motor': activate_motor}
#        try:
#            response = requests.put(raspberry_pi_url, json=data)
            #if response.status_code == 200:
            #    return jsonify({"message": "Mensagem enviada com sucesso"})
            #else:
            #    return jsonify({"error": f"Erro ao enviar mensagem: {response.content.decode('utf-8')}"}), 500
#        except requests.exceptions.RequestException as e:
#            return jsonify({"error": "Erro ao conectar ao Raspberry Pi"}), 500

#@app.route('/set_daily_goal', methods=['POST'])
#def set_daily_goal():
#    if request.method == 'POST':
#        daily_goal = request.json.get('daily_goal')
#        raspberry_pi_url = 'http://google.com'
#        data = {'daily_goal': daily_goal}
#        try:
#            response = requests.put(raspberry_pi_url, json=data)
            #if response.status_code == 200:
            #    return jsonify({"message": "Mensagem enviada com sucesso"})
            #else:
            #    return jsonify({"error": f"Erro ao enviar mensagem: {response.content.decode('utf->
#        except requests.exceptions.RequestException as e:
#            return jsonify({"error": "Erro ao conectar ao Raspberry Pi"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
