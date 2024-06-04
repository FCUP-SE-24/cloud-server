from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests
import json
import threading
import time

app = Flask(__name__)
api = Api(app)

new_bowl_data = {}

# bowls list
bowls_list_request = {'message': False}
bowls_list = {}
data_bowls_ready = threading.Event()

# get weight
weight_request = {'message': False}
weight = 0
weight_ready = threading.Event()

# arduinos number
arduinos_request = {'message': False}
arduinos_avaiable = 0
waiting_for_ard_count = threading.Event()

# daily goal
daily_goal_request = {'message': False}
daily_goal_bowl = 0
daily_goal_ready = threading.Event()

# food amount
food_amount_request = {'message': False}
food_amount_bowl = 0
food_amount_ready = threading.Event()

# last feeding time
last_feeding_time_request = {'message': False}
last_feeding_time = 0
last_feeding_time_ready = threading.Event()

# set daily goal
new_daily_goal_data = {'message': False}


# set feeding time
new_feeding_time = {'message': False}


#add_bowl_ready = threading.Event()

# Database Requests

@app.route('/get_bowls_list', methods=['GET'])
def get_bowls_list():
   bowls_list_request['message'] = True
   data_bowls_ready.wait()
   data_bowls_ready.clear()
   #bowls = ['Bowl 1', 'Bowl 2', 'Bowl 3', 'undefined1', 'undefined'}
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


# changed to comunicate with rpi
@app.route('/get_daily_goal', methods=['GET'])
def get_daily_goal():
   global daily_goal_request
   global daily_goal_bowl
   bowl_name = request.form['bowl_name']
   daily_goal_request = {'message': True, 'bowl_name':bowl_name}
   daily_goal_ready.wait()
   daily_goal_ready.clear()
   return jsonify({'daily_goal': daily_goal_bowl})
   
   
# added to comunicate with rpi
@app.route('/send_daily_goal', methods=['GET','POST'])
def send_daily_goal():
   global daily_goal_request
   global daily_goal_bowl
   if request.method == 'GET':
      return jsonify(daily_goal_request)
   elif request.method == 'POST':
      daily_goal_request = {'message': False}
      data = request.get_json()
      daily_goal_bowl = data['daily_goal']
      daily_goal_ready.set()
      return jsonify({'message':"daily goal send"})


# changed to comunicate with rpi
@app.route('/get_food_amount', methods=['GET'])
def get_food_amount():
   global food_amount_request
   global food_amount_bowl
   bowl_name = request.form['bowl_name']
   food_amount_request = {'message': True, 'bowl_name':bowl_name}
   food_amount_ready.wait()
   food_amount_ready.clear()
   return jsonify({'food_amount': food_amount_bowl})


# added to comunicate with rpi
@app.route('/send_food_amount', methods=['GET','POST'])
def send_food_amount():
   global food_amount_request
   global food_amount_bowl
   if request.method == 'GET':
      return jsonify(food_amount_request)
   elif request.method == 'POST':
      food_amount_request = {'message': False}
      data = request.get_json()
      food_amount_bowl = data['food_amount']
      food_amount_ready.set()
      return jsonify({'message':"food amount send"})


# changed to comunicate with rpi
@app.route('/get_last_feeding_time', methods=['GET'])
def get_last_feeding_time():
   global last_feeding_time_request
   global last_feeding_time
   data = request.args
   bowl_name = data.get('bowl_name')
   last_feeding_time_request = {'message': True, 'bowl_name':bowl_name}
   last_feeding_time_ready.wait()
   last_feeding_time_ready.clear()
   return jsonify({'last_feeding_time': last_feeding_time})
   
   
# added to comunicate with rpi
@app.route('/send_last_feeding_time', methods=['GET','POST'])
def send_last_feeding_time():
   global last_feeding_time_request
   global last_feeding_time
   if request.method == 'GET':
      return jsonify(last_feeding_time_request)
   elif request.method == 'POST':
      last_feeding_time_request = {'message': False}
      data = request.get_json()
      last_feeding_time = data['last_feeding_time']
      last_feeding_time_ready.set()
      return jsonify({'message':"food amount send"})


# changed to comunicate with rpi
@app.route('/get_weight', methods=['GET'])
def get_weight():
   global weight_request
   data = request.args
   bowl_name = data.get('bowl_name')
   weight_request = {'message':True,'bowl_name':bowl_name}
   weight_ready.wait()
   weight_ready.clear()
   return jsonify({'weight': weight})


# added to comunicate with rpi
@app.route('/send_weight', methods=['GET','POST'])
def send_weight():
   global weight_request
   global weight
   if request.method == 'GET':
      return jsonify(weight_request)
   elif request.method == 'POST':
      weight_request = {'message': False}
      data = request.get_json()
      weight = data['weight']
      weight_ready.set()
      return jsonify({'message':"weight send"})


# changed to comunicate with rpi
@app.route('/get_undefined_count', methods=['GET'])
def get_undefined_count():
   global arduinos_request
   global arduinos_avaiable
   arduinos_request['message'] = True
   waiting_for_ard_count.wait()
   waiting_for_ard_count.clear()
   return jsonify({'count': arduinos_avaiable})
     
      
# added to comunicate with rpi
@app.route('/send_arduinos_count', methods=['GET', 'POST'])
def receive_undefined_count():
   global arduinos_request
   global arduinos_avaiable
   if request.method == 'GET':
      return jsonify(arduinos_request)
   elif request.method == 'POST':
      arduinos_request['message'] = False
      data = request.get_json()
      arduinos_avaiable = data['number_arduinos']
      waiting_for_ard_count.set()
      return jsonify({'message':"count send"})


# changed to comunicate with rpi
@app.route('/set_daily_goal', methods=['POST'])
def set_daily_goal():
   global new_daily_goal_data
   bowl_name = request.form['bowl_name']
   daily_goal = request.form['daily_goal']
   new_daily_goal_data = {'message':True,'bowl_name':bowl_name,'daily_goal':daily_goal}
   time.sleep(3)
   return {'message': f'Daily goal of {bowl_name} was successfully changed to {daily_goal}'}
   
   
# added to comunicate with rpi
@app.route('/rpi_set_daily_goal', methods=['GET','POST'])
def rpi_set_daily_goal():
   global new_daily_goal_data
   if request.method == 'POST':
       new_daily_goal_data = {'message': False}
   return jsonify(new_daily_goal_data)


# changed to comunicate with rpi
@app.route('/set_feeding_time', methods=['POST'])
def set_feeding_time():
   global new_feeding_time
   bowl_name = request.form['bowl_name']
   feeding_time = request.form['feeding_time']
   new_feeding_time = {'message':True,'bowl_name':bowl_name,'feeding_time':feeding_time}
   time.sleep(3)
   return {'message': f'Last feeding time set to {feeding_time}'}


# added to comunicate with rpi
@app.route('/rpi_set_feeding_time', methods=['GET','POST'])
def rpi_set_feeding_time():
   global new_feeding_time
   if request.method == 'POST':
       new_daily_goal_data = {'message': False}
   return jsonify(new_feeding_time)

@app.route('/send_bowl', methods=['POST','GET'])
def send_bowl():
   global new_bowl_data
   if request.method == 'POST':
       new_bowl_data = request.get_json()
       #add_bowl_ready.set()
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
