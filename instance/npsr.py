from flask import Flask, jsonify, request
from pypsrp.client import Client

app = Flask(__name__)

client = None  # Define the client variable

@app.route('/set_credentials', methods=['POST'])
def set_credentials():
    global client
    try: 
        data = request.get_json()
        hostname = data.get('hostname')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')

        # Initialize the client with the provided credentials
        client = Client(hostname, port=port, username=username, password=password, ssl=False)
        
        return jsonify({'message': 'Credentials set successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

    
@app.route('/get_run', methods = ['GET'])
def get_run():
    try:
        result = client.execute_ps("""Get-Service | Where-Object { $_.Status -eq "Running" } | Select-Object -ExpandProperty Name""")
        output = [item.strip() for item in result[0].strip().split('\n')]
        return jsonify({'running ' : output})
    except Exception as e:
        return jsonify({'Error ': str(e)})
     
@app.route('/get_ip', methods = ['GET'])
def get_ip():
    try:
        result = client.execute_ps("(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias (Get-NetAdapter | Where-Object {$_.Status -eq 'Up' -and $_.Name -notlike '*Loopback*'}).InterfaceAlias).IPAddress")
        output = [result[0].strip().split('\n')]
        return jsonify({'ip address ': output})
    except Exception as e:
        return jsonify({'Error ': str(e)})

@app.route('/get_host', methods=['GET'])
def get_host():
    if client is None:
        return jsonify({'error': 'Credentials not set. Set credentials using /set_credentials endpoint.'})
    try:
        result = client.execute_ps("hostname")
        output = [result[0].strip()]
        return jsonify({'hostname': output})
    except Exception as e:
        return jsonify({'error': str(e)})

  
@app.route('/location', methods = ['GET'])
def get_loc():
    result = client.execute_ps('PWD')
    output = result[0].strip()
    return jsonify({'output' : output})
   

@app.route('/get_cpu_percent', methods=['GET'])
def get_cpu_percent():
    try:
        result = client.execute_ps("""Get-Counter '\Processor(_Total)\% Processor Time' | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue""")
        
        # Convert the result to a float and round it to two decimal places
        cpu_percentage = round(float(result[0].strip()), 2)

        return jsonify({'CPU_percentage': [cpu_percentage]})
    except Exception as e:
        return jsonify({'ERROR': str(e)})
  
@app.route('/get_stop', methods = ['GET'])
def get_stop():
    try:
        result = client.execute_ps("""Get-Service | Where-Object { $_.Status -eq "stopped" } | Select-Object -ExpandProperty Name""")
        output = [item.strip() for item in result[0].strip().split('\n')]
        return jsonify({'stopped ' : output})
    except Exception as e:
        return jsonify({'Error ': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
