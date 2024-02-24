from flask import Flask,jsonify,request
from pypsrp.client import Client

app = Flask(__name__)

hostname = "dev.autointelli.com"
port = 15985
username= "administrator"
password= "@ut0!ntell!@123"

 
client = Client(hostname, port=port, username=username, password=password, ssl=False,)

@app.route('/get_host', methods = ['GET'])
def get_host():
        result = client.execute_ps("hostname")
        output = [result[0].strip()]
        return jsonify({'hostname': output})
   
    
@app.route('/loc', methods = ['GET'])
def get_loc():
    client = Client(hostname,username=username,port=port,password= password, ssl=False)
    result = client.execute_ps('PWD')
    output = result[0].strip()
    return jsonify({'output' : output})
    
@app.route('/get_ip', methods = ['GET'])
def get_ip():
    try:
        result = client.execute_ps("(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias (Get-NetAdapter | Where-Object {$_.Status -eq 'Up' -and $_.Name -notlike '*Loopback*'}).InterfaceAlias).IPAddress")
        output = [result[0].strip().split('\n')]
        return jsonify({'ip address ': output})
    except Exception as e:
        return jsonify({'Error ': str(e)})
    
@app.route('/get_run', methods = ['GET'])
def get_run():
    try:
        result = client.execute_ps("""Get-Service | Where-Object { $_.Status -eq "Running" } | Select-Object -ExpandProperty Name""")
        output = [item.strip() for item in result[0].strip().split('\n')]
        return jsonify({'running ' : output})
    except Exception as e:
        return jsonify({'Error ': str(e)})
    
@app.route('/get_cpu_percent', methods=['GET'])
def get_cpu_percent():
    try:
        result = client.execute_ps("""Get-Counter '\Processor(_Total)\% Processor Time' | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue""")
        
        # Convert the result to a float and round it to two decimal places
        cpu_percentage = round(float(result[0].strip()), 2)

        return jsonify({'CPU_percentage': [cpu_percentage]})
    except Exception as e:
        return jsonify({'ERROR': str(e)})
    
if __name__ == "__main__":
    app.run(debug=True)