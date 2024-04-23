from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

@app.route('/get_weight', methods=['GET'])
def get_weight():
    #weight = requests.get('http://raspberry_pi_ip/get_weight').json()
    return {'weight': 100}

#@app.route('/send_weight', methods=['POST'])
#def receive_weight():
#    if request.method == 'POST':
#        data = request.get_json()
#        print("data received\n")
#        return jsonify({"message": "Data received and processed successfully!"})
#    return jsonify({"error": "Invalid data"}), 400

@app.route('/control_motor', methods=['POST'])
def control_motor():
    data = request.json
    return {'message':'on' if data.get('activate_motor')== 'on' else 'off'}

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

@app.route('/set_daily_goal', methods=['POST'])
def set_daily_goal():
    data = request.json
    #response = requests.post('http://raspberry_pi_ip/set_daily_goal', json=data)
    #return response.json()
    return {'message': f'Daily goal set to {data.get("daily_goal")}'}

@app.route('/get_bowls_list', methods=['GET'])
def get_bowls_list():
   #bowls = requests.get('http://raspberry_pi_ip/get_bowls_list').json()
   bowls = ['Bowl 1', 'Bowl 2', 'Bowl 3']
   return {'bowls':bowls}

@app.route('/add_bowl', methods=['POST'])
def add_bowl():
   data = request.json
   new_bowl = data.get('bowl_name')
   return {'message': f'Cup {new_bowl} added successfully'}

@app.route('/get_food_amount', methods=['GET'])
def get_food_amount():
   food_amount = 50
   return {'food_amount': food_amount}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
