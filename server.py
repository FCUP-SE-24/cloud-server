from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests
import json
import threading

app = Flask(__name__)
api = Api(app)

new_bowl_data = {'user_id': "knfjwjwo", 'daily_goal': 70.0, 'bowl_name': "lalalala"}
bowls_list_request = {'message': True}
bowls_list = {}
data_bowls_ready = threading.Event()
daily_goal_request = {'message': False}
add_bowl_ready = threading.Event()

# Database Requests

@app.route('/get_bowls_list', methods=['GET'])
def get_bowls_list():
   bowls_list_request['message'] = True
   data_bowls_ready.wait()
   data_bowls_ready.clear()
   return jsonify(bowls_list)

@app.route('/send_bowls_list', methods=['GET','POST'])
def send_bowls_list():
   global bowls_list
   if request.method == 'GET':
      return jsonify(bowls_list_request)
   elif request.method == 'POST':
      bowls_list_request['message'] = False
      bowls_list = request.get_json()
      data_bowls_ready.set()
      return jsonify({'message':"bowls list send"})

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
   food_amount = 70
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

@app.route('/get_undefined_count', methods=['GET'])
def get_undefined_count():
      # get number of bowls without name
      # query to database
      return {'count': 2}

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

@app.route('/send_bowl', methods=['POST','GET'])
def send_bowl():
   global new_bowl_data
   if request.method == 'POST':
       new_bowl_data = request.get_json()
       #add_bowl_ready.set()
   print(new_bowl_data)
   #elif request.method == 'GET':
   return jsonify(new_bowl_data)
   #new_bowl = request.form['bowl_name']
   #daily_goal = request.form['daily_goal']
   #new_bowl_data = request.get_json()
   #return {'message': f'Bowl {new_bowl} added successfully with daily goal of {daily_goal}'}


@app.route('/add_bowl', methods=['POST'])
def add_bowl():
   global new_bowl_data
   user_id = request.form['user_id']
   daily_goal = request.form['daily_goal']
   bowl_name = request.form['bowl_name']
   new_bowl_data = {'user_id':user_id, 'daily_goal':daily_goal, 'bowl_name':bowl_name}
   #new_bowl_data = request.get_json()
   #add_bowl_ready.wait()
   #add_bowl_ready.clear()
   return jsonify({'message': "New bowl added"})

# ----------

# Other types of requests

@app.route('/control_motor', methods=['POST'])
def control_motor():
   bowl_name = request.form['bowl_name']
   # Get the 'activate_motor' value from the request
   activate_motor = request.form['activate_motor']

    # Prepare the data to send to the Raspberry Pi
   #  data = {'message': 'on' if activate_motor == 'on' else 'off'}

   #  try:
   #      # Send the data to the Raspberry Pi
   #      response = requests.post(RASPBERRY_PI_URL, json=data)

   #      # Check if the request was successful
   #      if response.status_code == 200:
   #          return jsonify(data)
   #      else:
   #          return jsonify({'error': f"Failed to control motor: {response.content.decode('utf-8')}"}), 500
   #  except requests.exceptions.RequestException as e:
   #      return jsonify({'error': 'Failed to connect to Raspberry Pi'}), 500
   state = 'on' if request.form['activate_motor']== 'on' else 'off'
   return {'message': f'Motor is {state} for bowl {bowl_name}'}

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
