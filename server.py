from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

class Get_Weight(Resource):
    def get(self):
        return jsonify({"message": "34"})

@app.route('/send_weight', methods=['POST'])
def receive_weight():
    if request.method == 'POST':
        data = request.get_json()
        print("data received\n")
        return jsonify({"message": "Data received and processed successfully!"})
    return jsonify({"error": "Invalid data"}), 400

@app.route('/change_motor_state', methods=['POST'])
def change_motor_state():
    if request.method == 'POST':
        activate_motor = request.json.get('activate_motor')
        raspberry_pi_url = 'http://google.com'
        data = {'activate_motor': activate_motor}
        try:
            response = requests.put(raspberry_pi_url, json=data)
            #if response.status_code == 200:
            #    return jsonify({"message": "Mensagem enviada com sucesso"})
            #else:
            #    return jsonify({"error": f"Erro ao enviar mensagem: {response.content.decode('utf-8')}"}), 500
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Erro ao conectar ao Raspberry Pi"}), 500

@app.route('/set_daily_goal', methods=['POST'])
def set_daily_goal():
    if request.method == 'POST':
        daily_goal = request.json.get('daily_goal')
        raspberry_pi_url = 'http://google.com'
        data = {'daily_goal': daily_goal}
        try:
            response = requests.put(raspberry_pi_url, json=data)
            #if response.status_code == 200:
            #    return jsonify({"message": "Mensagem enviada com sucesso"})
            #else:
            #    return jsonify({"error": f"Erro ao enviar mensagem: {response.content.decode('utf->
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Erro ao conectar ao Raspberry Pi"}), 500

api.add_resource(Get_Weight,'/get_weight')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
