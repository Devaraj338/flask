from flask import Flask, jsonify
from pypsrp.client import Client

app = Flask(__name__)

hostname = "dev.autointelli.com"
port = 15985
username = "administrator"
password = "@ut0!ntell!@123"

def get_client():
    return Client(hostname, username=username, port=port, password=password, ssl=False)

@app.route('/host', methods=['GET'])
def get_host():
    client = get_client()
    result = client.execute_ps('hostname')
    output = result[0].strip()
    return jsonify({'output': output})

@app.route('/loc', methods=['GET'])
def get_loc():
    client = get_client()
    result = client.execute_ps('PWD')
    output = result[0].strip()
    return jsonify({'output': output})

@app.route('/services', methods=['GET'])
def get_running_services():
    client = get_client()
    ps_script = "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object DisplayName, Status"
    result = client.execute_ps(ps_script)
    services = []
    for service in result:
        service_info = service.strip().split()
        service_name = service_info[0]
        service_status = service_info[1]
        services.append({'ServiceName': service_name, 'Status': service_status})
    return jsonify({'services': services})


    
@app.route('/get_ip', methods = ['GET'])
def get_ip():
    try:
        result = client.execute_ps("(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias (Get-NetAdapter | Where-Object {$_.Status -eq 'Up' -and $_.Name -notlike '*Loopback*'}).InterfaceAlias).IPAddress")
        output = [result[0].strip().split('\n')]
        return jsonify({'ip address ': output})
    except Exception as e:
        return jsonify({'Error ': str(e)})
    











if __name__ == "__main__":
    app.run(debug=True)
