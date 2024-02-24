from flask import Flask, jsonify, request
from pypsrp.client import Client

app = Flask(__name__)

client = None  # Define the client variable


def authenticate_client(hostname, port, username, password):
    global client
    try:
        # Initialize the client with the provided credentials
        client = Client(hostname, port=port, username=username, password=password, ssl=False)
        return True
    except Exception as e:
        print(f"Error authenticating: {str(e)}")
        return False


@app.route('/get_run', methods=['GET'])
def get_run():
    try:
        data = request.get_json()
        hostname = data.get('hostname')
        
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')

        auth_success = authenticate_client(hostname, port, username, password)
        if not auth_success:
            return jsonify({'error': 'Failed to authenticate. Check credentials.'})

        result = client.execute_ps("""Get-Service | Where-Object { $_.Status -eq "Running" } | Select-Object -ExpandProperty Name""")
        output = [item.strip() for item in result[0].strip().split('\n')]
        return jsonify({'running': output})
    except Exception as e:
        return jsonify({'Error': str(e)})



@app.route('/get_location', methods=['GET'])
def get_location():
    try:
        data = request.get_json()   
        hostname = data.get('hostname')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')

        auth_success = authenticate_client(hostname, port, username, password)
        if not auth_success:
            return jsonify({'error': 'Failed to authenticate. Check credentials.'})

        result = client.execute_ps("pwd")
        output = [item.strip() for item in result[0].strip().split('\n')]
        return jsonify({'location': output})
    except Exception as e:
        return jsonify({'Error': str(e)})


@app.route('/get_cpu_percent', methods=['GET'])
def get_cpu_percent():
    try:
        data = request.get_json()
        hostname = data.get('hostname')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')

        auth_success = authenticate_client(hostname, port, username, password)
        if not auth_success:
            return jsonify({'error': 'Failed to authenticate. Check credentials.'})

        result = client.execute_ps("""Get-Counter '\Processor(_Total)\% Processor Time' | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue""")
        cpu_percentage = round(float(result[0].strip()), 2)

        return jsonify({'CPU_percentage': [cpu_percentage]})
    except Exception as e:
        return jsonify({'Error': str(e)})

@app.route('/get_ip', methods = ['GET'])
def get_ip():
    try:
        data = request.get_json()
        hostname = data.get('hostname')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        result = client.execute_ps("(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias (Get-NetAdapter | Where-Object {$_.Status -eq 'Up' -and $_.Name -notlike '*Loopback*'}).InterfaceAlias).IPAddress")
        output = [result[0].strip().split('\n')]
        return jsonify({'ip address ': output})
    except Exception as e:
        return jsonify({'Error ': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
